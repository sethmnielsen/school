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
    cv::Rect roi;
    pvec img_files;
    vector<cv::Mat> imgs;
    vector<vector<cv::KeyPoint>> keypoints;
};

bool find_ball(CamData &cam, cv::Ptr<cv::SimpleBlobDetector> &detector, int i);
void find_middle(vector<cv::KeyPoint> &kps);
void track_ball(CamData &cam, int i);
void display_img(CamData &cam, cv::Mat img, string title);
const cv::SimpleBlobDetector::Params set_params();
void create_windows(CamData &camL, CamData &camR);

int main(int argc, char** argv)
{   
    CamData camL, camR;
    camL.name = "Left";
    camR.name = "Right";

    pvec files;
    string n = "2";
    if (argc > 1) { n = argv[1]; }
    string dir = "/home/seth/school/robotic_vision/4/bb_imgs/" + n;
    fs::path p(dir);
    copy(fs::directory_iterator(p), fs::directory_iterator(), back_inserter(files));
    sort(files.begin(), files.end());
    camL.img_files = pvec(files.begin(), files.begin() + (files.size()/2));
    camR.img_files = pvec(files.begin() + (files.size()/2), files.end());

    int w(200);
    camL.roi = cv::Rect(350, 0, w, w);
    camR.roi = cv::Rect(100, 0, w, w);

    const cv::SimpleBlobDetector::Params params = set_params();
    cv::Ptr<cv::SimpleBlobDetector> detector = cv::SimpleBlobDetector::create(params);

    create_windows(camL, camR);

    int t = 0;
    for (int i=0; i < camL.img_files.size(); i++)
    {   
        bool ballL = find_ball(camL, detector, i);
        bool ballR = find_ball(camR, detector, i);
        if (ballL && ballR) 
        {   
            t = 100;
            track_ball(camL, i);
            track_ball(camR, i);
        }
        else
        {
            t = 10;
            display_img(camL, camL.imgs[i], camL.name);
            display_img(camR, camR.imgs[i], camR.name);
        }
        if (cv::waitKey(t) == 113) break;
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
    cam.imgs.push_back(gray);
    if (i == 0)
    {
        vector<cv::KeyPoint> kp;
        cam.keypoints.push_back(kp);
        return false;
    }

    cv::Mat bin;
    cv::absdiff(cam.imgs[0], gray, bin);
    cv::threshold(bin, bin, 20, 255, 0);
    cv::Mat element = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(7,7));
    cv::erode(bin, bin, element);
    cv::dilate(bin, bin, element);

    vector<cv::KeyPoint> kps;
    detector->detect(bin, kps);

    if (kps.size()) { found_ball = true; }
    if (kps.size() > 1) { find_middle(kps); }

    cam.keypoints.push_back(kps);
    
    string title = "Binary " + cam.name;
    display_img(cam, bin, title);

    return found_ball;
}

void find_middle(vector<cv::KeyPoint> &kps)
{   
    cv::KeyPoint kp(0,0,0);
    for (int i=0; i < kps.size(); i++)
    {
        kp.pt.x += kps[i].pt.x;
        kp.pt.y += kps[i].pt.y;
        if (kps[i].size > kp.size)
            kp.size = kps[i].size;
    }

    kp.pt.x /= kps.size();
    kp.pt.y /= kps.size();

    vector<cv::KeyPoint> new_vec;
    new_vec.push_back(kp);
    kps = new_vec;
}

void track_ball(CamData &cam, int i)
{
    cv::Mat img_kps;
    cv::drawKeypoints(cam.imgs[i], cam.keypoints[i], img_kps, 
        cv::Scalar(0,0,255), cv::DrawMatchesFlags::DRAW_RICH_KEYPOINTS );

    display_img(cam, img_kps, cam.name);
}

void display_img(CamData &cam, cv::Mat img, string title)
{
    cv::Mat enlarged;
    cv::resize(img, enlarged, cv::Size(img.cols*2.5, img.rows*2.5), cv::INTER_NEAREST);
    cv::imshow(title, enlarged);
}

const cv::SimpleBlobDetector::Params set_params()
{
    cv::SimpleBlobDetector::Params params;
    params.minThreshold = 100;
    params.maxThreshold = 255;
    params.filterByColor = true;
    params.blobColor = 255;

    return params;
}

void create_windows(CamData &camL, CamData &camR)
{
    cv::namedWindow(camL.name);
    cv::namedWindow(camR.name);
    string binL = "Binary " + camL.name;
    string binR = "Binary " + camR.name;
    cv::namedWindow(binL);
    cv::namedWindow(binR);

    int x1(100), x2(610), y2(575);
    cv::moveWindow(camL.name, x1, 0);
    cv::moveWindow(camR.name, x2, 0);
    cv::moveWindow(binL, x1,y2);
    cv::moveWindow(binR, x2,y2);
}