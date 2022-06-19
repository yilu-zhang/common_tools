#include "opencv2/opencv.hpp"
#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char ** argv)
{
	//Mat img0 = imread("1912392039.JPG");
        string img_name = "13.jpg";
        string img_out_name = "3_t_p.png";
	Mat img = imread(img_name);

	if(img.empty())
	{
		cout<<"read error"<<endl;
		return -1;
	}

	//namedWindow("read img",0);
	//imshow("read img",img);

	cout<<(int)img.at<Vec3b>(72,184)[0]<<" "<<(int)img.at<Vec3b>(72,184)[1]<< " "<<(int)img.at<Vec3b>(72,184)[2]<<endl;
	for(int row=0;row<img.rows;row++)
	{
		for(int col=0;col<img.cols;col++)
		{

			//if(img.at<Vec3b>(row,col)[0]>220 && img.at<Vec3b>(row,col)[1] < 180  && img.at<Vec3b>(row,col)[2] < 100)
			if(img.at<Vec3b>(row,col)[0] > 100 && img.at<Vec3b>(row,col)[1] > 100  && img.at<Vec3b>(row,col)[2] > 100)
			{ 
				img.at<Vec3b>(row,col)[0]=255;
				img.at<Vec3b>(row,col)[1]=255;
				img.at<Vec3b>(row,col)[2]=255;
			}
                        //if(row < 100 && img.at<Vec3b>(row,col)[0] > 50 && img.at<Vec3b>(row,col)[0] != 255)
			//{
			//	img.at<Vec3b>(row,col)[0]=11;
			//	img.at<Vec3b>(row,col)[1]=5;
			//	img.at<Vec3b>(row,col)[2]=6;
			//}
		}
	}
        Mat kernel = getStructuringElement(MORPH_RECT, Size(8, 8), Point(-1, -1));
	morphologyEx(img, img, MORPH_OPEN, kernel);
        for(int row=0;row<img.rows;row++)
	{
		for(int col=0;col<img.cols;col++)
		{

			//if(img.at<Vec3b>(row,col)[0]>220 && img.at<Vec3b>(row,col)[1] < 180  && img.at<Vec3b>(row,col)[2] < 100)
			if(img.at<Vec3b>(row,col)[0] < 200 && img.at<Vec3b>(row,col)[1] < 200  && img.at<Vec3b>(row,col)[2] < 200)
			{
				img.at<Vec3b>(row,col)[0]=0;
				img.at<Vec3b>(row,col)[1]=0;
				img.at<Vec3b>(row,col)[2]=0;
			}
                        //if(row < 100 && img.at<Vec3b>(row,col)[0] > 50 && img.at<Vec3b>(row,col)[0] != 255)
			//{
			//	img.at<Vec3b>(row,col)[0]=11;
			//	img.at<Vec3b>(row,col)[1]=5;
			//	img.at<Vec3b>(row,col)[2]=6;
			//}
		}
	}
	imwrite(img_out_name,img);
	waitKey(0);
	return 0;
}
