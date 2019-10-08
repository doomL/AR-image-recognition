import threading
import binascii
from time import sleep
from utils import base64_to_pil_image, pil_image_to_base64

class Camera:
    def __init__(self, context):
        self.to_process = []
        self.to_output = []
        self.context = context

        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

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
        # print(self.output_img)
        # output_str is a base64 string in ascii
        # self.output_str = pil_image_to_base64(self.output_img)
        # convert eh base64 string in ascii to base64 string in _bytes_
        # self.to_output.append(binascii.a2b_base64(self.output_str))

        
    def keep_processing(self):
        while True:
            self.process_one()
            sleep(0.01)

    def enqueue_input(self, input):
        if self.to_process.__sizeof__()>=3:
            self.to_process.clear()
        self.to_process.append(input)

    def get_frame(self):
        while not self.to_output:
            sleep(0.05)
        return self.to_output.pop(0)

    def __del__(self):
        self.context.__del__()
