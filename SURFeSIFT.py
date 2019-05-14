from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
import glob

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
		roi = frame[0:self.rows, 0:self.cols]
			
		# Now black-out the area of logo in ROI
		videoCamera_bg = cv.bitwise_and(roi,roi,mask = self.mask_inv)

		# Take only region of logo from logo image.
		imgData_fg = cv.bitwise_and(LoadImg.imgData,LoadImg.imgData,mask = self.mask)

		# Put logo in ROI and modify the main image
		dst = cv.add(videoCamera_bg,imgData_fg)

		frame[0:self.rows, 0:self.cols ] = dst
		cv.imshow("dwad",LoadImg.imgData)

def main():

	loader=LoadImg()
	data=DisplayData(loader)
	#inizialize camera
	videoCapture = cv.VideoCapture(0)

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

	good_matches= []

	while videoCapture.isOpened():
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
			cv.waitKey(1)
			#cv.imshow('View',img_matches)
			cv.imshow('View',frame)
			if good_matches != None and len(good_matches)>=20:
				print("Banconota ",index)
				data.print(frame,loader)
			
			good_matches.clear()


	videoCapture.release()
	cv.destroyAllWindows()
	cv.waitKey()

if __name__ == "__main__":
	main()
