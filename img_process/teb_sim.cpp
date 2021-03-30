#include "opencv2/opencv.hpp"
#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char ** argv)
{
	Mat img0 = imread("/home/yiluzhang/Desktop/experiment/teb/4_8.png",IMREAD_GRAYSCALE);
	Mat img_erode,img_dilate,img_blob;

	if(img0.empty())
	{
		cout<<"read error"<<endl;
		return -1;
	}

	//namedWindow("read img",0);
	//imshow("read img",img0);

	//cout<<img.at<Vec3b>(0,0)[0]<<" "img.at<Vec3b>(0,0)[1]<< " "<<img.at<Vec3b>(0,0)[2]<<endl;
	for(int row=0;row<img0.rows;row++)
	{
		for(int col=0;col<img0.cols;col++)
		{
            if(col < 80 || col> 550 || row < 30 || row > 450 || img0.at<uchar>(row,col)<250)
            {
                img0.at<uchar>(row,col)=0;
                img0.at<uchar>(row,col)=0;
                img0.at<uchar>(row,col)=0;
            }
            else
            {
                img0.at<uchar>(row,col)=255;
                img0.at<uchar>(row,col)=255;
                img0.at<uchar>(row,col)=255;
            }

			/*if(col < 80 || col> 550 || row < 30 || row > 450 || img0.at<Vec3b>(row,col)[0]<250)
			{
				img0.at<Vec3b>(row,col)[0]=0;
				img0.at<Vec3b>(row,col)[1]=0;
				img0.at<Vec3b>(row,col)[2]=0;
			}
			else
			{
				img0.at<Vec3b>(row,col)[0]=255;
				img0.at<Vec3b>(row,col)[1]=255;
				img0.at<Vec3b>(row,col)[2]=255;
			}*/
		}
	}
	imwrite("/home/yiluzhang/Desktop/experiment/teb/4_8_process.png",img0);

    Mat element_erode = getStructuringElement(MORPH_RECT, Size(10, 10));
    erode(img0,img_erode,element_erode);
    imwrite("/home/yiluzhang/Desktop/experiment/teb/4_8_erode.png",img_erode);

    Mat element_dilate = getStructuringElement(MORPH_RECT, Size(15, 15));
    dilate(img_erode,img_dilate,element_dilate);
    imwrite("/home/yiluzhang/Desktop/experiment/teb/4_8_dilate.png",img_dilate);

    /*Ptr<SimpleBlobDetector> detector = SimpleBlobDetector::create();
    vector<KeyPoint> keypoints;
    cout << "keypoints size: " << keypoints.size() << endl;
    detector->detect(img_erode,keypoints);
    Mat img_with_keypoints;
    drawKeypoints(img_erode,keypoints,img_with_keypoints,Scalar(0,0,255),DrawMatchesFlags::DRAW_RICH_KEYPOINTS);
    imshow("keypoints",img_with_keypoints);
    imwrite("/home/yiluzhang/Desktop/experiment/teb/4_8_blob.png",img_with_keypoints);*/

    Mat image;
    image = img_dilate;
    vector<vector<Point>> contours;
    vector<Vec4i> hierarchy;
    findContours(image,contours,hierarchy,RETR_TREE,CHAIN_APPROX_SIMPLE,Point());
    Mat imageContours=Mat::zeros(image.size(),CV_8UC1);
    Mat Contours=Mat::zeros(image.size(),CV_8UC1);  //绘制
    for(int i=0;i<contours.size();i++)
    {
        //contours[i]代表的是第i个轮廓，contours[i].size()代表的是第i个轮廓上所有的像素点数
        for(int j=0;j<contours[i].size();j++)
        {
            //绘制出contours向量内所有的像素点
            Point P=Point(contours[i][j].x,contours[i][j].y);
            Contours.at<uchar>(P)=255;
        }

        //输出hierarchy向量内容
        char ch[256];
        sprintf(ch,"%d",i);
        string str=ch;
        //cout<<"向量hierarchy的第" <<str<<" 个元素内容为："<<endl<<hierarchy[i]<<endl<<endl;

        //绘制轮廓
        drawContours(imageContours,contours,i,Scalar(255),1,8,hierarchy);
    }

    /// Get the moments 图像矩
    vector<Moments> mu(contours.size());
    //求取每个轮廓的矩
    for (int i = 0; i < contours.size(); i++)
    {
        mu[i] = moments(contours[i], false);
    }

    ///  Get the centroid of figures. 轮廓质点
    vector<Point2f> mc(contours.size());
    for (int i = 0; i < contours.size(); i++)
    {
        mc[i] = Point2f(mu[i].m10 / mu[i].m00, mu[i].m01 / mu[i].m00);
    }

    /// Draw contours
    //画轮廓
    //Mat drawing(canny_output.size(), CV_8UC3, Scalar(255, 255, 255));

    for (int i = 0; i < contours.size(); i++)
    {
        Scalar color = Scalar(255, 255, 255);
        //画轮廓
        //drawContours(drawing, contours, i, color, 2, 8, hierarchy, 0, Point());
        //画质心
        circle(imageContours, mc[i], 2, color, -1, 7, 0);
        cout << i << ": " << mc[i].x <<" " << mc[i].y << endl;
    }
    cout << "width: " << imageContours.cols << " height:" << imageContours.rows << endl;

    double scale = sqrt(pow(mc[3].x-mc[4].x,2)+pow(mc[3].y-mc[4].y,2)) / 0.54;
    for (int i = 0; i < contours.size(); i++)
    {
        for(int j=i+1; j< contours.size();j++){
            cout << i << j << " : " << sqrt(pow(mc[i].x-mc[j].x,2)+pow(mc[i].y-mc[j].y,2)) / scale <<endl;
        }
    }

    for (int i = 0; i < contours.size(); i++)
    {
        cout << i << 6 << " : " << sqrt(pow(mc[i].x-245,2)+pow(mc[i].y-410,2)) / scale <<endl;
    }


    //imshow("Contours Image",imageContours); //轮廓
    //imshow("Point of Contours",Contours);   //向量contours内保存的所有轮廓点集
    imwrite("/home/yiluzhang/Desktop/experiment/teb/4_8_blob.png",imageContours);

	waitKey(0);
	return 0;
}
