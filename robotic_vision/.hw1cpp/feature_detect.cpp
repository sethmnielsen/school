#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <iostream>

using namespace cv;
using namespace std;

int main( int argc, char** argv )
{
    VideoCapture video(0);
    Mat frame;
    Mat gscale;
    Mat output_raw;
    Mat output_norm;
    Mat output;
    double thresh = 100;
    double maxValue = 255;

    int blocksize = 2;
    int ksize = 3;
    double k = 0.04;
    int n = 0;
    while (1) {
        video >> frame;
        cvtColor( frame, gscale, COLOR_BGR2GRAY );
        switch (n) {
            case 0:
                threshold(gscale, output, thresh, maxValue, THRESH_BINARY);
                break;
            case 1:
                Canny(gscale, output, 50, 150, 3);
                break;
            case 2:
                // goodFeaturesToTrack(frame, output_raw, 100, 0.01, 5);
                // cornerSubPix(output_raw, output)
                // cornerHarris(gscale, output, blocksize, ksize, k);
                // normalize(output_norm, output_raw);
                // convertScaleAbs( output_norm, output);
                // cout << "hello" << output_norm.size << endl;
                // cout << output.size << endl;
                break;
            case 3:
                cout << 3;
                break;
            case 4:
                cout << 4;
                break;
        }
        imshow("Window", output);
        if (waitKey(30) != -1) {
            n++;
            if (n > 4) n = 0;
        }
    }

    return 0;
}
