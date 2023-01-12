from detection.cv2ObjectDetection import extractTextBoxes
from detection.ocr import ocr_dump_folder
from utils.acumaticaUtils import AcumaticaDapper

if __name__ == "__main__":
    extractTextBoxes('image.png')
    output = ocr_dump_folder()
    for strOut in output:
        try:
            stock = AcumaticaDapper().createSQLStockItems(strOut)
        except Exception as e:
            print(f"Could not create item: {e}")
