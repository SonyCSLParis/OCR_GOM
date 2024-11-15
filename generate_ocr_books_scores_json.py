import json
from utils import write_content_in_file
from sort_data_related_to_ocr_books_scores import books_name, kraken_scores, paddleocr_scores, tesseract_scores

def generate_ocr_books_scores_json(books_name, kraken_scores, paddleocr_scores, tesseract_scores):
    print("generating ocr books scores json...")
    ocr_books_scores_json = []
    for index in range(len(books_name)):
        ocr_book_scores_json = {
        "book_name": books_name[index],
        "scores":[{"ocr_name": "kraken", "score": kraken_scores[index]},
            {"ocr_name": "paddleocr", "score": paddleocr_scores[index]},
            {"ocr_name": "tesseract", "score": tesseract_scores[index]}]
        }
        ocr_books_scores_json.append(ocr_book_scores_json)
    return json.dumps(ocr_books_scores_json, ensure_ascii=False, indent=4)

ocr_books_scores_json = generate_ocr_books_scores_json(books_name, kraken_scores, paddleocr_scores, tesseract_scores)
write_content_in_file("data/results/ocr_scores/ocr_books_scores.json", ocr_books_scores_json)
