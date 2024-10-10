from paddleocr import PaddleOCR,draw_ocr
from PIL import Image
import pytesseract
import subprocess


def ocr_paddle(im="test.jpg", res="result.jpg"):
   ocr = PaddleOCR(use_angle_cls=True, lang='fr')
   im = "../data/images/0012.jpg"
   result = ocr.ocr(im, cls=True)

   for idx in range(len(result)):
     res = result[idx]
     for line in res:
        print(line)

   from PIL import Image
   result = result[0]
   image = Image.open(img_path).convert('RGB')
   boxes = [line[0] for line in result]
   txts = [line[1][0] for line in result]
   scores = [line[1][1] for line in result]
   im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
   im_show = Image.fromarray(im_show)
   im_show.save('result.jpg')

def ocr_tesseract(im):
    pass

def ocr_kraken(im="test.jpg", res="result.txt"):
   subprocess.run(["kraken","-d", "cuda:0", "-i", im, res, "segment", "-bl", "ocr", "-m", "catmus-print-fondue-large.mlmodel"])

