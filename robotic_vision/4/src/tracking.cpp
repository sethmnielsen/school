#include <opencv2/opencv.hpp>
#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <sstream>
#include <filesystem>

namespace fs = std::filesystem;
using namespace std;

typedef vector<fs::path> pvec;

struct CamData {
    string name;
    cv::Mat img0, mtx, dist, R, P;
    vector<cv::Point2f> pts, output_pts;
    vector<cv::Point3f> persp, pts_3d;
    cv::Rect roi;
    pvec img_files;
    vector<cv::KeyPoint> keypoints;
};

cv::SimpleBlobDetector::Params set_params();
bool find_ball(CamData &cam, cv::Ptr<cv::SimpleBlobDetector> &detector, int i);
void track_ball(CamData &cam, int i);

int main()
{   
    CamData camL, camR;
    camL.name = "Left";
    camR.name = "Right";

    pvec files;
    fs::path p("/home/seth/school/robotic_vision/4/bb_imgs/1");
    copy(fs::directory_iterator(p), fs::directory_iterator(), back_inserter(files));
    sort(files.begin(), files.end());
    camL.img_files = pvec(files.begin(), files.begin() + (files.size()/2));
    camR.img_files = pvec(files.begin() + (files.size()/2), files.end());

    int w(300);
    camL.roi = cv::Rect(350, 50, w, w);
    camR.roi = cv::Rect(225, 50, w, w);

    cv::SimpleBlobDetector::Params params = set_params();
    cv::Ptr<cv::SimpleBlobDetector> detector = cv::SimpleBlobDetector::create(params);
    // Set initial image and crop it
    cv::Mat bgL = cv::imread( string(camL.img_files[0]) )( camL.roi );
    cv::Mat bgR = cv::imread( string(camR.img_files[0]) )( camR.roi );
    cv::cvtColor( bgL, camL.img0, cv::COLOR_BGR2GRAY );
    cv::cvtColor( bgR, camR.img0, cv::COLOR_BGR2GRAY );

    // cv::imshow("window", camL.img0);
    // cv::waitKey(0);

    for (int i=1; i < camL.img_files.size(); i++)
    {
        if (find_ball(camL, detector, i) && find_ball(camR, detector, i)) 
        {
            track_ball(camL, i);
            track_ball(camR, i);
        }
        cv::Mat img = cv::imread(string(camL.img_files[i]));
        img = img(camL.roi);
        cv::Mat gray, enlarged;
        cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);      
        cv::resize(gray, enlarged, cv::Size(gray.cols*3, gray.rows*3), cv::INTER_NEAREST);
        cv::imshow("window", enlarged);
        cv::waitKey(100);
    }

    return 0;
}

bool find_ball(CamData &cam, cv::Ptr<cv::SimpleBlobDetector> &detector, int i)
{
    bool found_ball(false);

    cv::Mat img, gray, enlarged;
    img = cv::imread(string(cam.img_files[i]));
    img = img(cam.roi);
    cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);

    cv::Mat frame;
    cv::absdiff(cam.img0, gray, frame);
    cv::threshold(frame, frame, 20, 255, 0);
    cv::Mat element = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(7,7));
    cv::erode(frame, frame, element);
    cv::dilate(frame, frame, element);

    detector->detect(frame, cam.keypoints);

    if (cam.keypoints.size()) { found_ball = true; }
    
    return found_ball;
}

void track_ball(CamData &cam, int i)
{
    // cv::Point2f pos()
    // stringstream ss;
    // ss << cam.name << " Keypoint " << i << ": ( " << cam.keypoints[i].pt.x << ", "
                                                //   << cam.keypoints[i].pt.y << " )\n";
    // cout << ss.str();
}

cv::SimpleBlobDetector::Params set_params()
{
    cv::SimpleBlobDetector::Params params;
    params.minThreshold = 100;
    params.maxThreshold = 255;
    params.filterByColor = true;
    params.blobColor = 255;
    // params.filterByArea = false;
    // params.filterByCircularity = false;
    // params.filterByConvexity = false;
    // params.filterByInertia = false;

    return params;
}