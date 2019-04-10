#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;
using namespace std;

class Task3
{
public:

    py::array run(bool display) 
    {
        cv::FileStorage fin("../params/cam_params.yaml", cv::FileStorage::READ);
        cv::Mat M, dist;
        fin["mtx"] >> M;
        fin["dist"] >> dist;
        fin.release();

        double f( M.at<double>(0,0) );
        double w(59.0);

        string path("../imgs/T");
        cv::Mat img, original_img, prev_img, result, prev_result, gray, orig_gray;

        if (display)
        {
            cv::namedWindow("original");
            cv::namedWindow("image");
            cv::moveWindow("original", 800, 20);
        }
        
        cv::Rect roi{cv::Point2f{50, 182}, cv::Point2f{600, 342}};
        int end = 19;
        vector<double> z_vec(18,0);
        for (int i=1; i < end; i++)
        {
            img = cv::imread(path + to_string(i) + ".jpg");
            cv::cvtColor(img, gray, cv::COLOR_BGR2GRAY);
            gray = gray(roi);

            cv::Canny(gray, gray, 100, 165, 3);

            double min_x(640), max_x(0);
            cv::Point min, max;
            for (int i=0; i < gray.rows-1; i++)
            {
                cv::Rect roi2(0, i, gray.cols, 1);
                double mi, ma;
                cv::Mat temp( gray(roi2) );
                cv::minMaxLoc(temp, &mi, &ma, &min, &max);
                if (ma == 255 && max.x < min_x)
                    min_x = max.x;
                if (ma == 255 && max.x > max_x)
                    max_x = max.x;
            }

            z_vec[i] = f * w / (max_x - min_x);

            img.copyTo(result);
            result = result(roi);
            cv::circle(result, cv::Point2f(min_x, 50), 3, cv::Scalar(0, 0, 255), -1);
            cv::circle(result, cv::Point2f(max_x, 50), 3, cv::Scalar(0, 0, 255), -1);
            
            if (display)
            {
                cv::imshow("image", result);
                cv::imshow("original", gray);
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
        return py::array(z_vec.size(), z_vec.data());
    }
};

PYBIND11_MODULE(task3_py, m) {
    py::class_<Task3>(m, "Task3")
        .def(py::init<>())
        .def("run", &Task3::run);
}
