#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main( int argc, char** argv )
{
    VideoCapture video(0);
    if (video.isOpened()) {
        cout << "opened camera" << endl;
    }
    Mat frame;
    while (1) {
        video >> frame;
        imshow("Window", frame);
        waitKey(1);
    }
    return 0;
}
