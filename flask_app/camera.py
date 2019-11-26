import threading
import binascii
import cv2
from time import sleep
from utils import base64_to_pil_image, pil_image_to_base64
from VideoSave import VideoSave

class Camera:
    def __init__(self, context):
        self.to_process = []
        self.to_output = []
        self.context = context
<<<<<<< HEAD
        self.input_img = None
        self.out= None
        self.rec=False
=======

        self.videoSave = VideoSave() 

>>>>>>> 6c24fa8f140b93dd477b7d8dbb992fb04cc2c4f9
        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def getInputImage(self):
        return self.input_img

    def recording(self,rec):
        self.rec=rec
        self.out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (self.input_img.size))

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
<<<<<<< HEAD
        if self.rec:
            self.out.write(np.asarray(self.input_img))
=======

            # se l'immagine non è None utilizzo save video per salvarmi 
            # lo stream video.
            self.videoSave.saveFrame(self.input_img)
        
>>>>>>> 6c24fa8f140b93dd477b7d8dbb992fb04cc2c4f9
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
