//#include "stdafx.h"
#include <iostream>
#include "OpenNI.h"

// 载入OpenCV头文件
#include "opencv2/opencv.hpp"
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

using namespace std;
using namespace openni;
using namespace cv;

int main( int argc, char** argv )
{
    // 初始化OpenNI环境
    OpenNI::initialize();

    // 声明并打开Device设备，我用的是Kinect。
    Device devAnyDevice;
    if(devAnyDevice.open(ANY_DEVICE ) != STATUS_OK)
    {
	printf("open fail!\n");
	return -1;
    }

    // 创建彩色图像数据流
    VideoStream streamColor;
    if(streamColor.create( devAnyDevice, SENSOR_COLOR )!=STATUS_OK)
    {
	printf("readframe fail!\n");
	return -1;
    }
    
    // 设置彩色图像视频模式
    VideoMode mModeColor;
    mModeColor.setResolution( 640, 480 );
    mModeColor.setFps( 30 );
    mModeColor.setPixelFormat( PIXEL_FORMAT_RGB888 );

    streamColor.setVideoMode( mModeColor);

    // 图像模式注册
    if( devAnyDevice.isImageRegistrationModeSupported(
        IMAGE_REGISTRATION_DEPTH_TO_COLOR ) )
    {
        devAnyDevice.setImageRegistrationMode( IMAGE_REGISTRATION_DEPTH_TO_COLOR );
    }
        
    // 打开图像数据流
    if(streamColor.start()!=STATUS_OK)
    {
	printf("readframe fail!\n");
	return -1;
    }

    // 创建OpenCV图像窗口
    namedWindow( "Color Image",  0);

    // 循环读取数据流信息并保存在VideoFrameRef中
    VideoFrameRef  frameColor;

    while( true )
    {
        // 读取数据流
        if(streamColor.readFrame( &frameColor )!=STATUS_OK)
	{
	   printf("readframe fail!\n");
	   return -1;
	}
        
        // 将彩色图像数据转化成OpenCV格式
        const cv::Mat mImageRGB(frameColor.getHeight(), frameColor.getWidth(), CV_8UC3, (void*)frameColor.getData());
        // 首先将RGB格式转换为BGR格式
        cv::Mat cImageBGR;
        cv::cvtColor( mImageRGB, cImageBGR, CV_RGB2BGR );
        // 然后显示彩色图像
        cv::imshow( "Color Image", cImageBGR );

        // 终止快捷键
        if( cv::waitKey(1) == 'q')
            break;
    }

    // 关闭数据流
    streamColor.destroy();

    // 关闭设备
    devAnyDevice.close();

    // 最后关闭OpenNI
    openni::OpenNI::shutdown();

    return 0;
}
