
from utils import acumaticaUtils
import random
import string

# printing lowercase
def getRandomString(length):
     letters = string.ascii_lowercase
     return ''.join(random.choice(letters) for i in range(length))
     
stock = acumaticaUtils.AcumaticaDapper().createSQLStockItems(getRandomString(8))
print(stock)
exit()
import numpy as np
def orderByXaxisPosition(elem):
     return elem[1][0][0]

Data_output_example = [   (   '514453',
            np.array([[0.,  0.000000e+00],
       [ 1.130000e+02,  0.000000e+00],
       [ 1.130000e+02,  3.000000e+01],
       [ 0.000000e+00,  3.000000e+01]], dtype=np.float32)),
        (   '6622',
            np.array([[112.,   0.],
       [174.,   0.],
       [174.,  29.],
       [112.,  29.]], dtype=np.float32)),
        (   'Coco',
            np.array([[-9.184852e-16,   0.],
       [174.,   0.],
       [174.,  29.],
       [112.,  29.]], dtype=np.float32))]
#print(Data_output_example)


Data_output_example.sort(key=orderByXaxisPosition)
print(Data_output_example)

from detection.ocr import ocr_dump_folder
ocr_dump_folder()
