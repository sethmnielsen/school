#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
using namespace cv;

Point2f point_corrected(Point2f pt, int w, Mat img);

int main(int argc, char **argv)
{

  int skip_frames = 0;
  if ( argc > 1)
    skip_frames = stoi(argv[1]);
  else
    skip_frames = 10;
    
  VideoCapture cap("/home/seth/school/robotic_vision/5/MotionFieldVideo.mp4");
  int w(5);
  int ws = w*10;
  Size winSize(21, 21), templateSize(w,w), searchSize(ws,ws);
  int match_method = cv::TM_SQDIFF_NORMED;

  TermCriteria crit{TermCriteria::COUNT + TermCriteria::EPS, 40, 0.001};
  int MAX_CORNERS(500), PYRAMID_LEVEL(2);
  double QUALITY(0.01), MIN_DIST(10.0), MIN_EIG(0.02);

  vector<Point2f> corners;
  vector<Point2f> prev_corners;

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

    // int counter(0);
    for (int i=0; i < prev_corners.size(); i++)
    {
      Point2f pt = point_corrected(prev_corners[i], w, frame);
      Rect templ_roi(pt, templateSize);
      Mat templ = prev_gray(templ_roi);
      Point2f search_pt = point_corrected(prev_corners[i], ws, frame);
      Rect search_roi(search_pt, searchSize);
      Mat search_box = gray(search_roi);

      int res_cols = search_box.cols - templ.cols + 1;
      int res_rows = search_box.rows - templ.rows + 1;
      Mat result;
      result.create(res_rows, res_cols, CV_32FC1);
      matchTemplate(search_box, templ, result, match_method);
      normalize(result, result, 0, 1, cv::NORM_MINMAX, -1, Mat());

      double minVal; double maxVal;
      cv::Point matchLoc, minLoc, maxLoc;
      cv::minMaxLoc( result, &minVal, &maxVal, &minLoc, &maxLoc, cv::Mat());
      matchLoc.x = pt.x - res_cols/2.0 + minLoc.x;
      matchLoc.y = pt.y - res_rows/2.0 + minLoc.y;
      
      circle(frame, prev_corners[i], 3, Scalar(0,255,0), -1);
      line(frame, prev_corners[i], matchLoc, Scalar(0,0,255), 1);
      // counter++;
    }
    // cout << "circles: " << counter << endl;
    
    cv::imshow("Feature Matching", frame);
    char c = (char)waitKey(40);
    if ( c == 'q' )
      break;
  }
  cap.release();

  return 0;
}

Point2f point_corrected(Point2f pt, int w, Mat img)
{
  double x, y;

  if(pt.x > img.cols - w/2.0)
    x = img.cols - w;
  else if(pt.x < w/2.0)
    x = 0;
  else
    x = pt.x- w/2.0;
  if(pt.y > img.rows - w/2.0)
    y = img.rows - w;
  else if(pt.y < w/2.0)
    y = 0;
  else
     y = pt.y - w/2.0;

  return cv::Point2f(x, y);
}