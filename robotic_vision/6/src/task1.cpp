#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
using namespace cv;

Point2f point_corrected(Point2f pt, int w, Mat img);
void motion_field();
void display_img(Mat img, string title = "Image");

int main()
{
  motion_field();
  return 0;
}

void motion_field()
{
  VideoCapture cap("/home/seth/school/robotic_vision/6/imgs/TurnCube1%0d.jpg");
  int m = cv::CAP_PROP_FRAME_COUNT;
  vector<Mat> imgs(m);
  
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
  imgs.push_back(frame);
    
  gray.copyTo(prev_gray);
  goodFeaturesToTrack(prev_gray, prev_corners, MAX_CORNERS, QUALITY, MIN_DIST);
  orig_corners = prev_corners;

  for (int i=0; i < orig_corners.size(); i++)
  {
    circle(frame, orig_corners[i], 3, Scalar(0,255,0), -1);
  }

  for (int j=1; j < m; j++)
  {
    cap >> frame;
    imgs.push_back(frame);
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

    // display_img(frame);

  }
  cap.release();
  
  F = findFundamentalMat(orig_corners, new_corners, cv::FM_RANSAC, 
                          3, 0.99, mask);

  stereoRectifyUncalibrated(orig_corners, new_corners, F, 
                            Size(frame.cols, frame.rows), H1, H2);

  cv::FileStorage fin("../cam_mat.yaml", cv::FileStorage::READ);
  Mat M, dist;
  fin["mtx"] >> M;
  fin["dist"] >> dist;
  fin.release();

  Mat R1, R2;
  R1 = M.inv()*H1*M;
  R2 = M.inv()*H2*M;

  Size sz(640,480);
  Mat map1_1, map1_2, map2_1, map2_2, rect1, rect2;
  initUndistortRectifyMap(M, dist, R1, M, sz, 5, map1_1, map1_2);
  remap(imgs[0], rect1, map1_1, map1_2, cv::INTER_LINEAR);
  initUndistortRectifyMap(M, dist, R2, M, sz, 5, map2_1, map2_2);
  remap(imgs.back(), rect2, map2_1, map2_2, cv::INTER_LINEAR);

  for (int i{1}; i < 21; i++)
  {
    cv::Point left_pt{0, 25*i};
    cv::Point right_pt{800, 25*i};
    cv::line(rect1,left_pt,right_pt,cv::Scalar(0,0,255),1);
    cv::line(rect2,left_pt,right_pt,cv::Scalar(0,0,255),1);
  }

  display_img(rect1, "Rectified First Frame");
  display_img(rect2, "Rectified Last Frame");
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

void display_img(Mat img, string title)
{
  if (img.empty())
  {
    cout << "Image empty!" << endl;
    return;
  }
  
  cv::imshow(title, img);
  char c = (char)waitKey(0);
  if ( c == 'q' )
  {
    destroyAllWindows();
    exit(0);
  }
}