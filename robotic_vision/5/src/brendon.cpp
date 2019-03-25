#include <opencv2/opencv.hpp>
#include <opencv2/features2d.hpp>
// #include <opencv2/xfeatures2d.hpp> //I don't have this

#include <iostream>
#include <vector>
#include <queue>

cv::Point2f getPoint(cv::Point2f pt, int side, cv::Mat img)
{
  float x, y;
  if(pt.x > img.cols - side/2.0)
    x = img.cols - side;
  else if(pt.x < side/2.0)
    x = 0;
  else
    x = pt.x- side/2.0;
  if(pt.y > img.rows - side/2.0)
    y = img.rows - side;
  else if(pt.y < side/2.0)
    y = 0;
  else
     y = pt.y - side/2.0;

  return cv::Point2f(x, y);
}

std::vector<cv::Mat> skipFrames(int n_frames)
{
  std::vector<cv::Mat> frames;
  cv::VideoCapture cap("/home/seth/school/robotic_vision/5/MotionFieldVideo.mp4");

  int max_corners(500), side(5);
  int s_side = 11 * side;
  double quality(0.01), min_dist(25.0);
  cv::Size template_size{side, side};
  cv::Size search_size{s_side, s_side};
  int match_method = cv::TM_SQDIFF_NORMED;
  while(true)
  {
    cv::Mat prev_img, img, g_img;
    cap >> img;
    if(img.empty())
      break;
    cv::cvtColor(img, g_img, cv::COLOR_BGR2GRAY);
    g_img.copyTo(prev_img);

    std::vector<cv::Point2f> prev_corners, orig_corners;
    cv::goodFeaturesToTrack(prev_img, prev_corners, max_corners, quality, min_dist);
    orig_corners = prev_corners;
    int counter(0);

    std::vector<cv::Point2f> new_corners;
    for(int i(0); i < n_frames; i++)
    {
      cap >> img;
      if(img.empty())
        break;
      cv::cvtColor(img, g_img, cv::COLOR_BGR2GRAY);

      //creates a template for each pt to search the img
      new_corners.clear();
      for(cv::Point2f pt : prev_corners)
      {
        cv::Point2f pt2 = getPoint(pt, side, img);
        cv::Rect roi{pt2, template_size};
        cv::Mat templ = prev_img(roi);

        cv::Point2f search_pt = getPoint(pt, s_side, img);
        cv::Rect search_roi{search_pt, search_size};
        cv::Mat search_img = g_img(search_roi);

        int result_cols = search_img.cols - templ.cols + 1;
        int result_rows = search_img.rows - templ.rows + 1;
        cv::Mat result;
        result.create(result_rows, result_cols, CV_32FC1);
        cv::matchTemplate(search_img, templ, result, match_method);

        cv::normalize(result, result, 0, 1, cv::NORM_MINMAX, -1, cv::Mat());

        double minVal; double maxVal;
        cv::Point matchLoc, minLoc, maxLoc;
        cv::minMaxLoc( result, &minVal, &maxVal, &minLoc, &maxLoc, cv::Mat());
        matchLoc.x = pt.x - result_cols/2.0 + minLoc.x;
        matchLoc.y = pt.y - result_rows/2.0 + minLoc.y;

        new_corners.push_back(matchLoc);
      }

      cv::Mat status;
      // std::cout << prev_corners.size() << "\t" << new_corners.size() << "\n";
      cv::Mat F = cv::findFundamentalMat(prev_corners, new_corners, cv::FM_RANSAC, 3, 0.99, status);

      //iterate through each pt and determine if the match is good
      prev_corners.clear();
      std::vector<cv::Point2f> temp;
      for(int j(0); j < status.rows; j++)
      {
        if(status.at<uchar>(j,0))
        {
          prev_corners.push_back(new_corners[j]);
          temp.push_back(orig_corners[j]);
        }
      }
      orig_corners = temp;
      std::cout << "\nstatus.rows: " << status.rows << std::endl;
      std::cout << "prev_corners size: " << prev_corners.size() << std::endl;
      std::cout << "orig_corners size: " << orig_corners.size() << std::endl;

      counter++;
      g_img.copyTo(prev_img);
    }

    if(!img.empty())
    {
      for(int i(0); i < prev_corners.size(); i++)
      {
        cv::circle(img, orig_corners[i], 3, cv::Scalar(0, 255, 0), -1);
        cv::line(img, orig_corners[i], prev_corners[i], cv::Scalar(0, 0, 255), 1);
      }
      cv::imshow("MotionField", img);
      char c = (char)cv::waitKey(0);
      if ( c == 'q' )
        break;
    
      frames.push_back(img);
    }
    else
      break;
  }
  cap.release();
  return frames;
}

void makeVideo(std::vector<cv::Mat> v1, std::vector<cv::Mat> v2, std::string filename)
{
  int ex = cv::VideoWriter::fourcc('M', 'P', 'E', 'G');
  cv::Size size(1920, 1080);
  cv::VideoWriter v_out(filename, ex, 20, size, true);

  for(int i(0); i < v1.size(); i++)
    v_out << v1[i];
  for(int i(0); i < v2.size(); i++)
    v_out << v2[i];
  v_out.release();
}

int main()
{
  std::vector<cv::Mat> set1, set2;
//   set1 = skipFrames(1); //number of sequential frames to match images in
  set2 = skipFrames(10);
//   makeVideo(set1, set2, "task3.avi");

  return 0;
}