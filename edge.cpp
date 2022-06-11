#include "stdafx.h"
#include <opencv2/opencv.hpp>
#include <algorithm>
#include <string>
#include <vector>
#include <WINSOCK2.H>  
#include <iostream>  
#include <stdio.h>  
#include <opencv2/core/core.hpp>  
#include <opencv2/highgui/highgui.hpp>  
#include <opencv2/imgproc/imgproc.hpp>  

#pragma  comment(lib,"ws2_32.lib")  

using namespace cv;
using namespace std;

VideoCapture cam(0);
Mat img_proc, gray, canny, dst, result;
bool detected = false;

struct Line {
	Point _p1;
	Point _p2;
	Point _center;

	Line(Point p1, Point p2) {
		_p1 = p1;
		_p2 = p2;
		_center = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2);
	}
};

bool cmp_y(const Line &p1, const Line &p2) {
	return p1._center.y < p2._center.y;
}

bool cmp_x(const Line &p1, const Line &p2) {
	return p1._center.x < p2._center.x;
}

Point2f computeIntersect(Line l1, Line l2) {
	int x1 = l1._p1.x, x2 = l1._p2.x, y1 = l1._p1.y, y2 = l1._p2.y;
	int x3 = l2._p1.x, x4 = l2._p2.x, y3 = l2._p1.y, y4 = l2._p2.y;
	if (float d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)) {
		Point2f pt;
		pt.x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d;
		pt.y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d;
		return pt;
	}
	return Point2f(-1, -1);
}

void scan(Mat img, bool debug = true) {

	double h_proc = img.size().height;
	double w_proc = img.size().width;
	img.copyTo(img_proc);

	cvtColor(img, gray, CV_BGR2GRAY);
	blur(gray, gray, Size(5, 5));
	Canny(gray, canny, 20, 60, 3, false);

	dilate(canny, canny, Mat(), Point(-1, -1), 3, 1, Scalar(1));

	vector<Vec4i> lines;
	vector<Line> horizontals, verticals;
	HoughLinesP(canny, lines, 5, CV_PI / 180, img.size().height / 2, img.size().height / 2, 20);


	for (size_t i = 0; i < lines.size(); i++) {
		Vec4i v = lines[i];
		double delta_x = v[0] - v[2], delta_y = v[1] - v[3];
		Line l(Point(v[0], v[1]), Point(v[2], v[3]));

		if (fabs(delta_x) > fabs(delta_y)) {
			horizontals.push_back(l);
		}
		else {
			verticals.push_back(l);
		}

		if (debug)
			line(img_proc, Point(v[0], v[1]), Point(v[2], v[3]), Scalar(0, 0, 255), 1, CV_AA);
	}

	if (horizontals.size() < 2) {
		if (horizontals.size() == 0 || horizontals[0]._center.y > h_proc / 2) {
			horizontals.push_back(Line(Point(0, 0), Point(w_proc - 1, 0)));
		}
		if (horizontals.size() == 0 || horizontals[0]._center.y <= h_proc / 2) {
			horizontals.push_back(Line(Point(0, h_proc - 1), Point(w_proc - 1, h_proc - 1)));
		}
	}
	if (verticals.size() < 2) {
		if (verticals.size() == 0 || verticals[0]._center.x > w_proc / 2) {
			verticals.push_back(Line(Point(0, 0), Point(0, h_proc - 1)));
		}
		if (verticals.size() == 0 || verticals[0]._center.x <= w_proc / 2) {
			verticals.push_back(Line(Point(w_proc - 1, 0), Point(w_proc - 1, h_proc - 1)));
		}
	}

	if (horizontals.size() > 2 && verticals.size() > 2) {
		detected = true;
	}
	else {
		detected = false;
	}

	sort(horizontals.begin(), horizontals.end(), cmp_y);
	sort(verticals.begin(), verticals.end(), cmp_x);

	if (debug) {
		line(img_proc, horizontals[0]._p1, horizontals[0]._p2, Scalar(0, 255, 0), 2, CV_AA);
		line(img_proc, horizontals[horizontals.size() - 1]._p1, horizontals[horizontals.size() - 1]._p2, Scalar(0, 255, 0), 2, CV_AA);
		line(img_proc, verticals[0]._p1, verticals[0]._p2, Scalar(255, 0, 0), 2, CV_AA);
		line(img_proc, verticals[verticals.size() - 1]._p1, verticals[verticals.size() - 1]._p2, Scalar(255, 0, 0), 2, CV_AA);
	}

	dst = Mat::zeros(h_proc, w_proc, CV_8UC3);

	vector<Point2f> dst_pts, img_pts;
	dst_pts.push_back(Point(0, 0));
	dst_pts.push_back(Point(w_proc - 1, 0));
	dst_pts.push_back(Point(0, h_proc - 1));
	dst_pts.push_back(Point(w_proc - 1, h_proc - 1));

	img_pts.push_back(computeIntersect(horizontals[0], verticals[0]));
	img_pts.push_back(computeIntersect(horizontals[0], verticals[verticals.size() - 1]));
	img_pts.push_back(computeIntersect(horizontals[horizontals.size() - 1], verticals[0]));
	img_pts.push_back(computeIntersect(horizontals[horizontals.size() - 1], verticals[verticals.size() - 1]));

	for (size_t i = 0; i < img_pts.size(); i++) {
		if (debug) {
			circle(img_proc, img_pts[i], 10, Scalar(255, 255, 0), 3);
		}
	}

	Mat transmtx = getPerspectiveTransform(img_pts, dst_pts);

	warpPerspective(img, dst, transmtx, dst.size());

	if (debug) {
		imshow("canny", canny);
		imshow("img_proc", img_proc);
	}

	cvtColor(dst, result, CV_BGR2GRAY);
	equalizeHist(result, result);
	threshold(result, result, 20, 255, THRESH_BINARY);
	erode(result, result, Mat(), Point(-1, -1), 2, 1, Scalar(1));

	if (detected) {
		imshow("dst", dst);
		imshow("result", result);
	}
}

int main(int argc, char** argv) {
	WORD sockVersion = MAKEWORD(2, 2);
	WSADATA data;
	if (WSAStartup(sockVersion, &data) != 0)
	{
		return 0;
	}

	SOCKET sclient = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
	if (sclient == INVALID_SOCKET)
	{
		printf("invalid socket !\n");
		return 0;
	}

	sockaddr_in serAddr;
	serAddr.sin_family = AF_INET;
	serAddr.sin_port = htons(5000);
	serAddr.sin_addr.S_un.S_addr = inet_addr("127.0.0.1");
	if (connect(sclient, (sockaddr *)&serAddr, sizeof(serAddr)) == SOCKET_ERROR)
	{
		printf("connect error !\n");
		closesocket(sclient);
		return 0;
	}

	char sendData[1000000] = "";

	while (1) {
		Mat image;
		cam.retrieve(image);
		
		scan(image);

		for (int i = 0; i < result.rows; i++)
		{
			uchar* data = result.ptr<uchar>(i);
			for (int j = 0; j < result.cols; j++)
			{
				sendData[result.cols * i + j] = data[j];
			}
		}

		send(sclient, sendData, 1000000, 0);

		int key = cv::waitKey(100); 
		if (key == 27)
			break;
	}
	closesocket(sclient);
	WSACleanup();
	return 0;
}
