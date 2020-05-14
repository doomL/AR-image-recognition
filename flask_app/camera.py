import threading
import binascii
import cv2
from time import sleep
from utils import base64_to_pil_image, pil_image_to_base64
from collections import deque
import numpy as np
#from VideoSave import VideoSave

class Camera:
    
    def __init__(self, context):
        self.to_process2 = []
        self.to_output2 = []
        self.to_process = deque()
        self.to_output = deque()
        self.context = context
        self.input_img = None
        self.out= None
        self.rec=False
        self.result=None
        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def getInputImage(self):
        return self.input_img

    def recording(self,rec):
        self.rec=rec
        self.out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 30.0, (self.input_img.size))

    def stopRec(self,rec):
        self.out.release()
        self.rec=rec

    def process_one(self):
        if not self.to_process:
            return

        # input is an ascii string. 
        self.input_str = self.to_process.pop() # c'era uno 0 dentro pop

        # convert it to a pil image
        self.input_img = base64_to_pil_image(self.input_str)


        if  self.input_img != None:
            b,g,r = cv2.split(np.asarray(self.input_img))
            self.result=self.context.doAlgorithm(cv2.merge([r,g,b]))

        # salvataggio video
        if self.rec:
            b,g,r = cv2.split(np.asarray(self.input_img))
            self.out.write(cv2.merge([r,g,b]))
            print("Sto Salvando Frame")



    def keep_processing(self):
        # questa sleep evita che si matchi prima che i descriptor vengono
        while True:
            # sleep(5) #forse risolto
            self.process_one()
            sleep(0.01)


    # QUANDO I FRAME IN DA PROCESSARE ARRIVA A 3 SVUOTIAMO
    def enqueue_input(self, input):
        # print("LA CODA E' :",len(self.to_process))
        if self.to_process.__sizeof__()>=2:
           self.to_process.clear()
        self.to_process.appendleft(input)

    #3
    def get_frame(self):
        while not self.to_output:
            # print("Buonanotte")
            sleep(0.05)

        print("qua")
        # cv2.imwrite("frame3.png",self.to_output.pop())
        return self.to_output.pop()  # c'era uno 0 dentro pop

    def get_result(self):
        return self.result