from heic2png import HEIC2PNG
import os
import cv2

def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

def convertHEICtopng(directory):
    k = 0
    for i in os.listdir(directory):
        print(i)
        heic_img = HEIC2PNG(os.path.join(directory,i))
        heic_img.save(os.path.join(directory, str(k)+".png"))
        k+= 1

def YOLOresize(directory):
    for i in os.listdir(directory):
        print(i)
        img = cv2.imread(os.path.join(directory,i), cv2.IMREAD_UNCHANGED)
        resize_image = cv2.resize(img, (416,416), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(os.path.join(directory, str(k)+".png"), resize_image)
        k+= 1
