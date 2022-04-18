# frame2diff
##### 두 프레임의 픽셀 값 차를 이용한 객체 검출[vehicle.py]

- 두 이미지의 픽셀 차를 문턱치 적용하여 엣지 추출
```
diff_image = cv2.absdiff(grayB, grayA)
ret, thresh = cv2.threshold(diff_image, 30, 255, cv2.THRESH_BINARY)
```

![예제](./img/예제.JPG)

##### 블러를 사용한 케니 엣지 [케니엣지.cpp]

- 그레이스케일로 변환 후 블러를 주고 캐니 엣지를 수행
- dilate로 엣지를 강조
```
cvtColor(img, gray, CV_BGR2GRAY);
blur(gray, gray, Size(5, 5));
Canny(gray, canny, 20, 60, 3, false);

dilate(canny, canny, Mat(), Point(-1, -1), 3, 1, Scalar(1));
```
