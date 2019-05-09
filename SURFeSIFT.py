from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import glob

# img1 = cv.imread('images/10.jpg')
# img2 = cv.imread('images/2.jpg')
imgArray = [cv.imread(file) for file in glob.glob("images/dataset/*.jpg")]

print(len(imgArray), "la lunghezza dell'array")

# if img1 is None or img2 is None:
    # print('Could not open or find the images!')
    # exit(0)


#inizialize camera
videoCapture = cv.VideoCapture(0)

#-- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
minHessian = 500
detector = cv.xfeatures2d_SURF.create(hessianThreshold=minHessian)

# keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
# keypoints2, descriptors2 = detector.detectAndCompute(img2, None)

keypointsArr = [None]*len(imgArray)
descriptorsArr = [None]*len(imgArray)
for curr_img in range(len(imgArray)):
	keypointsArr[curr_img]=detector.detectAndCompute(imgArray[curr_img],None)[0]
	descriptorsArr[curr_img]=detector.detectAndCompute(imgArray[curr_img],None)[1]

#-- Step 2: Matching descriptor vectors with a FLANN based matcher

# Since SURF is a floating-point descriptor NORM_L2 is used
matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
# knn_matches = matcher.knnMatch(descriptors1, descriptors2, 2)
#-- Filter matches using the Lowe's ratio test
ratio_thresh = 0.5

good_matches= []

#-- Show detected matches
#cv.imshow('Good Matches', img_matches
#cv.imwrite('sift.jpg',img_matches)

# img_matches = None
while videoCapture.isOpened():
	for index in range(len(imgArray)):
		ret, frame = videoCapture.read()
		keypointsFrame, descriptorsFrame = detector.detectAndCompute(frame, None)
		knn_matchesFrame = matcher.knnMatch(descriptorsArr[index], descriptorsFrame, 2)
	#for curr_desc in range(len(descriptorsArr)):
		#knn_matchesFrameArray[curr_desc]=matcher.knnMatch(descriptorsArr[curr_desc],descriptorsFrame,2)
	#for curr_match in knn_matchesFrameArray:
		for m,n in knn_matchesFrame:
			if m.distance < ratio_thresh * n.distance:
				good_matches.append(m)
		print("Punti trovati",len(good_matches)," Banconota ",index)
		#percentage=good_
	#-- Draw matches
		img_matches = np.empty((max(imgArray[index].shape[0], frame.shape[0]), imgArray[index].shape[1]+frame.shape[1], 3), dtype=np.uint8)
		cv.drawMatches(imgArray[index],keypointsArr[index] , frame, keypointsFrame, good_matches, img_matches, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
		#gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		cv.waitKey(1)
		cv.imshow('View',img_matches)
		#cv.imshow('View',frame)
		if good_matches != None and len(good_matches)>=20:
			print("Banconota ",index)
			break
		good_matches.clear()


videoCapture.release()
cv.waitKey()
