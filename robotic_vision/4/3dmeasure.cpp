#include <opencv2/opencv.hpp>
#include <string>
#include <vector>

using namespace std;

struct CamData {
    cv::Mat img_raw;
    cv::Mat img_gray;
    cv::Mat mtx;
    cv::Mat dist;
    vector<cv::Point2f> pts;
    vector<cv::Point3f> output_pts;
    cv::Mat R;
    cv::Mat P;
    vector<cv::Point3f> persp;
    cv::Mat 
};

void chessboard(CamData &cam, string param_file)
{
    cv::Size chess_size(10, 7);
    
    cv::TermCriteria criteria(cv::TermCriteria::EPS + 
                              cv::TermCriteria::MAX_ITER, 30, 0.001);

    cv::cvtColor(cam.img_raw, cam.img_gray, cv::COLOR_BGR2GRAY);
    vector<cv::Point2f> corners;
    int flags(cv::CALIB_CB_ADAPTIVE_THRESH + cv::CALIB_CB_NORMALIZE_IMAGE);
    bool success = cv::findChessboardCorners(cam.img_gray, chess_size, corners, flags);
    cv::cornerSubPix(cam.img_gray, corners, cv::Size(5,5), cv::Size(-1,-1), criteria);
    
    cv::FileStorage fin(param_file, cv::FileStorage::READ);
    fin["mtx"] >> cam.mtx;
    fin["dist"] >> cam.dist;
    fin.release();

    vector<cv::Point2f> pts{corners[0], corners[9], corners[69], corners[60]};
    for(int i=0; i < 4; i++) 
    {
        cam.pts.push_back(pts[i]);
    }
}

void undistort(CamData &cam, CamData cam2, cv::Mat Q)
{
    cv::undistortPoints(cam.pts, cam.output_pts, cam.mtx, cam.dist, cam.R, cam.P);

    for(int i=0; i < cam.output_pts.size(); i++)
    {
        cv::Point3f pt(cam.output_pts[i].x, cam.output_pts[i].y, 
                       cam.output_pts[i].x - cam2.output_pts[i].x);
        cam.persp.push_back(pt);
    }

    cv::perspectiveTransform(cam.persp, )
}

int main() 
{
    CamData camL, camR;
    camL.img_raw = cv::imread("../3/my_imgs/stereo/stereoL26.bmp");
    camR.img_raw = cv::imread("../3/my_imgs/stereo/stereoR26.bmp");
    string param_fileL{"./left_cam.yaml"};
    string param_fileR{"./right_cam.yaml"};
    
    // Get intrinsic parameters
    chessboard(camL, param_fileL);
    chessboard(camR, param_fileR);
    
    // Get extrinsic parameters
    cv::FileStorage fin("stereo.yaml", cv::FileStorage::READ);
    cv::Mat R, T, E, F;
    fin["R"] >> R;
    fin["E"] >> E;
    fin["T"] >> T;
    fin["F"] >> F;
    fin.release();
    
    // Rectification params
    cv::Mat Q;
    cv::stereoRectify(camL.mtx, camL.dist, camR.mtx, camR.dist, camL.img_raw.size(), 
                      R, T, camL.R, camR.R, camL.P, camR.P, Q);

    undistort(camL, camR, Q);
    undistort(camR, camL, Q);


    return 0;
}