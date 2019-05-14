from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import glob
import sys


class LoadImg:
	def __init__(self):
		imgArray = [cv.imread(file) for file in glob.glob("images/dataset/*.jpg")]
		print(len(imgArray), "la lunghezza dell'array")
		imgData = cv.imread('images/maintenance.jpg',-1)

		if imgArray is None:
			print('Could not open or find the images!')
		self.imgArray = [cv.imread(file) for file in glob.glob("images/dataset/*.jpg")]
		print(len(self.imgArray), "la lunghezza dell'array")
		self.imgData = cv.imread('images/maintenance.jpg',-1)

		if self.imgArray is None:
			print('Could not open or find the images!')


class DisplayData:
	def __init__(self,LoadImg):
		self.rows,self.cols,self.channels = LoadImg.imgData.shape
		self.imgDatagray = cv.cvtColor(LoadImg.imgData,cv.COLOR_BGR2GRAY)
		self.ret,self.mask = cv.threshold(self.imgDatagray, 10, 255, cv.THRESH_BINARY)
		self.mask_inv = cv.bitwise_not(self.mask)
	
	def print(self,frame,LoadImg):
		alpha = 0
		# Select the region in the frame where we want to add the image and add the images using cv2.addWeighted()
		added_image = cv.addWeighted(frame[150:250,150:250,:],alpha,LoadImg.imgData[0:100,0:100,:],1-alpha,0)
    	# Change the region with the result
		frame[150:250,150:250] = added_image

def main():

	loader=LoadImg()
	data=DisplayData(loader)
	#inizialize camera

	#-- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
	minHessian = 500
	detector = cv.xfeatures2d_SIFT.create()

	keypointsArr = [None]*len(loader.imgArray)
	descriptorsArr = [None]*len(loader.imgArray)
	for curr_img in range(len(loader.imgArray)):
		keypointsArr[curr_img]=detector.detectAndCompute(loader.imgArray[curr_img],None)[0]
		descriptorsArr[curr_img]=detector.detectAndCompute(loader.imgArray[curr_img],None)[1]

	#-- Step 2: Matching descriptor vectors with a FLANN based matcher

	# Since SURF is a floating-point descriptor NORM_L2 is used
	matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
	#-- Filter matches using the Lowe's ratio test
	ratio_thresh = 0.6

	videoCapture = cv.VideoCapture(0)
	good_matches= []
	exit = False
	while videoCapture.isOpened() and not exit:
		for index in range(len(loader.imgArray)):
			ret, frame = videoCapture.read()

			keypointsFrame, descriptorsFrame = detector.detectAndCompute(frame, None)
			knn_matchesFrame = matcher.knnMatch(descriptorsArr[index], descriptorsFrame, 2)

			for m,n in knn_matchesFrame:
				if m.distance < ratio_thresh * n.distance:
					good_matches.append(m)
			#print("Punti trovati",len(good_matches)," Banconota ",index)

		#-- Draw matches
			img_matches = np.empty((max(loader.imgArray[index].shape[0], frame.shape[0]), loader.imgArray[index].shape[1]+frame.shape[1], 3), dtype=np.uint8)
			cv.drawMatches(loader.imgArray[index],keypointsArr[index] , frame, keypointsFrame, good_matches, img_matches, flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
			#gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
			cv.imshow('View',frame)

			if cv.waitKey(1) == 27:
				exit = True
			

			# cv.destroyAllWindows()
			#cv.imshow('View',img_matches)
			if good_matches != None and len(good_matches)>=20:
				print("Banconota ",index)
				data.print(frame,loader)
			
			cv.imshow('View',frame)
			
			good_matches.clear()

	if exit:
		videoCapture.release()
		cv.destroyAllWindows()

	

if __name__ == "__main__":
	main()
