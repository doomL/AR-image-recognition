from abc import ABC, abstractmethod
import cv2
import numpy as np
import argparse
from utils import loadImg,toRGB
from collections import deque
from math import sqrt
import argparse
from datetime import datetime
# import samples
# minhessian -> Un valore maggiore comporterà un numero inferiore, 
# ma (teoricamente) di punti di interesse più salienti, 
# mentre un valore inferiore comporterà punti più numerosi ma meno salienti.




class AlgorithmChooser(ABC):

    @abstractmethod
    def doAlgorithm(self,img):
        pass

# ORB HARRIS
class OrbHarrisAlgorithm(AlgorithmChooser):

    def __init__(self,loader):
        print("ORB HARRIS")
        self.orbMinMatches = 130  # di solito 120
        self.cont=0
        self.contaDiSeguito = 0
        self.loader = loader
        
        self.detector = cv2.ORB_create(nfeatures=700)

        self.keypointsArrDict= {}
        self.descriptorsArrDict= {}      

        prima=datetime.timestamp(datetime.now())
        for curr_Id in self.loader.id_Images:
            # self.keypointsArrDict[curr_Id] = self.detector.detectAndCompute(
            #     self.loader.id_Images[curr_Id], None)[0]
                
            self.descriptorsArrDict[curr_Id] = self.detector.detectAndCompute(
                self.loader.id_Images[curr_Id], None)[1]

        dopo=datetime.timestamp(datetime.now())
        print("TEMPO PER CARICARE : ",len(self.loader.id_Images)," ",dopo-prima)
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)

        self.ratio_tresh = 0.9

        self.good_matches = deque()


# ORB HARRIS DO FUNCTION

    def doAlgorithm(self, img):
        # print("ORB HARRIS")
        self.frame = np.asarray(img)
        # print("frame",self.frame)
        keypointsFrame, self.descriptorsFrame = self.detector.detectAndCompute(self.frame, None)
        
        if(np.all(self.descriptorsFrame!=None)):
            for curr_Id in self.loader.id_Images:
                knn_matchesFrame = self.matcher.knnMatch(self.descriptorsArrDict[curr_Id], self.descriptorsFrame, 2)

                # cv2.imwrite("frame.png",self.frame)
                for m, n in knn_matchesFrame:
                    if m.distance < self.ratio_tresh * n.distance:
                        self.good_matches.append(m)

                # print("PRIMA DI PULIRE HO TROVATO", len(self.good_matches))

                if self.good_matches != None and len(self.good_matches) >= self.orbMinMatches:
                    # self.contaDiSeguito += 1
                    # print("CONTA DI SEGUITO :",self.contaDiSeguito)
                    # if(self.contaDiSeguito>=1):
                    print("TROVATO MACCHINARIO: ", curr_Id, "CON ",len(self.good_matches),"MATCHES")
                    self.good_matches.clear()
                    return curr_Id

                # if self.good_matches != None and len(self.good_matches) < self.orbMinMatches:
                #     self.contaDiSeguito = 0
                self.good_matches.clear()




class SiftAlgorithm(AlgorithmChooser):

    def __init__(self,loader):

        print("SIFT")
        self.cont = 0
        self.siftMinMatches = 25
        self.loader=loader
        minHessian = 500
        self.detector = cv2.xfeatures2d_SIFT.create()
        self.keypointsArrDict= {}
        self.descriptorsArrDict= {}
        prima=datetime.timestamp(datetime.now())

        
        for curr_Id in self.loader.id_Images:
            self.keypointsArrDict[curr_Id] = self.detector.detectAndCompute(self.loader.id_Images[curr_Id], None)[0]
            self.descriptorsArrDict[curr_Id] = self.detector.detectAndCompute(self.loader.id_Images[curr_Id], None)[1]

        dopo=datetime.timestamp(datetime.now())
        print("TEMPO PER CARICARE SIFT: ",len(self.loader.id_Images)," ",dopo-prima)

        self.matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        self.ratio_tresh = 0.6

        self.good_matches = deque()

    def doAlgorithm(self, img):
        print("SIIIIIIIIIIIIIFT")
        self.frame = np.asarray(img)
        # print("frame",self.frame)
        keypointsFrame, self.descriptorsFrame = self.detector.detectAndCompute(self.frame, None)


        if(np.all(self.descriptorsFrame!=None)):
            for curr_Id in self.loader.id_Images:
                # print(self.descriptorsArr[index])
                # print("descriptor",self.descriptorsFrame)
                knn_matchesFrame = self.matcher.knnMatch(self.descriptorsArrDict[curr_Id], self.descriptorsFrame, 2)
                # cv2.imwrite("frame.png",self.frame)
                for m, n in knn_matchesFrame:
                    if m.distance < self.ratio_tresh * n.distance:
                        self.good_matches.append(m)

                # print("PRIMA DI PULIRE HO TROVATO", len(self.good_matches))
                

                if self.good_matches != None and len(self.good_matches) >= self.siftMinMatches:
                    print("TROVATO MACCHINARIO: ", curr_Id, "CON ",len(self.good_matches),"MATCHES")
                    self.good_matches.clear()
                    return curr_Id
                
                
                self.good_matches.clear()
                
        

        # print("IMMAGINE DI SIFT ALGORITHMMMMMMMMMMMMMM")
        # print(img)

        # return self.frame


class SurfAlgorithm(AlgorithmChooser):

    def __init__(self,loader):
        print("SURF")
        self.surfMinMatches = 15
        self.cont=0
        self.loader = loader
        minHessian = 1000
        self.detector = cv2.xfeatures2d_SURF.create()
        # self.detector = cv2.SURF()
        # print(len(self.loader.imgArray))
        self.keypointsArrDict={}
        self.descriptorsArrDict={}
        prima=datetime.timestamp(datetime.now())
        #self.keypointsArr = [None]*len(self.loader.id_Images)
        #self.descriptorsArr = [None]*len(self.loader.id_Images)
        
        for curr_Id in self.loader.id_Images:
            self.keypointsArrDict[curr_Id]=self.detector.detectAndCompute(self.loader.id_Images[curr_Id],None)[0]
            self.descriptorsArrDict[curr_Id]=self.detector.detectAndCompute(self.loader.id_Images[curr_Id],None)[1]

        dopo=datetime.timestamp(datetime.now())
        print("TEMPO PER CARICARE SURF : ",len(self.loader.id_Images)," ",dopo-prima)
        # print(self.descriptorsArrDict)     
       
       
        # for curr_img in range(len(self.loader.id_Images)):
            # self.keypointsArr[curr_img] = self.detector.detectAndCompute(
            #     self.loader.imgArray[curr_img], None)[0]
            # self.descriptorsArr[curr_img] = self.detector.detectAndCompute(
            #     self.loader.imgArray[curr_img], None)[1]
        self.matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_FLANNBASED)
        self.ratio_tresh = 0.6

        self.good_matches =deque()

    def doAlgorithm(self, img):
        print("SUUUUUURF")
        self.frame = toRGB(np.asarray(img))
        
        keypointsFrame, self.descriptorsFrame = self.detector.detectAndCompute(
            self.frame, None)


        if(np.all(self.descriptorsFrame!=None)):

            for curr_Id in self.loader.id_Images:
                # cv2.imwrite("frame.png",self.loader.id_Images[curr_Id])
    
                knn_matchesFrame = self.matcher.knnMatch(self.descriptorsArrDict[curr_Id], self.descriptorsFrame,2)

                for m, n in knn_matchesFrame:
                    if m.distance < self.ratio_tresh * n.distance:
                        self.good_matches.append(m)

                # print("PRIMA DI PULIRE HO TROVATO", len(self.good_matches))
                if self.good_matches != None and len(self.good_matches) >= self.surfMinMatches:
                    print("TROVATO MACCHINARIO: ", curr_Id, "CON ",len(self.good_matches), "MATCHES")
                    self.good_matches.clear()
                    return curr_Id
                
                self.good_matches.clear()



# OOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRBBBBBBBBBBBBBBBBBBBBBBBB

class OrbAlgorithm(AlgorithmChooser):

    def __init__(self,loader):
        print("ORB FAST SCORE")
        self.orbMinMatches = 50
        self.cont=0
        self.loader = loader
        minHessian = 500
        self.detector = cv2.ORB_create(nfeatures=300,scoreType=cv2.ORB_FAST_SCORE )

        # print(len(self.loader.imgArray))

        self.keypointsArrDict= {}
        self.descriptorsArrDict= {}        
        prima=datetime.timestamp(datetime.now())
        for curr_Id in self.loader.id_Images:
            # self.keypointsArrDict[curr_Id] = self.detector.detectAndCompute(
            #     self.loader.id_Images[curr_Id], None)[0]
            self.descriptorsArrDict[curr_Id] = self.detector.detectAndCompute(
                self.loader.id_Images[curr_Id], None)[1]

        dopo=datetime.timestamp(datetime.now())
        print("TEMPO PER CARICARE ORB FAST: ",len(self.loader.id_Images)," ",dopo-prima)

        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        self.ratio_tresh = 0.9

        self.good_matches = deque()


# OOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRBBBBBBBBBBBBBBBBBBBBBBBB

    def doAlgorithm(self, img):
        # print("ORB")
        self.frame = np.asarray(img)
        # print("frame",self.frame)
        keypointsFrame, self.descriptorsFrame = self.detector.detectAndCompute(self.frame, None)

        if(np.all(self.descriptorsFrame!=None)):
            # print("ENTRO 1")
            for curr_Id in self.loader.id_Images:
                knn_matchesFrame = self.matcher.knnMatch(self.descriptorsArrDict[curr_Id], self.descriptorsFrame, 2)

                for m, n in knn_matchesFrame:

                    # cv2.imwrite("frame.png",self.frame)
                    if m.distance < self.ratio_tresh * n.distance:
                        # print("ENTRO 3")
                        self.good_matches.append(m)

                # print("PRIMA DI PULIRE HO TROVATO", len(self.good_matches))

                if self.good_matches != None and len(self.good_matches) >= self.orbMinMatches:
                        print("TROVATO MACCHINARIO: ", curr_Id, "CON ",len(self.good_matches),"MATCHES")
                        self.good_matches.clear()
                        return curr_Id

                self.good_matches.clear()


        

class AkazeAlgorithm(AlgorithmChooser):

    def __init__(self,loader):
        print("CREO AKAZE")
        self.akazeMinMatches = 10
        self.loader = loader
        self.detector = cv2.AKAZE.create()

        
        self.parser = argparse.ArgumentParser(description='Code for AKAZE local features matching tutorial.')
        self.parser.add_argument('--homography', help='Path to the homography matrix.', default='H1to3p.xml')
        self.fs = cv2.FileStorage(cv2.samples.findFile(args.homography), cv2.FILE_STORAGE_READ)
        # self.homography = fs.getFirstTopLevelNode().mat()

        self.keypointsArrDict= {}
        self.descriptorsArrDict= {}  

        for curr_Id in self.loader.id_Images:
            self.keypointsArrDict[curr_Id] = self.detector.detectAndCompute(
                self.loader.id_Images[curr_Id], None)[0]
            self.descriptorsArrDict[curr_Id] = self.detector.detectAndCompute(
                self.loader.id_Images[curr_Id], None)[1]

        self.matcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)


    def doAlgorithm(self, img):

        #print("AKAZE")

        self.frame = np.asarray(img)



        keypointsFrame, self.descriptorsFrame = self.detector.detectAndCompute(self.frame, None)
        self.ratio_tresh = 0.8
        self.matched1 = []
        self.matched2 = []

        self.inliers1 = []
        self.inliers2 = []
        self.good_matches = []

        self.inlier_threshold = 2.5

        if(np.all(self.descriptorsFrame!=None)):
            
            for curr_Id in self.loader.id_Images:
                knn_matchesFrame = self.matcher.knnMatch(self.descriptorsArrDict[curr_Id], self.descriptorsFrame, 2)

                for m, n in knn_matchesFrame:
                    print("111111111111")
                    if m.distance < self.ratio_tresh * n.distance:
                        self.matched1.append(self.keypointsArrDict[curr_Id][m.queryIdx])
                        self.matched2.append(keypointsFrame[m.trainIdx])


                for i, m in enumerate(self.matched1):
                    print("222222222222")
                    col = np.ones((3,1), dtype=np.float64)
                    col[0:2,0] = m.pt
                    col = np.dot(self.homography, col)
                    col /= col[2,0]
                    dist = sqrt(pow(col[0,0] - matched2[i].pt[0], 2) +\
                                pow(col[1,0] - matched2[i].pt[1], 2))

                    if dist < self.inlier_threshold:
                        print("33333333333333")
                        self.good_matches.append(cv2.DMatch(len(inliers1), len(inliers2), 0))
                        self.inliers1.append(self.matched1[i])
                        self.inliers2.append(self.matched2[i])
                        
                        
                
    
                        

            # print("GOOD MATCHES", len(self.good_matches))

                if self.good_matches != None and len(self.good_matches) >= self.akazeMinMatches:
                        print("TROVATO MACCHINARIO: ", curr_Id, "CON ",len(self.good_matches),"MATCHES")
                        self.good_matches.clear()
                        return curr_Id
                
                self.good_matches.clear()
                self.inliers1.clear()
                self.inliers2.clear()
                self.matched1.clear()
                self.matched2.clear()





