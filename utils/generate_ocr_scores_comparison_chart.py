import numpy as np
import matplotlib.pyplot as plt
import textwrap
from compare_ocr import kraken_scores, paddleocr_scores, tesseract_scores, expected_result_subfolders

def retrieve_books_name(folders_name):
    books_name = []
    for subfolder in folders_name:
        books_name.append(subfolder.replace('_', ' '))
    return books_name

def generate_ocr_scores_comparison_chart(kraken_scores, paddleocr_scores, tesseract_scores, books_name):
    print("generating ocr comparison scores chart...")

    bars_width = 0.25
    kraken_bar_x_pos = np.arange(len(kraken_scores))
    paddleocr_bar_x_pos = np.arange(len(paddleocr_scores)) + (bars_width * 1)
    tesseract_bar_x_pos = np.arange(len(tesseract_scores)) + (bars_width * 2)

    plt.bar(kraken_bar_x_pos, kraken_scores, color ='#4198D7', width = bars_width, label ='Kraken')
    plt.bar(paddleocr_bar_x_pos, paddleocr_scores, color ='#46D39A', width = bars_width, label ='PaddleOCR')
    plt.bar(tesseract_bar_x_pos, tesseract_scores, color ='#E55759', width = bars_width, label ='Tesseract')

    plt.xlabel('books', fontsize = 15)
    plt.ylabel('scores', fontsize = 15)
    plt.xticks(kraken_bar_x_pos, books_name, rotation='vertical', fontsize=10, ha='right', wrap=True)
    plt.subplots_adjust(0.03, 0.27, 0.99, 0.99)

    plt.legend()
    plt.show()

books_name = retrieve_books_name(expected_result_subfolders)
generate_ocr_scores_comparison_chart(kraken_scores, paddleocr_scores, tesseract_scores, books_name)
