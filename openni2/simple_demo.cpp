#include <iostream>
#include "OpenNI.h"
/*#include "OniPlatform.h"
#include "OniProperties.h"
#include "OniEnums.h"

#include "OniCAPI.h"
#include "OniCProperties.h"
#include "OniCTypes.h"*/

using namespace openni;

int main(int argc, char** argv)
{
    // 初始化OpenNI环境
    openni::OpenNI::initialize();
    printf("init success!\n");

    // 声明并打开Device设备，我用的是Kinect。
    openni::Device devAnyDevice;
    if (devAnyDevice.open( openni::ANY_DEVICE )!= STATUS_OK)
    {
	printf("open fail\n");
        return -1;
    }
    printf("open success!\n");

    // 创建并打开深度数据流
    openni::VideoStream streamDepth;
    streamDepth.create( devAnyDevice, openni::SENSOR_DEPTH );
    streamDepth.start();
    printf("start depth success!\n");

    // 同样的创建并打开彩色图像数据流
    openni::VideoStream streamColor;
    if(streamColor.create( devAnyDevice, openni::SENSOR_COLOR )!=STATUS_OK)
    {
        printf("create color fail!\n");
    }
    streamColor.start();
    printf("start color success!\n");

    // 循环读取数据流信息并保存在VideoFrameRef中
    openni::VideoFrameRef frameDepth;
    openni::VideoFrameRef frameColor;
    for( int i = 0; i < 1000; ++ i )
    {
        // 读取数据流
	printf("readframe success!\n");
        streamDepth.readFrame( &frameDepth );
	printf("readframe success!\n");
        //streamColor.readFrame( &frameColor );
	printf("readframe success!\n");

        // 获取data array
        const openni::DepthPixel* pDepth
            = (const openni::DepthPixel*)frameDepth.getData();
        const openni::RGB888Pixel* pColor
            = (const openni::RGB888Pixel*)frameColor.getData();

        // 显示深度信息和对应的彩色R、G、B数值
        int idx = frameDepth.getWidth() * ( frameDepth.getHeight() + 1 ) / 2;
        std::cout  << pDepth[idx]  << "( "
            << (int)pColor[idx].r << ","
            << (int)pColor[idx].g << ","
            << (int)pColor[idx].b << ")"
            << std::endl;
    }

    // 关闭数据流
    streamDepth.destroy();
    streamColor.destroy();

    // 关闭设备
    devAnyDevice.close();

    // 最后关闭OpenNI
    openni::OpenNI::shutdown();

    return 0;
}
