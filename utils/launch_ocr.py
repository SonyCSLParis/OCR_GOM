from paddleocr import PaddleOCR,draw_ocr
from os.path import isfile, join
from os import listdir
from PIL import Image
import pytesseract
import subprocess
import time

def ocr_paddle(image_path, result_path):
   ocr = PaddleOCR(use_angle_cls=True, lang='fr')
   result = ocr.ocr(image_path, cls=True)
   file = open(result_path, 'w')

   for idx in range(len(result)):
     res = result[idx]
     if (res):
       for index, line in enumerate(res):
         txts = line[1][0]
         file.write(txts)
         if (index < len(res) - 1):
            file.write(' ')

def ocr_tesseract(image_path, result_path):
   txts = pytesseract.image_to_string(Image.open(image_path), lang='fra')
   if (txts):
    file = open(result_path, 'w')
    file.write(txts)

def ocr_kraken(image_path, result_path):
   subprocess.run(["kraken","-d", "cuda:0", "-i", im, res, "segment", "-bl", "ocr", "-m", "catmus-print-fondue-large.mlmodel"])

def file_is_in_range(img_path):
    for index in range(10):
            img_until_page_30 = "00" + str(index + 30) + ".png"
            if (img_until_page_30 in img_path):
                return True
    return False

def call_ocr_on_book(image_paths, images_folder_path, txt_folder_path, run_ocr):
   for image_path in image_paths:
      txt_path = image_path.replace('png', 'txt')
      final_img_path = images_folder_path + image_path
      final_txt_path = txt_folder_path + txt_path
      if (file_is_in_range(final_img_path) == True):
        run_ocr(final_img_path, final_txt_path)

def call_ocr_on_books(img_folder_path, txt_folder_path, ocr):
   corpus_img_folders = [f for f in listdir(img_folder_path)]
   corpus_img_folders.sort()
   for corpus_img_folder in corpus_img_folders:
       final_img_folder = img_folder_path + corpus_img_folder + '/'
       final_txt_folder = txt_folder_path + corpus_img_folder + '/'
       image_paths = [f for f in listdir(final_img_folder) if isfile(join(final_img_folder, f))]
       image_paths.sort()
       call_ocr_on_book(image_paths, final_img_folder, final_txt_folder, ocr)

def print_execution_time(start, ocr):
   end = time.time()
   time_elapsed = end - start
   print("time elapsed for", ocr,":", time_elapsed, "seconds.")

img_folder_path = "./data/corpus/corpus_img/"
kraken_page_by_page_result_folder_path = "data/results/page_by_page/kraken_results_txt/"
paddleocr_page_by_page_result_folder_path = "data/results/page_by_page/paddleocr_results_txt/"
tesseract_page_by_page_result_folder_path = "data/results/page_by_page/tesseract_results_txt/"

call_ocr_on_books(img_folder_path, paddleocr_page_by_page_result_folder_path, ocr_paddle)
