#include <opencv2/opencv.hpp>
#include <string>
#include <vector>

using namespace std;

struct CamData {
    string name;
    cv::Mat img, mtx, dist, R, P;
    vector<cv::Point2f> pts, output_pts;
    vector<cv::Point3f> persp, pts_3d;
};

void chessboard(CamData &cam, string param_file)
{
    cv::Size chess_size(10, 7);
    
    cv::TermCriteria criteria(cv::TermCriteria::EPS + 
                              cv::TermCriteria::MAX_ITER, 30, 0.001);

    cv::Mat gray;
    cv::cvtColor(cam.img, gray, cv::COLOR_BGR2GRAY);
    vector<cv::Point2f> corners;
    int flags(cv::CALIB_CB_ADAPTIVE_THRESH + cv::CALIB_CB_NORMALIZE_IMAGE);
    bool success = cv::findChessboardCorners(gray, chess_size, corners, flags);
    cv::cornerSubPix(gray, corners, cv::Size(5,5), cv::Size(-1,-1), criteria);
    
    cv::FileStorage fin(param_file, cv::FileStorage::READ);
    fin["mtx"] >> cam.mtx;
    fin["dist"] >> cam.dist;
    fin.release();

    vector<cv::Point2f> pts{corners[0], corners[9], corners[60], corners[69]};
    for(int i=0; i < 4; i++) { cam.pts.push_back(pts[i]); }
}

void calc_3dpoints(CamData &cam, CamData cam2, cv::Mat Q)
{
    CamData camL, camR;
    if(cam.name.compare("Left")) {
        camL = cam;
        camR = cam2;
    }
    else {
        camL = cam2;
        camR = cam;
    }
    
    for(int i=0; i < cam.output_pts.size(); i++)
    {
        cv::Point3f pt(cam.output_pts[i].x, cam.output_pts[i].y, 
                       camR.output_pts[i].x - camL.output_pts[i].x);
        cam.persp.push_back(pt);
    }

    cv::perspectiveTransform(cam.persp, cam.pts_3d, Q);

    cout << cam.name << " pts:\n" << cam.pts_3d[0] << endl
                                  << cam.pts_3d[1] << endl
                                  << cam.pts_3d[2] << endl
                                  << cam.pts_3d[3] << "\n\n";
}

void draw_circles(CamData &cam)
{
    for(int i=0; i < cam.pts_3d.size(); i++)
    {
        cv::circle(cam.img, cv::Point2f(cam.pts[i].x, cam.pts[i].y), 
                   5, cv::Scalar(0,0,255), 2, 8);

    }
    string filename = cam.name + "_task1.jpg";
    cv::imwrite(filename, cam.img);
    cv::imshow(cam.name, cam.img);
}

int main() 
{
    CamData camL, camR;
    camL.name = "Left";
    camR.name = "Right";
    camL.img = cv::imread("../../3/my_imgs/stereo/stereoL26.bmp");
    camR.img = cv::imread("../../3/my_imgs/stereo/stereoR26.bmp");
    string param_fileL{"../params/left_cam.yaml"};
    string param_fileR{"../params/right_cam.yaml"};
    
    // Get intrinsic parameters
    chessboard(camL, param_fileL);
    chessboard(camR, param_fileR);
    
    // Get extrinsic parameters
    cv::FileStorage fin("../params/stereo.yaml", cv::FileStorage::READ);
    cv::Mat R, T, E, F;
    fin["R"] >> R;
    fin["E"] >> E;
    fin["T"] >> T;
    fin["F"] >> F;
    fin.release();
    
    // Rectification params
    cv::Mat R1, R2, P1, P2, Q;
    cv::stereoRectify(camL.mtx, camL.dist, camR.mtx, camR.dist, camL.img.size(), 
                      R, T, R1, R2, P1, P2, Q);

    cv::undistortPoints(camL.pts, camL.output_pts, camL.mtx, camL.dist, R1, P1);
    cv::undistortPoints(camR.pts, camR.output_pts, camR.mtx, camR.dist, R2, P2);
    calc_3dpoints(camL, camR, Q);
    calc_3dpoints(camR, camL, Q);

    // Draw and show results
    draw_circles(camL);
    draw_circles(camR);
    cv::waitKey(0);

    return 0;
}