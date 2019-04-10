#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;
using namespace std;

class Task1
{
public:
    vector<cv::Point2f> find_features(const cv::Mat &img) 
    {
        vector<cv::Point2f> features;
        cv::Mat gray;
        int max_corners(200);
        double quality(0.01), min_dist(5.0);

        cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);
        cv::goodFeaturesToTrack(gray, features, max_corners, quality, min_dist);

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

    void track_features2(vector<cv::Point2f> &feats, vector<cv::Point2f> &prev_feats, 
                        const cv::Mat &img, const cv::Mat &prev_img)
    {
        cv::TermCriteria crit{cv::TermCriteria::COUNT + cv::TermCriteria::EPS, 40, 0.001};
        vector<uchar> status;
        vector<float> err;
        cv::Mat gray, prev_gray;
        cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);
        cv::cvtColor(prev_img, prev_gray, cv::COLOR_BGR2GRAY);
        cv::calcOpticalFlowPyrLK(prev_gray, gray, prev_feats, feats, status, err,
                                cv::Size(31, 31), 3, crit, 0, 0.01);

        vector<cv::Point2f> temp, prev_temp;
        for (int i=0; i < prev_feats.size(); i++)
        {
            if ( status[i] && err[i] < 20 )
            {
                temp.push_back(feats[i]);
                prev_temp.push_back(prev_feats[i]);
            }
        }

        feats = temp;
        prev_feats = prev_temp;
    }

    void track_features(vector<cv::Point2f> &feats, vector<cv::Point2f> &prev_feats, 
                        const cv::Mat &img, const cv::Mat &original_img)
    {
        int w(5);
        int ws(11*w);
        cv::Size templ_size{w, w};
        cv::Size search_size(ws, ws);
        int match_method = cv::TM_SQDIFF_NORMED;

        feats.clear();
        for (cv::Point2f pt : prev_feats)
        {
            cv::Point2f templ_pt = get_point(pt, w, original_img);
            cv::Rect templ_roi(templ_pt, templ_size);
            cv::Mat templ_img = original_img(templ_roi);
            cv::Point2f search_pt = get_point(pt, ws, original_img);
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

        vector<cv::Point2f> temp, temp_prev;
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

    void calc_time2impact(vector<cv::Point2f> feats, vector<cv::Point2f> prev_feats,
                        vector<double> &t_vec)
    {
        double sum(0), mean(0), a(0), t(0);
        double x1(0), x2(0), x1_prev(0), x2_prev(0);
        vector<vector<cv::Point2f>> pairs(2, vector<cv::Point2f>(2));
        vector<vector<cv::Point2f>> prev_pairs(2, vector<cv::Point2f>(2));
        int j = 0;
        for (int i=0; i < feats.size(); i++)
        {
            if (j > 1)
                break;

            if (feats[i].x == prev_feats[i].x)
                continue;
                
            if (pairs[j][0].x == 0 && feats[i].x < 310)
            {
                pairs[j][0] = feats[i];
                prev_pairs[j][0] = prev_feats[i];

                x1 = pairs[j][0].x;
                x1_prev = prev_pairs[j][0].x;
            }
            else if (pairs[j][1].x == 0 && feats[i].x > 330)
            {
                pairs[j][1] = feats[i];
                prev_pairs[j][1] = prev_feats[i];

                x2 = pairs[j][1].x;
                x2_prev = prev_pairs[j][1].x;

                a = (x2 - x1) / (x2_prev - x1_prev); 
                t = a / (a-1); // seconds to impact

                if (t < 0 || isinf(t) || isnan(t) )
                {
                    pairs[j][0] = cv::Point2f(0,0);
                    pairs[j][1] = cv::Point2f(0,0);
                    continue;
                }
                
                sum += t;
                j++;
            }
        }
        mean = sum / j;
        t_vec.push_back(mean);
    }

    py::array run(bool display) 
    {
        cv::FileStorage fin("../params/cam_params.yaml", cv::FileStorage::READ);
        cv::Mat M, dist;
        fin["mtx"] >> M;
        fin["dist"] >> dist;
        fin.release();


        vector<cv::Point2f> feats, prev_feats, orig_feats;
        string path("../imgs/T");
        cv::Mat img, original_img, prev_img, result, prev_result, gray, orig_gray;
        original_img = cv::imread(path + "1" + ".jpg");
        original_img.copyTo(img);

        if (display)
        {
            cv::namedWindow("original");
            cv::namedWindow("image");
            cv::moveWindow("original", 800, 20);
        }
        
        // cv::Rect roi(cv::Point2f(294, 172), cv::Point2f(363, 362));
        // cv::Rect roi(cv::Point2f(0, 0), cv::Point2f(640, 480));
        cv::Rect roi{cv::Point2f{50, 182}, cv::Point2f{600, 342}};
        orig_feats = find_features( original_img(roi) );
        int end = 19;
        vector<double> t_vec;
        prev_feats = orig_feats;
        for(int i=0; i < orig_feats.size(); i++)
        {
            orig_feats[i].x += roi.x;
            orig_feats[i].y += roi.y;
        }    
        for (int i=2; i < end; i++)
        {
            prev_feats = orig_feats;
            img = cv::imread(path + to_string(i) + ".jpg");
            track_features(feats, prev_feats, img, original_img);
            calc_time2impact(feats, prev_feats, t_vec);

            img.copyTo(result);
            original_img.copyTo(prev_result);

            for (cv::Point2f pt : feats)
                cv::circle(result, pt, 3, cv::Scalar(0,0,255), -1);
            for (cv::Point2f pt : prev_feats)
                cv::circle(prev_result, pt, 3, cv::Scalar(0,255,0), -1);

            if (display)
            {
                cv::imshow("image", result);
                cv::imshow("original", prev_result);
                char c = (char)cv::waitKey(0);
                if ( c == 'q' )
                    exit(0);
            }
        }
        
        // cout << "t: [" << t_vec[0];
        // for (int i=1; i < t_vec.size(); i++)
        // {
        //     cout << ", " << t_vec[i]; 
        // }
        // cout << "]\n";
        return py::array(t_vec.size(), t_vec.data());
    }
};

PYBIND11_MODULE(task1_py, m) {
    py::class_<Task1>(m, "Task1")
        .def(py::init<>())
        .def("run", &Task1::run);
}
