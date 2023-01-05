from heic2png import HEIC2PNG
import os
import cv2

def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))
            
if __name__ == '__main__':
    k = 0

    # imageFolder = "./groceriesDatasetRaw/"
    # k = 0
    # for i in os.listdir(imageFolder):
    #     print(i)
    #     heic_img = HEIC2PNG(os.path.join(imageFolder,i))
    #     heic_img.save(os.path.join(imageFolder, str(k))) # it'll show as `test.png`
    #     k+= 1

    imageFolder = "./416/"
    for i in os.listdir(imageFolder):
        print(i)
        img = cv2.imread(os.path.join(imageFolder,i), cv2.IMREAD_UNCHANGED)
        resize_image = cv2.resize(img, (416,416), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(os.path.join(imageFolder, str(k)+".png"), resize_image)
        k+= 1