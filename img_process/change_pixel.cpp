#include "opencv2/opencv.hpp"
#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char ** argv)
{
	Mat img0 = imread("1.jpg");
	Mat img = imread("2.jpg");

	if(img.empty())
	{
		cout<<"read error"<<endl;
		return -1;
	}

	namedWindow("read img",0);
	imshow("read img",img);

	//cout<<img.at<Vec3b>(0,0)[0]<<" "img.at<Vec3b>(0,0)[1]<< " "<<img.at<Vec3b>(0,0)[2]<<endl;
	for(int row=0;row<img.rows;row++)
	{
		for(int col=0;col<img.cols;col++)
		{

			if(img.at<Vec3b>(row,col)[0]>20)
			{
				img.at<Vec3b>(row,col)[0]=img0.at<Vec3b>(0,0)[0];
				img.at<Vec3b>(row,col)[1]=img0.at<Vec3b>(0,0)[1];
				img.at<Vec3b>(row,col)[2]=img0.at<Vec3b>(0,0)[2];
			}
			else
			{
				img.at<Vec3b>(row,col)[0]=255;
				img.at<Vec3b>(row,col)[1]=255;
				img.at<Vec3b>(row,col)[2]=255;
			}
		}
	}
	imwrite("3.jpg",img);
	waitKey(0);
	return 0;
}
