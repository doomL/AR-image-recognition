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

FILE_OUTPUT = 'output.avi'

class videoSave(object):
    def __init__(self):
        print("init mK")
        self.out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'X264'), 5.0, (100,100))
    def saveFrame(self, img):
        #if img != None:
        self.out.write(np.asarray(img))
        return img.transpose(Image.FLIP_LEFT_RIGHT)

    def __del__(self):
        pass
        #out.release()