import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import glob

videoCapture = cv.VideoCapture(0)

img1 = cv.imread('succo.jpg',0) # immagine da cercare
# img2 = cv.imread('2.jpg',0)

# la uso dopo prima provo con un'immagine sola e il flusso video
# imgArray = [cv.imread(file) for file in glob.glob("*.jpg")]
# print(len(imgArray))


# orb = cv.ORB_create(500)
orb = cv.ORB_create(nfeatures=1200, scoreType=cv.ORB_FAST_SCORE)

kp1, des1 = orb.detectAndCompute(img1,None)
# kp2, des2 = orb.detectAndCompute(img2,None)

bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

c = 0
exit = False
while videoCapture.isOpened() and not exit:
    ret, frame = videoCapture.read()
    kpFrame, desFrame = orb.detectAndCompute(frame, None)

    matches = bf.match(des1,desFrame)
    matches = sorted(matches, key = lambda x:x.distance)
    gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

    img_matches = np.empty((max(img1.shape[0],gray.shape[0]), img1.shape[1]+gray.shape[1], 3), dtype=np.uint8)
    cv.drawMatches(img1,kp1 , gray, kpFrame, matches[:20], img_matches, flags=2)

    print(len(matches))

    if len(matches)>=510:
        print("Trovata una corrispondenza con immagine ")

    cv.waitKey(1)
    cv.imshow('View',img_matches)

    if cv.waitKey(1) == 27:
        exit = True
        print("exit premuto")

if exit:
    videoCapture.release()
    cv.destroyAllWindows()
    

# img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:10],None, flags=2)
# plt.imshow(img3)
# plt.show()
