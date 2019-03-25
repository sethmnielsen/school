#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
using namespace cv;

vector<Mat> motion_field(int skip_frames);
void record_video(vector<Mat> vid1, vector<Mat> vid2, string filename); 

int main()
{
  std::vector<cv::Mat> vid1, vid2;
  vid1 = motion_field(1);
  vid2 = motion_field(10);
  record_video(vid1, vid2, "multiframe_task3.avi");
  return 0;
}

void record_video(vector<Mat> vid1, vector<Mat> vid2, string filename)
{
  Size size(1920, 1080);
  VideoWriter vid_out(filename, VideoWriter::fourcc('M', 'P', 'E', 'G'), 20, size, true);

  for (int i=0; i < vid1.size(); i++)
    vid_out << vid1[i];
  for (int i=0; i < vid2.size(); i++)
    vid_out << vid2[i];
  vid_out.release();
}

vector<Mat> motion_field(int skip_frames)
{
  VideoCapture cap("/home/seth/school/robotic_vision/5/MotionFieldVideo.mp4");
  vector<Mat> vid;
  Size winSize(31, 31);

  TermCriteria crit{TermCriteria::COUNT + TermCriteria::EPS, 40, 0.001};
  int MAX_CORNERS(500), PYRAMID_LEVEL(3);
  double quality(0.01), min_dist(10.0), min_eig(0.01);

  vector<Point2f> corners;
  vector<Point2f> prev_corners;

  Mat gray, prev_gray, frame;
  int frame_num = 0;
  cout << "-- Auto sequence start..." << endl;
  while (true)
  {
    if ( frame.empty() )
    {
      cap >> frame;
      cvtColor(frame, prev_gray, COLOR_BGR2GRAY);
    }
      
    for (int i=0; i <= skip_frames; i++)
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

    vector<uchar> status;
    vector<float> err;
    calcOpticalFlowPyrLK(prev_gray, gray, prev_corners, corners, status, err, winSize,
                         PYRAMID_LEVEL, crit, 0, min_eig);

    int counter(0);
    for (int i=0; i < prev_corners.size(); i++)
    {
      if ( status[i] && err[i] < 20 )
      {
        circle(frame, prev_corners[i], 3, Scalar(0,255,0), -1);
        line(frame, prev_corners[i], corners[i], Scalar(0,0,255), 1);
        counter++;
      }
    }
    cout << "Corners: " << counter << "; percentage: " << (double)counter / prev_corners.size() * 100.0 << endl;
    
    cv::imshow("Optical Flow", frame);
    char c = (char)waitKey(40);
    if ( c == 'q' )
      break;
  }
  cap.release();

  return vid;
}