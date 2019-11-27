import threading
import binascii
import cv2
from time import sleep
from utils import base64_to_pil_image, pil_image_to_base64
import numpy as np
#from VideoSave import VideoSave

class Camera:
    def __init__(self, context):
        self.to_process = []
        self.to_output = []
        self.context = context
        self.input_img = None
        self.out= None
        self.rec=False
        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def getInputImage(self):
        return self.input_img

    def recording(self,rec):
        self.rec=rec
        self.out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 20.0, (self.input_img.size))
        cv2.imwrite("img.jpg", np.asarray(self.input_img))

    def stopRec(self,rec):
        self.out.release()
        self.rec=rec

    def process_one(self):
        if not self.to_process:
            return
        # input is an ascii string. 
        self.input_str = self.to_process.pop(0)
        # convert it to a pil image
        self.input_img = base64_to_pil_image(self.input_str)
        ################## where the hard work is done ############
        # output_img is an PIL image
        # self.output_img = self.context.doAlgorithm(self.input_img)
        if  self.input_img != None:
            self.context.doAlgorithm(self.input_img)
        if self.rec:
            self.out.write(np.asarray(self.input_img))
        print("Sto Salvando Frame")
    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.01)


    # QUANDO I FRAME IN DA PROCESSARE ARRIVA A 3 SVUOTIAMO
    def enqueue_input(self, input):
        if self.to_process.__sizeof__()>=3:
            self.to_process.clear()
        self.to_process.append(input)

    def get_frame(self):
        while not self.to_output:
            sleep(0.05)
        return self.to_output.pop(0)
