#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <cmath>

using namespace std;

vector<cv::Point2d> find_features(const cv::Mat &img) 
{
    vector<cv::Point2d> features;
    cv::Mat gray;
    int max_corners(100);
    double quality(0.01), min_dist(10.0);

    cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);
    cv::goodFeaturesToTrack(img, features, max_corners, quality, min_dist);

    // POSSIBLY CROP TO ROI HERE //

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

    int end = 19;
    for (int i=2; i < end; i++)
    {
        prev_feats = orig_feats;
        track_features(feats, prev_feats, img, prev_img);
        calc_time2impact(feats, prev_feats, );
    }
    
    return 0;
}