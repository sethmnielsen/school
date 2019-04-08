#include <opencv2/opencv.hpp>
#include <iostream>
#include <string>
#include <vector>
#include <cmath>

using namespace std;

vector<cv::Mat> find_features() 
{
    vector<cv::Mat> features;
    return features;
}

void track_features(vector<cv::Mat> features)
{

}

void predict_impact(vector<cv::Mat> features)
{

}

int main() 
{
    vector<cv::Mat> feats = find_features();
    track_features(feats);
    predict_impact(feats);
    
    return 0;
}