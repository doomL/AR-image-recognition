from PIL import Image
from io import BytesIO
import numpy as np
import base64
import glob
import cv2

def pil_image_to_base64(pil_image):
    buf = BytesIO()
    pil_image.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue())

def base64_to_pil_image(base64_img):
    return Image.open(BytesIO(base64.b64decode(base64_img)))


# REMEBER CALC FEATURE 
def findPoints( img):
    detector = cv2.xfeatures2d_SURF.create(hessianThreshold=200)
    keypointsImg, descriptorsImg = detector.detectAndCompute(
        toRGB(stringToImage(img)), None)
    #print(keypointsImg)

    # Take in base64 string and return PIL image
def stringToImage(base64_string):
    #base64_string += "=" * ((4 - len(base64_string) % 4) % 4)  # ugh
    imgdata = base64.b64decode(base64_string)
    return Image.open(BytesIO(imgdata))

# convert PIL Image to an RGB image( technically a numpy array ) that's compatible with opencv
def toRGB(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

# class loadImg:
#     def __init__(self):
#         self.imgArray = [cv2.imread(file) for file in glob.glob("images/dataset/*.jpg")]
#         # print(len(self.imgArray), "la lunghezza dell'array")
#         self.imgData = cv2.imread('images/maintenance.jpg', -1)

#         if self.imgArray is None:
#             print('Could not open or find the images!')




class loadImg:

    # def __init__(self,mysql,session):
        
    #     selectImageQuery="SELECT id,base64 FROM images WHERE azienda = %s" 
        
    #     cur = mysql.connection.cursor()
        
    #     cur.execute(selectImageQuery,(session["azienda"],))

    #     dbImages=cur.fetchall()

    #     self.id_Images = {} # array associativo tra id e base64 dal DB
    #     for singleImage in dbImages:
    #         self.id_Images[singleImage[0]] =  toRGB(stringToImage(singleImage[1]))

    def __init__(self,db,session,Images):
        
        dbImages = db.session.query(Images).filter_by(azienda=session["azienda"]).all()

        self.id_Images = {} # array associativo tra id e base64 dal DB
        for singleImage in dbImages:
            self.id_Images[singleImage.id] =  toRGB(stringToImage(singleImage.base64))

    