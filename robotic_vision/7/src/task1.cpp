#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <cmath>
// #include <pybind11/pybind11.h>

// namespace py = pybind11;
using namespace std;

vector<cv::Point2d> find_features(const cv::Mat &img) 
{
    vector<cv::Point2d> features;
    cv::Mat gray;
    int max_corners(100);
    double quality(0.01), min_dist(10.0);
    cv::Rect roi(cv::Point2d(294, 172), cv::Point2f(369, 362));

    cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);
    cv::goodFeaturesToTrack(gray(roi), features, max_corners, quality, min_dist);

    return features;
}

cv::Point2f get_point(cv::Point2f pt, int w, const cv::Mat &img)
{
  float x, y;
  if(pt.x > img.cols - w/2.0)
    x = img.cols - w;
  else if(pt.x < w/2.0)
    x = 0;
  else
    x = pt.x- w/2.0;
  if(pt.y > img.rows - w/2.0)
    y = img.rows - w;
  else if(pt.y < w/2.0)
    y = 0;
  else
     y = pt.y - w/2.0;

  return cv::Point2f(x, y);
}


void track_features(vector<cv::Point2d> &feats, vector<cv::Point2d> &prev_feats, 
                    const cv::Mat &img, const cv::Mat &prev_img)
{
    int w(5);
    int ws(11*w);
    cv::Size templ_size{w, w};
    cv::Size search_size(ws, ws);
    int match_method = cv::TM_SQDIFF_NORMED;

    feats.clear();
    for (cv::Point2d pt : prev_feats)
    {
        cv::Point2d templ_pt = get_point(pt, w, prev_img);
        cv::Rect templ_roi(templ_pt, templ_size);
        cv::Mat templ_img = prev_img(templ_roi);
        cv::Point2d search_pt = get_point(pt, ws, prev_img);
        cv::Rect search_roi(search_pt, search_size);
        cv::Mat search_img = img(search_roi);

        int res_cols = search_img.cols - templ_img.cols + 1;
        int res_rows = search_img.rows - templ_img.rows + 1;
        cv::Mat result;
        result.create(res_rows, res_cols, CV_32FC1);
        matchTemplate(search_img, templ_img, result, match_method);
        cv::normalize(result, result, 0, 1, cv::NORM_MINMAX, -1, cv::Mat());

        double minVal;
        double maxVal;
        cv::Point matchLoc, minLoc, maxLoc;
        cv::minMaxLoc(result, &minVal, &maxVal, &minLoc, &maxLoc, cv::Mat());
        matchLoc.x = int(pt.x - res_cols / 2.0 + minLoc.x);
        matchLoc.y = int(pt.y - res_rows / 2.0 + minLoc.y);

        feats.push_back(matchLoc);
    }

    cv::Mat status, F;
    F = cv::findFundamentalMat(prev_feats, feats, cv::FM_RANSAC, 3, 0.99, status);

    vector<cv::Point2d> temp, temp_prev;
    for (int i=0; i < status.rows; i++)
    {
        if (status.at<uchar>(i, 0))
        {
            temp.push_back(feats[i]);
            temp_prev.push_back(prev_feats[i]);
        }
    }

    feats = temp;
    prev_feats = temp_prev;
}

void calc_time2impact(vector<cv::Point2d> feats, vector<cv::Point2d> prev_feats,
                      vector<double> &t_vec)
{
    int counter(0);
    double sum(0), mean(0), y(0), y_prev(0), a(0), t(0);
    for (int i=0; i < feats.size(); i++)
    {
        y = feats[i].y;
        y_prev = prev_feats[i].y;

        a = y / y_prev; 
        t = a / (a-1); // seconds to impact

        if (t < 0 || isinf(t) || isnan(t) )
            continue;
        
        sum += t;
        counter++;
    }
    mean = sum / counter;
    t_vec.push_back(mean);
}

int main() 
{
    cv::FileStorage fin("../params/cam_params.yaml", cv::FileStorage::READ);
    cv::Mat M, dist;
    fin["mtx"] >> M;
    fin["dist"] >> dist;
    fin.release();


    vector<cv::Point2d> feats, prev_feats, orig_feats;
    string path("../imgs/T");
    cv::Mat img, prev_img;
    img = cv::imread(path + "1" + ".jpg");
    img.copyTo(prev_img);
    
    orig_feats = find_features(img);
    prev_feats = orig_feats;

    int end = 19;
    vector<double> t_vec;

    for (int i=2; i < end; i++)
    {
        track_features(feats, prev_feats, img, prev_img);
        calc_time2impact(feats, prev_feats, t_vec);
    }
    
    cout << "t: [" << t_vec[0];
    for (int i=1; i < t_vec.size(); i++)
    {
        cout << ", " << t_vec[i]; 
    }
    cout << "]\n";

    for (cv::Point2d pt : feats)
        cv::circle(img, pt, 3, cv::Scalar(0,0,255), -1);
    for (cv::Point2d pt : prev_feats)
        cv::circle(prev_img, pt, 3, cv::Scalar(0,255,0), -1);

    cv::imshow("Image", img);
    cv::imshow("Prev", prev_img);
    cv::waitKey(0);
    
    return 0;
}