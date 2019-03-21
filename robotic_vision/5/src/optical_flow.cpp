#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
using namespace cv;


int main(int argc, char **argv)
{

  int skip_frames = 0;
  if ( argc > 1)
    skip_frames = stoi(argv[1]);
  else
    skip_frames = 10;
    
  VideoCapture cap("/home/seth/school/robotic_vision/5/MotionFieldVideo.mp4");
  Size subPixWinSize(10, 10), winSize(21, 21);

  TermCriteria crit{TermCriteria::COUNT + TermCriteria::EPS, 40, 0.001};
  int MAX_CORNERS = 500;
  double quality(0.01), min_dist(10.0), min_eig(0.02);

  vector<Point2f> corners;
  vector<Point2f> prev_corners;

  namedWindow("prev_gray", WINDOW_NORMAL | WINDOW_KEEPRATIO | WINDOW_GUI_EXPANDED);
  namedWindow("gray", WINDOW_NORMAL | WINDOW_KEEPRATIO | WINDOW_GUI_EXPANDED);
  
  Mat gray, prev_gray, frame;
  int frame_num = 0;
  cout << "-- Beginning launch sequence..." << endl;
  while (true)
  {
    if ( frame.empty() )
    {
      cap >> frame;
      cvtColor(frame, prev_gray, COLOR_BGR2GRAY);
    }
      
    for (int i=0; i < skip_frames; i++)
      cap >> frame;
    if (frame.empty())
    {
      cout << "-- Main engine cutoff"; 
      break;
    }

    if ( !gray.empty() )
      gray.copyTo(prev_gray);
    cvtColor(frame, gray, COLOR_BGR2GRAY);
    goodFeaturesToTrack(prev_gray, prev_corners, MAX_CORNERS, quality, min_dist);
    // cornerSubPix(prev_gray, prev_corners, subPixWinSize, Size(-1, -1), crit);

    vector<uchar> status;
    vector<float> err;
    cv::imshow("prev_gray", prev_gray);
    cv::imshow("gray", gray);
    waitKey(1);
    calcOpticalFlowPyrLK(prev_gray, gray, prev_corners, corners, status, err, winSize,
                         0, crit, 0, min_eig);

    int counter(0);
    for (int i=0; i < prev_corners.size(); i++)
    {
      // if ( !status[i] )
      //   continue;
      if ( status[i] && err[1] < 20 )
      {
        circle(frame, prev_corners[i], 3, Scalar(0,255,0), -1);
        line(frame, prev_corners[i], corners[i], Scalar(0,0,255), 1);
        counter++;
      }
    }
    
    cv::imshow("Optical Flow", frame);
    char c = (char)waitKey(1);
    if ( c == 'q' )
      break;
  }
  cap.release();

  return 0;
}