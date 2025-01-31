import numpy as np
import matplotlib.pyplot as plt
import textwrap
from sort_data_related_to_ocr_books_scores import books_name, kraken_scores, paddleocr_scores, tesseract_scores

def generate_ocr_books_scores_comparison_chart(books_name, kraken_scores, paddleocr_scores, tesseract_scores):
    print("Generating OCR Accuracy Scores by Book and Framework Chart...")

    plt.figure("OCR Accuracy Scores by Book and Framework", figsize=(10, len(books_name) * 0.5))

    bars_width = 0.25
    y_positions = np.arange(len(books_name))

    plt.barh(y_positions - bars_width, kraken_scores, color='#4198D7', height=bars_width, label='Kraken')
    plt.barh(y_positions, paddleocr_scores, color='#46D39A', height=bars_width, label='PaddleOCR')
    plt.barh(y_positions + bars_width, tesseract_scores, color='#E55759', height=bars_width, label='Tesseract')

    plt.xlabel('OCR Accuracy Scores', fontsize=15)
    plt.ylabel('Books', fontsize=15)
    plt.yticks(y_positions, books_name, fontsize=10)
    plt.title("OCR Accuracy Scores by Book and Framework", fontsize=16)
    plt.legend(title="OCR Frameworks")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.subplots_adjust(left=0.35)
    plt.show()

generate_ocr_books_scores_comparison_chart(books_name, kraken_scores, paddleocr_scores, tesseract_scores)
