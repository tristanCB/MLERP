import os
import pprint
pp = pprint.PrettyPrinter(indent=4)
from utils.utils import absoluteFilePaths
import matplotlib.pyplot as plt
import keras_ocr

def ocr_image(path):
    pipeline = keras_ocr.pipeline.Pipeline()
    images = [
        keras_ocr.tools.read(url) for url in [path]
    ]
    prediction_groups = pipeline.recognize(images)
    pp.pprint(prediction_groups)
    
    # Plot the predictions
    fig, axs = plt.plot(nrows=len(images), figsize=(20, 20))
    for ax, image, predictions in zip(axs, images, prediction_groups):
        keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)
    fig.savefig("./ocrTest.png")


def ocr_dump_folder():
    # keras-ocr will automatically download pretrained
    # weights for the detector and recognizer.
    pipeline = keras_ocr.pipeline.Pipeline()

    # Get a set of three example images
    images = [
        keras_ocr.tools.read(url) for url in [i for i in absoluteFilePaths(r"./imageDump")]
    ]

    # Each list of predictions in prediction_groups is a list of
    # (word, box) tuples.

    def orderByXaxisPosition(elem):
        return elem[1][0][0]

    prediction_groups = pipeline.recognize(images)
    pp.pprint(prediction_groups)
    textOutputs = []
    for pred_g in prediction_groups:
        conctText = ''
        pred_g.sort(key=orderByXaxisPosition)
        for pred in pred_g:
            conctText += pred[0]
        pp.pprint(conctText)
        textOutputs.append(conctText)
    
    # Plot the predictions
    fig, axs = plt.subplots(nrows=len(images), figsize=(20, 20))
    for ax, image, predictions in zip(axs, images, prediction_groups):
        keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)
    fig.savefig("./ocrTest.png")
    return textOutputs
