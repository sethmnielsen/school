#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <string>
#include <iostream>
#include <glob.h>
#include <vector>

// #define SHOW

cv::Point2d getPoint(cv::Point2d pt, int size, const cv::Mat& img)
{
    double x,y;
    if(pt.x > img.cols - size/2.0)
        x = img.cols - size;
    else if(pt.x < size/2.0)
        x = 0;
    else
        x = pt.x- size/2.0;
    if(pt.y > img.rows - size/2.0)
        y = img.rows - size;
    else if(pt.y < size/2.0)
        y = 0;
    else
        y = pt.y - size/2.0;

  return cv::Point2d(x, y);
}

void featureMatch(const std::vector<cv::Point2d>& prev_corners, const cv::Mat& prev_img,
                  const cv::Mat& img, std::vector<cv::Point2d>& new_corners)
{
    new_corners.clear();
    int ts{5};
    int ss{12*ts};
    cv::Size template_size{ts,ts};
    cv::Size search_size{ss,ss};
    int method{cv::TM_SQDIFF_NORMED};
    for (cv::Point2d pt : prev_corners)
    {
        cv::Point2d template_pt{getPoint(pt,ts,prev_img)};
        cv::Rect template_roi{template_pt,template_size};
        cv::Mat template_img{prev_img(template_roi)};

        cv::Point2d search_pt{getPoint(pt,ss,prev_img)};
        cv::Rect search_roi{search_pt,search_size};
        cv::Mat search_img{img(search_roi)};

        int result_cols{search_img.cols - template_img.cols + 1};
        int result_rows{search_img.rows - template_img.rows + 1};
        cv::Mat result;
        result.create(result_rows, result_cols, CV_32FC1);
        cv::matchTemplate(search_img, template_img, result, method);
        cv::normalize(result, result, 0, 1, cv::NORM_MINMAX, -1, cv::Mat());

        double min_val, max_val;
        cv::Point match_loc, min_loc, max_loc;
        cv::minMaxLoc(result, &min_val, &max_val, &min_loc, &max_loc, cv::Mat());
        match_loc.x = int(pt.x - result_cols/2.0 + min_loc.x);
        match_loc.y = int(pt.y - result_rows/2.0 + min_loc.y);

        new_corners.push_back(match_loc);
    }
}

void getF(std::string glob_path, std::vector<cv::Point2d>& original_pts,
             std::vector<cv::Point2d>& end_pts, cv::Mat& F, cv::Mat& first_img,
          cv::Mat& last_img)
{
    // get all of the img filenames in a vector
    glob_t result;
    glob(glob_path.c_str(), GLOB_TILDE, NULL,&result);
    std::vector<std::string> filenames;
    for (size_t i{0}; i < result.gl_pathc; i++)
    {
        filenames.push_back(std::string(result.gl_pathv[i]));
    }
    // grab the first image
    cv::Mat prev_img, prev_img_g, img, img_g;
    prev_img = cv::imread(filenames[0]);
    cv::cvtColor(prev_img,prev_img_g,cv::COLOR_BGR2GRAY);
    prev_img.copyTo(first_img);

    std::vector<cv::Point2d> prev_corners, original_corners, new_corners;
    int max_corners{500};
    double quality{0.01}, min_distance{23.0};
    cv::goodFeaturesToTrack(prev_img_g, prev_corners, max_corners, quality, min_distance);
    original_corners = prev_corners;

    for (std::string filename : filenames)
    {
        img = cv::imread(filename);
        cv::cvtColor(img, img_g, cv::COLOR_BGR2GRAY);
        cv::Mat temp_img;
        img.copyTo(temp_img);

        featureMatch(prev_corners, prev_img_g, img_g, new_corners);

        cv::Mat status;
        F = cv::findFundamentalMat(prev_corners,new_corners,cv::FM_RANSAC,3,0.99,status);

        prev_corners.clear();
        std::vector<cv::Point2d> temp;
        for (int i{0}; i < status.rows; i++)
        {
            if (status.at<uchar>(i,0))
            {
                prev_corners.push_back(new_corners[i]);
                temp.push_back(original_corners[i]);
            }
        }
        original_corners = temp;
        img_g.copyTo(prev_img_g);

        for (int i{0}; i < prev_corners.size(); i++)
        {
            cv::circle(temp_img, original_corners[i], 2, cv::Scalar(0,255,0), -1);
            cv::line(temp_img, original_corners[i], prev_corners[i], cv::Scalar(0,0,255),1);
        }
#ifdef SHOW
        cv::imshow("Debug",temp_img);
        cv::waitKey(0);
#endif
    }
    original_pts = original_corners;
    end_pts = prev_corners;
    last_img = cv::imread(filenames[5]);
}

void rectify(std::string dir)
{
    std::string path{"../"+dir+"/*.jpg"};
    std::vector<cv::Point2d> original_pts, final_pts;
    cv::Mat F, first_img, last_img;
    getF(path, original_pts, final_pts, F, first_img, last_img);

    cv::Mat H1, H2;
    cv::stereoRectifyUncalibrated(original_pts, final_pts, F, first_img.size(), H1, H2);
    std::cout << "original_pts size: " << original_pts.size() << std::endl;
    std::cout << "final_pts size: " << final_pts.size() << std::endl;
    std::cout << "H1: " << H1 << std::endl;

    cv::FileStorage in{"../guess_params.yaml", cv::FileStorage::READ};
    cv::Mat M, dist;
    in["Cam_Mat"] >> M;
    in["Distortion"] >> dist;
    in.release();

    cv::Mat R1, R2;
    R1 = M.inv()*H1*M;
    R2 = M.inv()*H2*M;
    std::cout << "R1: " << R1 << std::endl;

    cv::Size img_size{640,480};
    cv::Mat map1_1, map1_2, map2_1, map2_2, first_rect, last_rect;
    cv::initUndistortRectifyMap(M, dist, R1, M, img_size, 5, map1_1, map1_2);
    remap(first_img, first_rect, map1_1, map1_2, cv::INTER_LINEAR);
    cv::initUndistortRectifyMap(M, dist, R2, M, img_size, 5, map2_1, map2_2);
    remap(last_img, last_rect, map2_1, map2_2, cv::INTER_LINEAR);

    for (int i{1}; i < 21; i++)
    {
        cv::Point left_pt{0, 25*i};
        cv::Point right_pt{800, 25*i};
        cv::line(first_rect,left_pt,right_pt,cv::Scalar(0,0,255),1);
        cv::line(last_rect,left_pt,right_pt,cv::Scalar(0,0,255),1);
    }

    cv::imshow("Rectified 1st Frame",first_rect);
    cv::imshow("Rectified Last Frame", last_rect);
    cv::waitKey(0);
}

int main()
{
    rectify("Parallel_Cube");
    rectify("Parallel_Real");
    rectify("Turned_Cube");
    rectify("Turned_Real");

    return 0;
}