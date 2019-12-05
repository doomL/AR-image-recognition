from __future__ import print_function
import cv2 
import numpy as np
import argparse
import glob
import sys
from flask import Flask, render_template, Response
from flask_mysqldb import MySQL 

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'hostremotemyslq.com:3306'
app.config['MYSQL_USER'] = 'LZAHaN9tbA'
app.config['MYSQL_PASSWORD'] = 'DcbgVhCK63'
app.config['MYSQL_DB'] = 'LZAHaN9tbA'

mySql = MySQL(app)

@app.route('/')
def index():
   return render_template('hello.html')

def gen(camera):
   while True:
      frame = camera.get_frame()
      yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
   return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/login',methods=['GET', 'POST'])
def login():
   details = request.form



class VideoCamera(object):
   def __init__(self):
      self.video = cv2.VideoCapture(0)
      self.loader=LoadImg()
      #data=DisplayData(self.loader)
	   #inizialize camera

   	#-- Step 1: Detect the keypoints using SURF Detector, compute the descriptors
      minHessian = 500
      self.detector = cv2.ORB_create(nfeatures=1200, scoreType=cv2.ORB_FAST_SCORE)

      self.keypointsArr = [None]*len(self.loader.imgArray)
      self.descriptorsArr = [None]*len(self.loader.imgArray)
      for curr_img in range(len(self.loader.imgArray)):
         self.keypointsArr[curr_img]=self.detector.detectAndCompute(self.loader.imgArray[curr_img],None)[0]
         self.descriptorsArr[curr_img]=self.detector.detectAndCompute(self.loader.imgArray[curr_img],None)[1]

	   #-- Step 2: Matching descriptor vectors with a FLANN based self.matcher

	   # Since SURF is a floating-point descriptor NORM_L2 is used
      self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
      #-- Filter matches using the Lowe's ratio test
      self.ratio_tresh = 0.6

	   #videoCapture = cv2.VideoCapture(0)
      exit = False

   def __del__(self):
      self.video.release()

   def get_frame(self):
      for index in range(len(self.loader.imgArray)):
         ret, frame = self.video.read()

         keypointsFrame, descriptorsFrame = self.detector.detectAndCompute(frame, None)
         #knn_matchesFrame = self.matcher.knnMatch(self.descriptorsArr[index], descriptorsFrame, 2)
         self.matches = self.matcher.match(self.descriptorsArr[index], descriptorsFrame)
         self.matches = sorted(self.matches, key = lambda x: x.distance)

         #for m,n in matches:
          #  if m.distance < self.ratio_tresh * n.distance:
          #     self.good_matches.append(m)
			#print("Punti trovati",len(self.good_matches)," Banconota ",index)

         # print(len(self.matches))

         if len(self.matches) >= 510: 
            print("Trovata una corrispondenza con immagine ", index)

		#-- Draw matches
      # img_matches = np.empty((max(self.loader.imgArray[index].shape[0], frame.shape[0]), self.loader.imgArray[index].shape[1]+frame.shape[1], 3), dtype=np.uint8)
      # cv2.drawMatches(self.loader.imgArray[index],self.keypointsArr[index] , frame, keypointsFrame, self.good_matches, img_matches, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
		#gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      # cv2.imshow('View',frame)

      # if cv2.waitKey(1) == 27:
      #    exit = True
			

		# cv2.destroyAllWindows()
		#cv2.imshow('View',img_matches)
      success, image = self.video.read()
      ret, jpeg = cv2.imencode('.jpg', image)
      return jpeg.tobytes()


class LoadImg:
	def __init__(self):
		self.imgArray = [cv2.imread(file) for file in glob.glob("images/dataset/*.jpg")]
		print(len(self.imgArray), "la lunghezza dell'array")
		self.imgData = cv2.imread('images/maintenance.jpg',-1)

		if self.imgArray is None:
		   print('Could not open or find the images!')

class DisplayData:
   def __init__(self,LoadImg):
      self.rows,self.cols,self.channels = LoadImg.imgData.shape
      self.imgDatagray = cv2.cvtColor(LoadImg.imgData,cv2.COLOR_BGR2GRAY)
      self.ret,self.mask = cv2.threshold(self.imgDatagray, 10, 255, cv2.THRESH_BINARY)
      self.mask_inv = cv2.bitwise_not(self.mask)

   def print(self,frame,LoadImg):
      alpha = 0
      # Select the region in the frame where we want to add the image and add the images using cv2.addWeighted()
      added_image = cv2.addWeighted(frame[150:250,150:250,:],alpha,LoadImg.imgData[0:100,0:100,:],1-alpha,0)
      # Change the region with the result
      frame[150:250,150:250] = added_image

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
    