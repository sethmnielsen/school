#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
using namespace cv;

Point2f point_corrected(Point2f pt, int w, Mat img);
void motion_field();
void display_img(Mat img);

int main()
{
  motion_field();
  return 0;
}

void motion_field()
{
  VideoCapture cap("/home/seth/school/robotic_vision/6/imgs/TurnCube1%0d.jpg");
  int m = cv::CAP_PROP_FRAME_COUNT;
  
  int w(5);
  int ws = w*11;
  Size templateSize(w,w), searchSize(ws,ws);
  int match_method = cv::TM_SQDIFF_NORMED;

  int MAX_CORNERS(500);
  double QUALITY(0.01), MIN_DIST(25.0);
  
  vector<Point2f> new_corners, prev_corners, orig_corners, temp;
  vector<uchar> mask;

  Mat F, H1, H2; // fundamental matrix, homography matrices

  cout << "-- Auto sequence start..." << endl;
  Mat frame, gray, prev_gray;
  cap >> frame;
  cvtColor(frame, gray, COLOR_BGR2GRAY);
    
  gray.copyTo(prev_gray);
  goodFeaturesToTrack(prev_gray, prev_corners, MAX_CORNERS, QUALITY, MIN_DIST);
  orig_corners = prev_corners;

  for (int i=0; i < orig_corners.size(); i++)
  {
    circle(frame, orig_corners[i], 3, Scalar(0,255,0), -1);
  }

  display_img(frame);

  for (int j=1; j < m; j++)
  {
    cap >> frame;
    if (frame.empty())
      break;

    cvtColor(frame, gray, COLOR_BGR2GRAY);
    
    new_corners.clear();
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
      matchLoc.x = prev_corners[i].x - res_cols/2.0 + minLoc.x;
      matchLoc.y = prev_corners[i].y - res_rows/2.0 + minLoc.y;

      new_corners.push_back(matchLoc);
    }

    F = findFundamentalMat(prev_corners, new_corners, cv::FM_RANSAC, 
                              3, 0.99, mask);

    prev_corners.clear();
    temp.clear();
    for (int i=0; i < mask.size(); i++)
    {
      if (mask[i])
      {
        prev_corners.push_back(new_corners[i]);
        temp.push_back(orig_corners[i]);
      }
    }
    orig_corners = temp;
    gray.copyTo(prev_gray);

    for (int i=0; i < prev_corners.size(); i++)
    {
      circle(frame, orig_corners[i], 3, Scalar(0,255,0), -1);
      line(frame, orig_corners[i], prev_corners[i], Scalar(0,0,255), 1);
    }

    display_img(frame);

    stereoRectifyUncalibrated(orig_corners, prev_corners, F, 
                              Size(frame.cols, frame.rows), H1, H2);
  }

  cap.release();
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

  return Point2f(x, y);
}

void display_img(Mat img)
{
  if (img.empty())
  {
    cout << "Image empty!" << endl;
    return;
  }
  
  cv::imshow("Multi-Frame Tracking", img);
  char c = (char)waitKey(0);
  if ( c == 'q' )
    destroyAllWindows();
    exit(0);
}