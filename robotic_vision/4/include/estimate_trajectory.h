#include <opencv2/opencv.hpp>
#include <string>
#include <vector>
#include <iostream>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

namespace py = pybind11;
namespace fs = std::filesystem;
using namespace std;

typedef vector<fs::path> pvec;

class TrajectoryEstimator
{
public:
    struct CamData {
        string name;
        cv::Mat mtx, dist, R, P, Q;
        cv::Rect roi;
        pvec img_files;
        vector<cv::Mat> imgs;
        vector<vector<cv::KeyPoint>> keypoints;
        vector<vector<cv::Point2f>> points;
    };
    
    TrajectoryEstimator() {};
    ~TrajectoryEstimator() {};
    void init(bool display);
    py::array run(int i);
    bool find_ball(CamData &cam, int i);
    void find_middle(vector<cv::KeyPoint> &kps);
    void track_ball(CamData &cam, int i);
    void display_img(CamData &cam, cv::Mat img, string title);
    const cv::SimpleBlobDetector::Params set_params();
    void create_windows();
    void setup_cam(CamData &cam, string param_file);
    vector<double> calc_3dpoints(int i);

private:
    CamData camL, camR;
    cv::Ptr<cv::SimpleBlobDetector> detector;
    bool display_;
};

PYBIND11_MODULE(estimate_trajectory_interface, m) {
    py::class_<TrajectoryEstimator>(m, "TrajectoryEstimator")
        .def(py::init<>())
        .def("init", &TrajectoryEstimator::init)
        .def("run", &TrajectoryEstimator::run);
}