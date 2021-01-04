#include <iostream>
#include <fstream>
using namespace std;

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <Eigen/Geometry> 
#include <boost/format.hpp>  // for formating strings
#include <pcl/point_types.h> 
#include <pcl/io/pcd_io.h> 
#include <pcl/filters/voxel_grid.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/filters/statistical_outlier_removal.h>

#include <pcl/registration/icp.h>


int main( int argc, char** argv )
{
    vector<cv::Mat> colorImgs, depthImgs;    // 彩色图和深度图
    vector<Eigen::Isometry3d> poses;         // 相机位姿
    vector<Eigen::Matrix3d> Rs;
    vector<Eigen::Vector3d> ts;
    
    ifstream fin("./data/pose.txt");
    if (!fin)
    {
        cerr<<"cannot find pose file"<<endl;
        return 1;
    }
    
    for ( int i=0; i<5; i++ )
    {
        boost::format fmt( "./data/%s/%d.%s" ); //图像文件格式
        //colorImgs.push_back( cv::imread( (fmt%"color"%(i+1)%"png").str() ));
        depthImgs.push_back( cv::imread( (fmt%"depth"%(i+1)%"pgm").str(), -1 )); // 使用-1读取原始图像
        
        double data[7] = {0};
        for ( int i=0; i<7; i++ )
        {
            fin>>data[i];
        }

        Eigen::Quaterniond q( data[6], data[3], data[4], data[5] );
        Eigen::Matrix3d R(q);
        Eigen::Vector3d t( data[0], data[1], data[2] );
        Eigen::Isometry3d T(q);
        T.pretranslate(t);
        poses.push_back( T );
        Rs.push_back(R);
        ts.push_back(t);
    }

    cout << "the pose1:" << endl << poses[0].matrix() << endl << poses[0].matrix().inverse()<<endl;
    cout << "the relative pose T12:" << endl << (poses[1].inverse()*poses[2]).matrix() << endl;
    cout << "the relative pose T21:" << endl << poses[2].matrix().inverse()*poses[1].matrix() << endl;

    //cout << "the R12:" << endl << Rs[0].transpose()*Rs[1] << endl;
    //cout << "the t12:" << endl << Rs[0].transpose()*ts[1]-Rs[0].transpose()*ts[0] << endl;
    
    
    // 计算点云并拼接
    // 相机内参 
    double cx = 325.5;
    double cy = 253.5;
    double fx = 518.0;
    double fy = 519.0;
    double depthScale = 1000.0;
    
    cout<<"正在将图像转换为点云..."<<endl;
    
    // 定义点云使用的格式：这里用的是XYZRGB
    typedef pcl::PointXYZ PointT; 
    typedef pcl::PointCloud<PointT> PointCloud;
    
    // 新建一个点云
    double max_z=0,min_z=0;
    PointCloud::Ptr pointCloud( new PointCloud );
    PointCloud::Ptr pointCloud_target( new PointCloud );
    vector< PointCloud::Ptr > frame_cloud;
     vector< PointCloud::Ptr > frame_cloud_filter;
    for ( int i=0; i<5; i++ )
    {
        PointCloud::Ptr current( new PointCloud );
        cout<<"转换图像中: "<<i+1<<endl; 
        //cv::Mat color = colorImgs[i]; 
        cv::Mat depth = depthImgs[i];
        Eigen::Isometry3d T = poses[i];
        for ( int v=0; v<depth.rows; v++ )
            for ( int u=0; u<depth.cols; u++ )
            {
                unsigned int d = depth.ptr<unsigned short> ( v )[u]; // 深度值
                if ( d < 1000 ) continue; // 为0表示没有测量到
                if ( d >= 7000 ) continue; // 深度太大时不稳定，去掉
                Eigen::Vector3d point; 
                point[2] = double(d)/depthScale; 
                point[0] = (u-cx)*point[2]/fx;
                point[1] = (v-cy)*point[2]/fy; 
                Eigen::Vector3d pointWorld = point;
                

                if(i==0)
                {
                    Eigen::Vector3d pointWorld1 = poses[1].inverse()*poses[2]*point;
                    PointT p1 ;
                    p1.x = pointWorld1[0];
                    p1.y = pointWorld1[1];
                    p1.z = pointWorld1[2];
                    pointCloud_target->points.push_back(p1);
                }
               
                PointT p ;
                p.x = pointWorld[0];
                p.y = pointWorld[1];
                p.z = pointWorld[2];
                //p.b = (i+1)*30;
                //p.g = (i+1)*30;
                //p.r = (i+1)*30;
                current->points.push_back( p );

               
            }
        
        frame_cloud.push_back(current);
        
        // depth filter and statistical removal 
        PointCloud::Ptr tmp ( new PointCloud );
        pcl::StatisticalOutlierRemoval<PointT> statistical_filter;
        statistical_filter.setMeanK(50);
        statistical_filter.setStddevMulThresh(1.0);
        statistical_filter.setInputCloud(current);
        statistical_filter.filter( *tmp );
        frame_cloud_filter.push_back(tmp);
        //(*pointCloud) += *tmp;
    }

  cout << "the number of points of source is:" << (*frame_cloud[2]).size() << endl;
  cout << "the number of points of targent is:" << (*frame_cloud[3]).size() << endl;
  pcl::IterativeClosestPoint<PointT, PointT> icp,icp_filter;
  icp.setInputSource(frame_cloud[0]);
  icp.setInputTarget(pointCloud_target);

  icp_filter.setInputSource(frame_cloud_filter[2]);
  icp_filter.setInputTarget(frame_cloud_filter[3]);
  
  pcl::PointCloud<PointT> Final,Final_filter;
  icp.align(Final);
  icp_filter.align(Final_filter);

  std::cout << "has converged:" << icp.hasConverged() << " score: " <<
  icp.getFitnessScore() << std::endl;
  std::cout << icp.getFinalTransformation() << std::endl;//return Ttarget_source

  std::cout << "filter has converged:" << icp_filter.hasConverged() << " score: " <<
  icp_filter.getFitnessScore() << std::endl;
  std::cout << icp_filter.getFinalTransformation() << std::endl;


   // pointCloud->is_dense = false;
    //cout<<"点云共有"<<pointCloud->size()<<"个点."<<endl;
    
    // voxel filter 
    //pcl::VoxelGrid<PointT> voxel_filter; 
    //voxel_filter.setLeafSize( 0.01, 0.01, 0.01 );       // resolution 
    //PointCloud::Ptr tmp ( new PointCloud );
    //voxel_filter.setInputCloud( pointCloud );
    //voxel_filter.filter( *tmp );
    //tmp->swap( *pointCloud );
    
    //cout<<"滤波之后，点云共有"<<pointCloud->size()<<"个点."<<endl;
    
    //pcl::io::savePCDFileBinary("map.pcd", *pointCloud );
    return 0;
}
