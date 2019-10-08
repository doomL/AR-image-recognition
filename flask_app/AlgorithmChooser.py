from abc import ABC, abstractmethod
import cv2
import numpy as np
import argparse

from utils import loadImg
class AlgorithmChooser(ABC):

    @abstractmethod
    def doAlgorithm(self,img):
        pass


class SiftAlgorithm():
    def __init__(self):
        print("SIFT")
        self.loader=loadImg()
        minHessian = 500
        self.detector = cv2.xfeatures2d_SIFT.create()
        print(len(self.loader.imgArray))
        self.keypointsArr = [None]*len(self.loader.imgArray)
        self.descriptorsArr = [None]*len(self.loader.imgArray)
        for curr_img in range(len(self.loader.imgArray)):
            self.keypointsArr[curr_img] = self.detector.detectAndCompute(self.loader.imgArray[curr_img], None)[0]
            self.descriptorsArr[curr_img] = self.detector.detectAndCompute(self.loader.imgArray[curr_img], None)[1]
        self.matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        self.ratio_tresh = 0.6

        self.good_matches = []

    def doAlgorithm(self, img):
        self.frame = np.asarray(img)
        # print("frame",self.frame)
        keypointsFrame, self.descriptorsFrame = self.detector.detectAndCompute(self.frame, None)

        for index in range(len(self.loader.imgArray)):
            # print(self.descriptorsArr[index])
            # print("descriptor",self.descriptorsFrame)
            knn_matchesFrame = self.matcher.knnMatch(self.descriptorsArr[index], self.descriptorsFrame, 2)

            for m, n in knn_matchesFrame:
                if m.distance < self.ratio_tresh * n.distance:
                    self.good_matches.append(m)

        print("GOOD MATCHES", len(self.good_matches))

        if self.good_matches != None and len(self.good_matches) >= 40:
            print("TROVATA BANCONOTA ", index, "CON ",len(self.good_matches),"MATCHES")

        self.good_matches.clear()
        

        # print("IMMAGINE DI SIFT ALGORITHMMMMMMMMMMMMMM")
        # print(img)

        # return self.frame


class SurfAlgorithm(AlgorithmChooser):

    def __init__(self):
        print("SURF")
        self.loader = loadImg()
        minHessian = 500
        self.detector = cv2.xfeatures2d_SURF.create()
        print(len(self.loader.imgArray))
        self.keypointsArr = [None]*len(self.loader.imgArray)
        self.descriptorsArr = [None]*len(self.loader.imgArray)
        for curr_img in range(len(self.loader.imgArray)):
            self.keypointsArr[curr_img] = self.detector.detectAndCompute(
                self.loader.imgArray[curr_img], None)[0]
            self.descriptorsArr[curr_img] = self.detector.detectAndCompute(
                self.loader.imgArray[curr_img], None)[1]
        self.matcher = cv2.DescriptorMatcher_create(
            cv2.DescriptorMatcher_FLANNBASED)
        self.ratio_tresh = 0.6

        self.good_matches = []


    def doAlgorithm(self, img):
        self.frame = np.asarray(img)
        # print("frame",self.frame)
        keypointsFrame, self.descriptorsFrame = self.detector.detectAndCompute(
            self.frame, None)

        for index in range(len(self.loader.imgArray)):
            # print(self.descriptorsArr[index])
            # print("descriptor",self.descriptorsFrame)
            knn_matchesFrame = self.matcher.knnMatch(
                self.descriptorsArr[index], self.descriptorsFrame, 2)

            for m, n in knn_matchesFrame:
                if m.distance < self.ratio_tresh * n.distance:
                    self.good_matches.append(m)

        print("GOOD MATCHES", len(self.good_matches))

        if self.good_matches != None and len(self.good_matches) >= 27:
            print("TROVATA BANCONOTA ", index, "CON ",
                  len(self.good_matches), "MATCHES")

        self.good_matches.clear()

