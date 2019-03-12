#include <opencv2/opencv.hpp>
#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;
using namespace std;

struct CamData {
    string name;
    cv::Mat img, bg, mtx, dist, R, P;
    vector<cv::Point2f> pts, output_pts;
    vector<cv::Point3f> persp, pts_3d;
    cv::Rect roi;
};

bool get_roi(CamData &cam)
{
    cv::cvtColor(cam.img, cam.bg, cv::COLOR_BGR2GRAY);

    int w(100);
    cam.roi = cv::Rect(325, 50, w, w);
    bool found_ball(false);
    return found_ball;
}

int main()
{   
    CamData camL, camR;
    camL.name = "Left";
    camR.name = "Right";
    camL.img = cv::imread("../bb_imgs/1/PL00.bmp");
    camR.img = cv::imread("../bb_imgs/1/PR00.bmp");

    // string path = "/path/to/directory";
    // for (const auto & entry : filesystem::directory_iterator(path))
    //     std::cout << entry.path() << std::endl;
    typedef vector<fs::path> pvec;
    pvec files;

    fs::path p("../bb_imgs/1");
    copy(fs::directory_iterator(p), fs::directory_iterator(), back_inserter(files));
    sort(files.begin(), files.end());
    pvec imgsL(files.begin(), files.begin() + (files.size()/2));
    pvec imgsR(files.begin() + (files.size()/2), files.end());


    for (pvec::const_iterator f(imgsL.begin()); f != imgsL.end(); f++)
    {
        cout << "Left: " << *f << '\n';
        // get_roi()
    }

    for (pvec::const_iterator f(imgsR.begin()); f != imgsR.end(); f++)
    {
        cout << "Right: " << *f << '\n';
        // get_roi()
    }

    return 0;
}