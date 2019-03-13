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
    cv::Mat mtx, dist, R, P;
    cv::Rect roi;
    pvec img_files;
    vector<cv::Mat> imgs;
    vector<vector<cv::KeyPoint>> keypoints;
    vector<vector<cv::Point2f>> points;
};

bool find_ball(CamData &cam, cv::Ptr<cv::SimpleBlobDetector> &detector, int i);
void find_middle(vector<cv::KeyPoint> &kps);
void track_ball(CamData &cam, int i);
void display_img(CamData &cam, cv::Mat img, string title);
const cv::SimpleBlobDetector::Params set_params();
void create_windows(CamData &camL, CamData &camR);
void setup_cam(CamData &cam, string param_file);
void calc_3dpoints(CamData &camL, CamData camR, cv::Mat Q, int i);

int main(int argc, char** argv)
{   
    CamData camL, camR;
    camL.name = "Left";
    camR.name = "Right";

    create_windows(camL, camR);
    
    pvec files;
    string n = "2";
    if (argc > 1) { n = argv[1]; }
    string prefix = "/home/seth/school/robotic_vision/4/";
    string dir = prefix + "bb_imgs/" + n;
    fs::path p(dir);
    copy(fs::directory_iterator(p), fs::directory_iterator(), back_inserter(files));
    sort(files.begin(), files.end());
    camL.img_files = pvec(files.begin(), files.begin() + (files.size()/2));
    camR.img_files = pvec(files.begin() + (files.size()/2), files.end());

    int w(200);
    camL.roi = cv::Rect(350, 50, w, w);
    camR.roi = cv::Rect(100, 50, w, w);

    const cv::SimpleBlobDetector::Params params = set_params();
    cv::Ptr<cv::SimpleBlobDetector> detector = cv::SimpleBlobDetector::create(params);

    // Get intrinsics
    setup_cam(camL, prefix + "params/left_cam.yaml");
    setup_cam(camR, prefix + "params/right_cam.yaml");
    // Get extrinsic parameters
    cv::FileStorage fin(prefix + "params/stereo.yaml", cv::FileStorage::READ);
    cv::Mat R, T, E, F;
    fin["R"] >> R;
    fin["E"] >> E;
    fin["T"] >> T;
    fin["F"] >> F;
    fin.release();

    // Rectification params
    cv::Mat R1, R2, P1, P2, Q;
    cv::stereoRectify(camL.mtx, camL.dist, camR.mtx, camR.dist, cv::Size(w,w), 
                      R, T, camL.R, camR.R, camL.P, camR.P, Q);

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
            calc_3dpoints(camL, camR, Q, i);
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

void setup_cam(CamData &cam, string param_file)
{
    cv::FileStorage fin(param_file, cv::FileStorage::READ);
    fin["mtx"] >> cam.mtx;
    fin["dist"] >> cam.dist;
    fin.release();
}

bool find_ball(CamData &cam, cv::Ptr<cv::SimpleBlobDetector> &detector, int i)
{
    bool found_ball(false);

    vector<cv::KeyPoint> kps;
    vector<cv::Point2f> pts;

    cv::Mat img, gray, enlarged;
    img = cv::imread(string(cam.img_files[i]));
    img = img(cam.roi);
    cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);
    cam.imgs.push_back(gray);
    if (i == 0)
    {
        cam.keypoints.push_back(kps);
        cam.points.push_back(pts);
        return false;
    }

    cv::Mat bin;
    cv::absdiff(cam.imgs[0], gray, bin);
    cv::threshold(bin, bin, 20, 255, 0);
    cv::Mat element = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(7,7));
    cv::erode(bin, bin, element);
    cv::dilate(bin, bin, element);

    detector->detect(bin, kps);

    if (kps.size()) 
    { 
        found_ball = true; 
        if (kps.size() > 1) { find_middle(kps); }
        cv::Point2f pt(kps[0].pt.x, kps[0].pt.y);
        pt.x += cam.roi.x;
        pt.y += cam.roi.y;
        pts.push_back(pt);
    }

    cam.keypoints.push_back(kps);
    cam.points.push_back(pts);
    
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
    // Undistort
    cv::undistortPoints(cam.points[i], cam.points[i], 
                             cam.mtx, cam.dist, cam.R, cam.P);
    
    cv::Mat img_kps;
    cam.keypoints[i][0].pt = cam.points[i][0];
    cv::drawKeypoints(cam.imgs[i], cam.keypoints[i], img_kps, 
        cv::Scalar(0,0,255), cv::DrawMatchesFlags::DRAW_RICH_KEYPOINTS );
    

    display_img(cam, img_kps, cam.name);
}

void calc_3dpoints(CamData &camL, CamData camR, cv::Mat Q, int i)
{
    vector<cv::Point3f> persp_pts, pts_3d;
    cv::Point3f pt(camL.points[i][0].x, camL.points[i][0].y, 
                    camL.points[i][0].x - camR.points[i][0].x);
    persp_pts.push_back(pt);

    // Get 3d ball location in left camera frame 
    cv::perspectiveTransform(persp_pts, pts_3d, Q);
    pts_3d[0].x -= 10.135;
    pts_3d[0].y -= 29.0;
    pts_3d[0].z -= 21.0;

    cout << i << ":" << pts_3d[0] << "\n";
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

void display_img(CamData &cam, cv::Mat img, string title)
{
    cv::Mat enlarged;
    cv::resize(img, enlarged, cv::Size(img.cols*2.5, img.rows*2.5), cv::INTER_NEAREST);
    cv::imshow(title, enlarged);
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