from __future__ import print_function
import cv2
import numpy as np
import argparse
import glob
import sys
from flask import Flask, render_template, Response, request
from flask_mysqldb import MySQL 
import base64
import io
from PIL import Image
import AlgorithmChooser

MIN_MATCHES=25
     
class Algorithm(object):
    def __init__(self):
        # self.algorithm = AlgorithmChooser
        self.loader = LoadImg()
        #-- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
        minHessian = 500
        self.detector = cv2.xfeatures2d_SIFT.create()

        self.keypointsArr = [None]*len(self.loader.imgArray)
        self.descriptorsArr = [None]*len(self.loader.imgArray)
        for curr_img in range(len(self.loader.imgArray)):
            self.keypointsArr[curr_img] = self.detector.detectAndCompute(self.loader.imgArray[curr_img], None)[0]
            self.descriptorsArr[curr_img] = self.detector.detectAndCompute(self.loader.imgArray[curr_img], None)[1]

        #-- Step 2: Matching descriptor vectors with a FLANN based self.matcher

        # Since SURF is a floating-point descriptor NORM_L2 is used
        self.matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        #-- Filter matches using the Lowe's ratio test
        self.ratio_tresh = 0.6

        self.good_matches = []

    def apply_algorithm(self,img):
        frame = np.asarray(img)
        keypointsFrame, descriptorsFrame = self.detector.detectAndCompute(frame, None)
        
        for index in range(len(self.loader.imgArray)):
            knn_matchesFrame = self.matcher.knnMatch(self.descriptorsArr[index], descriptorsFrame, 2)

            for m, n in knn_matchesFrame:
                if m.distance < self.ratio_tresh * n.distance:
                    self.good_matches.append(m)

        if self.good_matches != None and len(self.good_matches) >= MIN_MATCHES:
            print("Banconota ", index)

        self.good_matches.clear()

        return img

    #-- Draw matches
        ##img_matches = np.empty((max(self.loader.imgArray[index].shape[0], frame.shape[0]),self.loader.imgArray[index].shape[1]+frame.shape[1], 3), dtype=np.uint8)
        #   cv2.drawMatches(self.loader.imgArray[index], self.keypointsArr[index], frame, keypointsFrame,
                        #   self.good_matches, img_matches, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        #   cv2.imshow('View', frame)

class CalcFeature:
    def __init__(self,img):
        detector = cv2.xfeatures2d_SURF.create(hessianThreshold=200)
        keypointsImg, descriptorsImg = detector.detectAndCompute(self.toRGB(self.stringToImage(img)), None)
        print(keypointsImg)
        
        # Take in base64 string and return PIL image
    def stringToImage(self,base64_string):
        base64_string += "=" * ((4 - len(base64_string) % 4) % 4) #ugh
        imgdata = base64.b64decode(base64_string)
        return Image.open(io.BytesIO(imgdata))

    # convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
    def toRGB(self,image):
        return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        

class LoadImg:
    def __init__(self):
        self.imgArray = [cv2.imread(file)for file in glob.glob("images/dataset/*.jpg")]
        print(len(self.imgArray), "la lunghezza dell'array")
        self.imgData = cv2.imread('images/maintenance.jpg', -1)

        if self.imgArray is None:
            print('Could not open or find the images!')