#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
using namespace cv;

vector<Mat> process_frames(int skip_frames, int pyramid_level);
void record_video(vector<Mat> vid1, vector<Mat> vid2, string filename); 

int main()
{
  std::vector<cv::Mat> vid1, vid2, vid3, vid4;
  vid1 = process_frames(1, 0);
  vid2 = process_frames(10, 0);
  vid3 = process_frames(1, 3);
  vid4 = process_frames(10, 3);
  record_video(vid1, vid2, "../videos/task1_0pyrlevel.avi");
  record_video(vid3, vid4, "../videos/task1_3pyrlevel.avi");
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

vector<Mat> process_frames(int skip_frames, int pyramid_level)
{
  VideoCapture cap("/home/seth/school/robotic_vision/5/MotionFieldVideo.mp4");
  vector<Mat> vid;
  Size winSize(31, 31);

  TermCriteria crit{TermCriteria::COUNT + TermCriteria::EPS, 40, 0.001};
  int MAX_CORNERS(500);
  double QUALITY(0.01), MIN_DIST(10.0), MIN_EIG(0.01);

  vector<Point2f> corners;
  vector<Point2f> prev_corners;

  int frame_num = 0;
  cout << "-- Auto sequence start..." << endl;
  while (true)
  {
    Mat gray, prev_gray, frame;
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
    goodFeaturesToTrack(prev_gray, prev_corners, MAX_CORNERS, QUALITY, MIN_DIST);

    vector<uchar> status;
    vector<float> err;
    calcOpticalFlowPyrLK(prev_gray, gray, prev_corners, corners, status, err, winSize,
                         pyramid_level, crit, 0, MIN_EIG);

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
    if (frame_num % 5 == 0)
      cout << "Corners: " << counter << "; percentage: " << (double)counter / prev_corners.size() * 100.0 << endl;
    
    // cv::imshow("Optical Flow", frame);
    // char c = (char)waitKey(40);
    // if ( c == 'q' )
    //   break;
    
    frame_num++;
    vid.push_back(frame);
  }
  cap.release();

  return vid;
}