#include <iostream>
#include <fstream>
using namespace std;
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <Eigen/Geometry> 
#include <boost/format.hpp>  // for formating strings
#include <pcl/point_types.h> 
#include <pcl/io/pcd_io.h> 
#include <pcl/visualization/pcl_visualizer.h>
#include <math.h>
#include <algorithm>

using namespace std;
using namespace cv;

#define PI_PER_D 0.017453292
int main( int argc, char** argv )
{
    vector<cv::Mat> colorImgs, depthImgs;    // 彩色图和深度图
    vector<Eigen::Isometry3d, Eigen::aligned_allocator<Eigen::Isometry3d>> poses;         // 相机位姿

    ifstream T_bc("./config.txt");
    if (!T_bc)
    {
        cerr<<"请在有config.txt的目录下运行此程序"<<endl;
        return 1;
    }

    double T_bc_data[15] = {0};
        for ( auto& d:T_bc_data )
            T_bc>>d;

    Eigen::Vector3d t_bc(T_bc_data[0],T_bc_data[1],T_bc_data[2]);
    double theta=T_bc_data[3]*PI_PER_D;
    //cout<<sin(theta)<<endl;
    Eigen::Quaterniond q_bc(cos(theta/2),sin(theta/2),0,0);
    
    ifstream fin("./pose.txt");
    if (!fin)
    {
        cerr<<"请在有pose.txt的目录下运行此程序"<<endl;
        return 1;
    }
    
    for ( int i=0; i<8; i++ )
    {
        boost::format fmt( "./%s/%d.%s" ); //图像文件格式
        //colorImgs.push_back( cv::imread( (fmt%"color"%(i+1)%"png").str() ));
        depthImgs.push_back( cv::imread( (fmt%"depth"%(i+1)%"png").str(), -1 )); // 使用-1读取原始图像
        
        double data[4] = {0};
        for ( auto& d:data )
            fin>>d;
        Eigen::Quaterniond q( cos(data[3]/2*PI_PER_D), 0.0, sin(data[3]/2*PI_PER_D), 0.0);
        //Eigen::Matrix3d R_wbk(q*q_bc);
        Eigen::Vector3d t_wc = q*t_bc;
        //Eigen::Vector3d t_wo2 = R_wbk*t_bo;
        Eigen::Isometry3d T(q*q_bc);
        //T.pretranslate( Eigen::Vector3d( data[0], data[1], data[2] ));
        T.pretranslate(t_wc);
        poses.push_back( T );
        //cout<<"T:"<<endl;
        //cout<<R_wbk<<endl;
        //cout<<t_wo<<endl;
        //cout<<t_wo2<<endl;
    }
    
    // 计算点云并拼接
    // 相机内参 
    double cx = T_bc_data[5];
    double cy = T_bc_data[6];
    double fx = T_bc_data[7];
    double fy = T_bc_data[8];
    double depthScale = T_bc_data[9];
    
    cout<<"正在将图像转换为点云..."<<endl;
    
    // 定义点云使用的格式：这里用的是XYZRGB
    typedef pcl::PointXYZRGB PointT; 
    typedef pcl::PointCloud<PointT> PointCloud;
    
    // 新建一个点云
    PointCloud::Ptr pointCloud( new PointCloud ); 
    PointCloud::Ptr pointCloud_i( new PointCloud ); 
    PointCloud::Ptr pointCloud_layer_1( new PointCloud );

    // cout << T_bc_data[13] <<" " <<T_bc_data[14] << endl;
    double layer1_max_x(-99999),layer1_max_z(-99999),layer1_min_x(99999),layer1_min_z(99999);
    for ( int i=0; i<8; i++ )
    {
        cout<<"转换图像中: "<<i+1<<endl; 
        //cv::Mat color = colorImgs[i]; 
        cv::Mat depth = depthImgs[i];
        Eigen::Isometry3d T = poses[i];
        int j = 0;
        //cout << depth.rows << " " << depth.cols << endl;
        for ( int v=0; v<depth.rows; v++ )
            for ( int u=0; u<depth.cols; u++ )
            {
                unsigned int d = depth.ptr<unsigned short> ( v )[u]; // 深度值
                if ( double(d) < 10 ) continue; // 为0表示没有测量到
                if ( double(d) > 60000 ) continue;
                Eigen::Vector3d point;
                //if(j<100000000 && j%10==0) 
                   // cout<<double(d)<<" ";
                //j++;
                point[2] = double(d)/depthScale; 
                point[0] = (u-cx)*point[2]/fx;
                point[1] = (v-cy)*point[2]/fy; 
                Eigen::Vector3d pointWorld = T*point;
                //Eigen::Vector3d pointWorld = point;
                if(pointWorld[1]<T_bc_data[10] || pointWorld[1]>T_bc_data[11])continue;

               
                if(pointWorld[1]>T_bc_data[13]&&pointWorld[1]<T_bc_data[14])
                {
                    PointT p_layer1 ;
                    p_layer1.x = pointWorld[0];
                    p_layer1.y = pointWorld[1];
                    p_layer1.z = pointWorld[2];
                    pointCloud_layer_1->points.push_back(p_layer1);

                    if(pointWorld[2] > layer1_max_z)
                        layer1_max_z = pointWorld[2];
                    if(pointWorld[2] < layer1_min_z)
                        layer1_min_z = pointWorld[2];
                    if(pointWorld[0] > layer1_max_x)
                        layer1_max_x = pointWorld[0];
                    if(pointWorld[0] < layer1_min_x)
                        layer1_min_x = pointWorld[0];                   
                }




                if(T_bc_data[12]==1)pointWorld[1]=0;
                
                PointT p ;
                p.x = pointWorld[0];
                p.y = pointWorld[1];
                p.z = pointWorld[2];
                //p.b = color.data[ v*color.step+u*color.channels() ];
                //p.g = color.data[ v*color.step+u*color.channels()+1 ];
                //p.r = color.data[ v*color.step+u*color.channels()+2 ];
                if(i%2 == 0)
                {
                    p.b = 90;
                    p.g = 90;
                    p.r = 90;
                }
                else
                {
                    p.b = 240;
                    p.g = 240;
                    p.r = 240;
                }
                pointCloud->points.push_back( p );

                if((i+1) == T_bc_data[4])
                {
                    PointT p_i ;
                    p_i.x = point[0];
                    p_i.y = point[1];
                    p_i.z = point[2];
                    p_i.b = 240;
                    p_i.g = 240;
                    p_i.r = 240;
                    pointCloud_i->points.push_back(p_i);
                }
            }
    }
    
    pointCloud->is_dense = false;
    cout<<"点云共有"<<pointCloud->size()<<"个点."<<endl;
    pcl::io::savePCDFileBinary("map.pcd", *pointCloud );

    if(!pointCloud_i->points.empty())
    {
        pcl::io::savePCDFileBinary("i_map.pcd", *pointCloud_i );
    }

    cv::Mat layer1_img(480, 640, CV_8UC1, 255);
    double detal_x,detal_z,scale_factor_x_1,scale_factor_z_1,scale_factor_1;
    bool ori_flag;
    detal_x = layer1_max_x - layer1_min_x;
    detal_z = layer1_max_z - layer1_min_z;
    if(detal_x > detal_z)
    {
        //scale_factor_x_1 = ;
        //scale_factor_z_1 = (;
        scale_factor_1=min((layer1_img.cols-100)/detal_x,(layer1_img.rows-100)/detal_z);
        ori_flag = true;

    }
    else
    {
        scale_factor_1=min((layer1_img.cols-100)/detal_z,(layer1_img.rows-100)/detal_x);
        ori_flag = false;
    }

    cout<<"点云共有"<<pointCloud_layer_1->size()<<"个点."<<endl;
    cout<<"The scale_factor_1 is:" << scale_factor_1 << endl;
    for(auto& point:pointCloud_layer_1->points)
    {
        int x_axis,z_axis;
        if(ori_flag)
        {
            int i,j;
            for(i=0;i<1;i++)
                for(j=0;j<1;j++)
                    layer1_img.at<uchar>(50+(int)(scale_factor_1*(layer1_max_z-point.z))+i,j+50+(int)(scale_factor_1*(point.x-layer1_min_x)))=0;
        }
        else
        {
            int i,j;
            for(i=0;i<1;i++)
                for(j=0;j<1;j++)
                    layer1_img.at<uchar>(i+50+(int)(scale_factor_1*(layer1_max_x-point.x)),j+50+(int)(scale_factor_1*(layer1_max_z-point.z)))=0;
        }
    }

    imwrite("layer1_1.jpg",layer1_img);


    return 0;
}
