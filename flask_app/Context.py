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

class Context:
    def __init__(self, strategyChoose : AlgorithmChooser):
        print("Costruttore di Context")
        self.strategy = strategyChoose

    def doAlgorithm(self, img):
        self.strategy.doAlgorithm(img)

    #@AlgorithmChooser.setter
    def setStrategy(self, strategyChoose: AlgorithmChooser) :
        self.strategy = strategyChoose

    def setStrategy2(self,strategyChoose):
        self.strategy = strategyChoose
    

    @property
    def getStrategy(self) -> AlgorithmChooser:
        return self.strategy




    #-- Draw matches
        ##img_matches = np.empty((max(self.loader.imgArray[index].shape[0], frame.shape[0]),self.loader.imgArray[index].shape[1]+frame.shape[1], 3), dtype=np.uint8)
        #   cv2.drawMatches(self.loader.imgArray[index], self.keypointsArr[index], frame, keypointsFrame,
                        #   self.good_matches, img_matches, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
        #   cv2.imshow('View', frame)
