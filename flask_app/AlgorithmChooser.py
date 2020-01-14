from abc import ABC, abstractmethod
import cv2
import numpy as np
import argparse
from utils import loadImg,toRGB
from collections import deque
# minhessian -> Un valore maggiore comporterà un numero inferiore, 
# ma (teoricamente) di punti di interesse più salienti, 
# mentre un valore inferiore comporterà punti più numerosi ma meno salienti.




class AlgorithmChooser(ABC):

    @abstractmethod
    def doAlgorithm(self,img):
        pass

class SiftAlgorithm():
    def __init__(self,loader):

        print("SIFT")
        self.cont = 0
        self.siftMinMatches = 25
        self.loader=loader
        minHessian = 500
        self.detector = cv2.xfeatures2d_SIFT.create()
        self.keypointsArrDict= {}
        self.descriptorsArrDict= {}
        
        for curr_Id in self.loader.id_Images:
            self.keypointsArrDict[curr_Id] = self.detector.detectAndCompute(self.loader.id_Images[curr_Id], None)[0]
            self.descriptorsArrDict[curr_Id] = self.detector.detectAndCompute(self.loader.id_Images[curr_Id], None)[1]
        
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

                for m, n in knn_matchesFrame:
                    if m.distance < self.ratio_tresh * n.distance:
                        self.good_matches.append(m)

            # print("GOOD MATCHES", len(self.good_matches))

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
        # print(len(self.loader.imgArray))
        self.keypointsArrDict={}
        self.descriptorsArrDict={}
        
        #self.keypointsArr = [None]*len(self.loader.id_Images)
        #self.descriptorsArr = [None]*len(self.loader.id_Images)
        
        for curr_Id in self.loader.id_Images:
            print("+++++++++++++++++++++++++++++++++++++++")
            print("----------------------------------------------------")
            self.keypointsArrDict[curr_Id]=self.detector.detectAndCompute(self.loader.id_Images[curr_Id],None)[0]
            self.descriptorsArrDict[curr_Id]=self.detector.detectAndCompute(self.loader.id_Images[curr_Id],None)[1]

        print(self.descriptorsArrDict)     
       
       
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
        # print("frame",self.frame)
        
        keypointsFrame, self.descriptorsFrame = self.detector.detectAndCompute(
            self.frame, None)


        # print(self.descriptorsArr)
        # print("stop")

        # print(self.descriptorsFrame) -> None
        if(np.all(self.descriptorsFrame!=None)):

            for curr_Id in self.loader.id_Images:
                cv2.imwrite("wsdadaw.png",self.loader.id_Images[curr_Id])
                # print(self.descriptorsArr[index])
                #print("descriptor",s   elf.descriptorsFrame)
                knn_matchesFrame = self.matcher.knnMatch(self.descriptorsArrDict[curr_Id], self.descriptorsFrame,2)

                for m, n in knn_matchesFrame:
                    if m.distance < self.ratio_tresh * n.distance:
                        self.good_matches.append(m)

                #print("GOOD MATCHES", len(self.good_matches))
                if self.good_matches != None and len(self.good_matches) >= self.surfMinMatches:
                    print("TROVATO MACCHINARIO: ", curr_Id, "CON ",len(self.good_matches), "MATCHES")
                    self.good_matches.clear()
                    return curr_Id
                self.good_matches.clear()



# OOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRBBBBBBBBBBBBBBBBBBBBBBBB

class OrbAlgorithm():

    def __init__(self,loader):
        print("ORB")
        self.orbMinMatches = 15
        self.cont=0
        self.loader = loader
        minHessian = 500
        self.detector = cv2.ORB_create(nfeatures=1200, scoreType=cv2.ORB_FAST_SCORE)

        # print(len(self.loader.imgArray))

        self.keypointsArrDict= {}
        self.descriptorsArrDict= {}        

        for curr_Id in self.loader.id_Images:
            self.keypointsArrDict[curr_Id] = self.detector.detectAndCompute(
                self.loader.id_Images[curr_Id], None)[0]
            self.descriptorsArrDict[curr_Id] = self.detector.detectAndCompute(
                self.loader.id_Images[curr_Id], None)[1]

        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
        self.ratio_tresh = 0.6

        self.good_matches = deque()


# OOOOOOOOOOOOOOOOOORRRRRRRRRRRRRRRRRRRBBBBBBBBBBBBBBBBBBBBBBBB

    def doAlgorithm(self, img):
        print("ORB")
        self.frame = np.asarray(img)
        # print("frame",self.frame)
        keypointsFrame, self.descriptorsFrame = self.detector.detectAndCompute(self.frame, None)

        if(np.all(self.descriptorsFrame!=None)):
            for curr_Id in self.loader.id_Images:
                knn_matchesFrame = self.matcher.knnMatch(self.descriptorsArrDict[curr_Id], self.descriptorsFrame, 2)

                for m, n in knn_matchesFrame:
                    if m.distance < self.ratio_tresh * n.distance:
                        self.good_matches.append(m)

            # print("GOOD MATCHES", len(self.good_matches))

                if self.good_matches != None and len(self.good_matches) >= self.orbMinMatches:
                        print("TROVATO MACCHINARIO: ", curr_Id, "CON ",len(self.good_matches),"MATCHES")
                        self.good_matches.clear()
                        return curr_Id

                self.good_matches.clear()
        


