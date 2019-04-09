#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <glob.h>

using namespace std;
using namespace cv;

vector<Point2d> undistortConvert2CamFrame(vector<Point2d> corners, Mat M, Mat dist);
Point2d point_corrected(Point2d pt, int w, const Mat &img);
void sfm(string sequence);
void display_img(Mat img, string title = "Image", int t = 0);

void sfm(string sequence)
{
    string dir = "/home/seth/school/robotic_vision/6/imgs/";
    string image_sequence = dir + sequence + "1%0d.jpg";
    VideoCapture cap(image_sequence, cv::CAP_IMAGES);
    int m = cv::CAP_PROP_FRAME_COUNT - 1;
    vector<Mat> imgs(6);
    
    namedWindow("original");
    namedWindow("final");
    moveWindow("final", 800, 20);

    int w(5);
    int ws = w * 12;
    Size templateSize(w, w), searchSize(ws, ws);
    int match_method = cv::TM_SQDIFF_NORMED;

    int MAX_CORNERS(500);
    double QUALITY(0.01), MIN_DIST(25.0);

    vector<Point2d> new_corners, prev_corners, orig_corners, final_corners, temp;

    cv::FileStorage fin("/home/seth/school/robotic_vision/6/cam_mat.yaml", cv::FileStorage::READ);
    Mat M, dist;
    fin["mtx"] >> M;
    fin["dist"] >> dist;
    fin.release();

    Mat F, H1, H2; // fundamental matrix, homography matrices

    Mat frame, prev_frame, gray, prev_gray, mask, img;
    cap >> frame;
    cvtColor(frame, prev_gray, COLOR_BGR2GRAY);
    frame.copyTo(imgs[0]);
    frame.copyTo(prev_frame);
    prev_gray.copyTo(gray);

    goodFeaturesToTrack(prev_gray, prev_corners, MAX_CORNERS, QUALITY, MIN_DIST);
    orig_corners = prev_corners;
    mask = Mat::ones(prev_corners.size(), 1, CV_16U);

    // for (int i = 0; i < orig_corners.size(); i++)
        // circle(img, orig_corners[i], 3, Scalar(0, 255, 0), -1);
    // display_img(img);

    for (int j = 0; j < m; j++)
    {
        if (j != 0)
        {
            cap >> frame;
            // frame = imread(filename);
            if (frame.empty())
                break;
            frame.copyTo(imgs[j]);
        }

        cvtColor(frame, gray, COLOR_BGR2GRAY);

        new_corners.clear();
        for (Point2d pt : prev_corners)
        {
            Point2d templ_pt = point_corrected(pt, w, prev_frame);
            Rect templ_roi(templ_pt, templateSize);
            Mat templ = prev_frame(templ_roi);
            Point2d search_pt = point_corrected(pt, ws, prev_frame);
            Rect search_roi(search_pt, searchSize);
            Mat search_box = frame(search_roi);

            int res_cols = search_box.cols - templ.cols + 1;
            int res_rows = search_box.rows - templ.rows + 1;
            Mat result;
            result.create(res_rows, res_cols, CV_32FC1);
            matchTemplate(search_box, templ, result, match_method);
            cv::normalize(result, result, 0, 1, cv::NORM_MINMAX, -1, Mat());

            double minVal;
            double maxVal;
            cv::Point matchLoc, minLoc, maxLoc;
            cv::minMaxLoc(result, &minVal, &maxVal, &minLoc, &maxLoc, cv::Mat());
            matchLoc.x = int(pt.x - res_cols / 2.0 + minLoc.x);
            matchLoc.y = int(pt.y - res_rows / 2.0 + minLoc.y);

            new_corners.push_back(matchLoc);
        }
        
        prev_corners = undistortConvert2CamFrame(prev_corners, M, dist);
        new_corners = undistortConvert2CamFrame(new_corners, M, dist);
        
        F = findFundamentalMat(prev_corners, new_corners, cv::FM_RANSAC,
                           3, 0.99, mask);
        prev_corners.clear();
        temp.clear();
        for (int i = 0; i < mask.rows; i++)
        {
            if (mask.at<uchar>(i,0))
            {
                prev_corners.push_back(new_corners[i]);
                temp.push_back(orig_corners[i]);
            }
        }
        orig_corners = temp;
        gray.copyTo(prev_gray);
        frame.copyTo(prev_frame);

        // for (int i = 0; i < prev_corners.size(); i++)
        // {
        //     circle(img, orig_corners[i], 3, Scalar(0, 255, 0), -1);
        //     line(img, orig_corners[i], prev_corners[i], Scalar(0, 0, 255), 1);
        // }

    }
    cap.release();
    final_corners = prev_corners;

    cout << "\nRESULTS FOR SEQUENCE " << sequence << ":\n\n";

    std::cout << "orig_corners size: " << orig_corners.size() << std::endl;
    std::cout << "final_corners size: " << final_corners.size() << std::endl;

    F = findFundamentalMat(orig_corners, final_corners, cv::FM_RANSAC,
                            3, 0.99, mask);

    Mat E, R1, R2, t, R;
    E = M.t() * F * M;
    cv::decomposeEssentialMat(E, R1, R2, t);
    double error1 = abs(3 - cv::trace(R1).val[0]);
    double error2 = abs(3 - cv::trace(R2).val[0]);

    if (sequence.substr(0,8) == "Parallel")
    {
        if (error1 < error2)
        {   
            R = R1;
            cout << "R == R1:\n" << R1 << endl;
        }
        else
        {   
            R = R2;
            cout << "R == R2:\n" << R2 << endl;
        }
        t *= 2.7;
    }
    else
    {
        if (error1 > error2)
        {   
            R = R1;
            cout << "R == R1: \n" << R1 << endl;
        }
        else
        {   
            R = R2;
            cout << "R == R2: \n" << R2 << endl;
        }
        t *= 2.3;
    }
    if (t.at<double>(0) > 0)
        cout << "t: \n" << t << endl;
    else
    {
        t = -t;
        cout << "t == -t: \n" << t << endl;
    }

    Size img_size{640,480};
    Mat P1, P2, Q;
    cv::stereoRectify(M,dist,M,dist,img_size, R, t, R1, R2, P1, P2, Q);
    Mat img_orig, img_final;
    imgs[0].copyTo(img_orig);
    imgs.back().copyTo(img_final);

    vector<Point3d> first_points;
    // PC: 0, 1, 12, 13
    // PR: 0, 3, 7, 10
    // TC: 2, 9, 12, 16
    // TR: 9, 0, 4, 8
    vector<int> inds{9, 0, 4, 8};
    for (int i=0; i < inds.size(); i++)
    {
        Point2d oc = orig_corners[inds[i]];
        Point2d fc = final_corners[inds[i]];
        Point3d pt_first(oc.x, oc.y, fc.x - oc.x);
        first_points.push_back(pt_first);

        circle(img_orig, oc, 5, Scalar(0,0,255), -1);
        circle(img_final, fc, 5, Scalar(0,0,255), -1);
    }

    vector<Point3d> obj_points;
    perspectiveTransform(first_points, obj_points, Q);

    std::cout << "F:\n" << F << std::endl;
    std::cout << "E:\n" << E << std::endl;
    std::cout << "t:\n" << t << std::endl;
    std::cout << "R1:\n" << R1 << std::endl;
    std::cout << "R2:\n" << R2 << std::endl;
    std::cout << "Q:\n" << Q << std::endl;

    std::cout << "\nfirst_points: \n\t";
    for (int i=0; i < first_points.size(); i++)
    {
        cout << first_points[i] << "\n\t";
    }
    
    std::cout << "\n\n3D points:" << std::endl;
    for (int i=0; i < obj_points.size(); i++)
        std::cout << obj_points[i] << std::endl;

    imshow("original", img_orig);
    imshow("final", img_final);
    char c = (char)waitKey(0);
    if (c == 'q')
    {
        destroyAllWindows();
        exit(0);
    }
    else if (c == 't')
    {
        imwrite("results/" + sequence + "_t3.jpg", img_orig);
    }
}

// Functions

vector<Point2d> undistortConvert2CamFrame(vector<Point2d> corners, Mat M, Mat dist)
{
    double fx{M.at<double>(0, 0)};
    double fy{M.at<double>(1, 1)};
    double Ox{M.at<double>(0, 2)};
    double Oy{M.at<double>(1, 2)};

    undistortPoints(corners, corners, M, dist);

    for (int i=0; i < corners.size(); i++)
    {
        corners[i].x = corners[i].x * fx + Ox;
        corners[i].y = corners[i].y * fy + Oy;
    }
    return corners;
}

Point2d point_corrected(Point2d pt, int w, const Mat &img)
{
    double x, y;

    if (pt.x > img.cols - w / 2.0)
        x = img.cols - w;
    else if (pt.x < w / 2.0)
        x = 0;
    else
        x = pt.x - w / 2.0;
    if (pt.y > img.rows - w / 2.0)
        y = img.rows - w;
    else if (pt.y < w / 2.0)
        y = 0;
    else
        y = pt.y - w / 2.0;

    return Point2d(x, y);
}

void display_img(Mat img, string title, int t)
{
    if (img.empty())
    {
        cout << "Image empty!" << endl;
        return;
    }

    cv::imshow(title, img);
    char c = (char)waitKey(t);
    if (c == 'q')
    {
        destroyAllWindows();
        exit(0);
    }
}

int main()
{
    // sfm("ParallelCube");
    // sfm("ParallelReal");
    // sfm("TurnCube");
    sfm("TurnReal");
    return 0;
}