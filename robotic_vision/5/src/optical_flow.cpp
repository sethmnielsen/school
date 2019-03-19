#include <opencv2/opencv.hpp>
#include <string>
#include <vector>

using namespace std;
using namespace cv;

Point2f point;
bool addRemovePt = false;

int main(int argc, char** argv, Mat hi)
{
    VideoCapture cap("MotionFieldVideo.mp4");
    TermCriteria termcrit(TermCriteria::COUNT|TermCriteria::EPS,20,0.03);
    Size subPixWinSize(10,10), winSize(31,31);
    
    int MAX_FEATURES = 500;
    bool init = false;

    namedWindow( "LK Optical Flow", 1 );
    vector<Point2f> points[2];    
    
    Mat gray, prev_gray, img, frame;   

    for(;;)
    {
        cap >> frame;
        if ( frame.empty() )
            break;
        
        frame.copyTo(img);
        cvtColor(img, gray, COLOR_BGR2GRAY);

        if ( init )
        {
            goodFeaturesToTrack( gray, points[1], MAX_FEATURES, 0.01, 10, Mat(), 3, 0, 0.04 );
            cornerSubPix(gray, points[1], subPixWinSize, Size(-1,-1), termcrit);
            
        }
        
    }
    
    return 0;
}