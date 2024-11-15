from generate_ocr_books_scores import kraken_scores, paddleocr_scores, tesseract_scores, expected_result_subfolders

def retrieve_books_name(folders_name):
    books_name = []
    for subfolder in folders_name:
        books_name.append(subfolder.replace('_', ' '))
    return books_name

def sort_data_related_to_ocr_books_scores(books_name, kraken_scores, paddleocr_scores, tesseract_scores):
    books_scores = []
    for index in range(len(books_name)):
        books_scores.append((books_name[index], kraken_scores[index], paddleocr_scores[index], tesseract_scores[index]))
    books_scores.sort(key=lambda x:x[1],reverse=True)
    books_names = list((row[0] for row in books_scores))
    kraken_scores = list((row[1] for row in books_scores))
    paddleocr_scores = list((row[2] for row in books_scores))
    tesseract_scores = list((row[3] for row in books_scores))
    return books_name, kraken_scores, paddleocr_scores, tesseract_scores

books_name = retrieve_books_name(expected_result_subfolders)
books_name, kraken_scores, paddleocr_scores, tesseract_scores = sort_data_related_to_ocr_books_scores(books_name, kraken_scores, paddleocr_scores, tesseract_scores)
