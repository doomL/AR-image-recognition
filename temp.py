from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import glob	


parser = argparse.ArgumentParser(description='Code for Feature Matching with FLANN tutorial.')
parser.add_argument('--input1', help='Path to input image 1.', default='10.jpg')
parser.add_argument('--input2', help='Path to input image 2.', default='2.jpg')




args = parser.parse_args()
img1 = cv.imread('10.jpg')
img2 = cv.imread('2.jpg')
imgArray = [cv.imread(file) for file in glob.glob("*.jpg")]

print(len(imgArray), "la lunghezza dell'array")

if img1 is None or img2 is None:
    print('Could not open or find the images!')
    exit(0)


#inizialize camera
videoCapture = cv.VideoCapture(0)

#-- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
minHessian = 200
detector = cv.xfeatures2d_SURF.create(hessianThreshold=minHessian)

keypoints1, descriptors1 = detector.detectAndCompute(img1, None)
keypoints2, descriptors2 = detector.detectAndCompute(img2, None)

keypointsArr = []
descriptorsArr = []
for curr_img in range(0,len(imgArray)):
	indice = 0
	keypointsArr,descriptorsArr=detector.detectAndCompute(curr_img,None)
	
#-- Step 2: Matching descriptor vectors with a FLANN based matcher

# Since SURF is a floating-point descriptor NORM_L2 is used
matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
knn_matches = matcher.knnMatch(descriptors1, descriptors2, 2)
#-- Filter matches using the Lowe's ratio test
ratio_thresh = 0.6
good_matches = []


#-- Show detected matches
#cv.imshow('Good Matches', img_matches
#cv.imwrite('sift.jpg',img_matches)

while videoCapture.isOpened():
	good_matches.clear()
	ret, frame = videoCapture.read()
	keypointsFrame, descriptorsFrame = detector.detectAndCompute(frame, None)
	knn_matchesFrame = matcher.knnMatch(descriptors1, descriptorsFrame, 2)
	for curr_desc in descriptorsArr:
		knn_matchesFrameArray.append(matcher.knnMatch(curr_desc,descriptorsFrame,2))
	for curr_match in knn_matchesFrameArray:
		for m,n in curr_match:
			if m.distance < ratio_thresh * n.distance:
				good_matches.append(m)
	print("Punti trovati",len(good_matches))

	#-- Draw matches
	for index in range(0,len(imgArray)):
		img_matches = np.empty((max(curr_img.shape[0], frame.shape[0]), curr_img.shape[1]+frame.shape[1], 3), dtype=np.uint8)
		cv.drawMatches(imgArray[index], keypointsArr[index], frame, keypointsFrame, good_matches, img_matches, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

	gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	cv.waitKey(50)
	cv.imshow('Camera Open Maybe',img_matches)

	if cv.waitKey(1) & 0xFF == ord('q'):
		print("tasto premuto")
		break

videoCapture.release()
cv.waitKey()