from os import listdir
from Bio import Align
from typing import List
from difflib import SequenceMatcher, HtmlDiff
from utils import get_file_content

def put_folder_content_in_list(folder_path, subfolders):
    content_list = []
    for subfolder in subfolders:
        file_to_read = folder_path + subfolder + '/' + subfolder + ".txt"
        content_list.append(get_file_content(file_to_read))
    return content_list

def generate_difflib_html_files_name(ocr_name, book_names):
    html_files_names = []
    for book_name in book_names:
        html_files_names.append(ocr_name + "/" + book_name + ".html")
    return html_files_names

def generate_pairwise_score(target_content, query_content):
    aligner = Align.PairwiseAligner(match_score=1.0, mismatch_score=-5.0, gap_score=-0.5)
    score = aligner.score(target_content, query_content)
    score_ratio = score / len(target_content)
    return score_ratio

def generate_difflib_score(target_content, query_content):
    seq_match = SequenceMatcher(None, target_content, query_content)
    score_ratio = seq_match.ratio()
    print("similarity score:", score_ratio, "out of 1.0.")
    return score_ratio

def generate_difflib_html_report(target_content, query_content, html_file_name):
    html_diff = HtmlDiff().make_file(target_content.splitlines(), query_content.splitlines())
    with open(html_file_name, "w", encoding="utf-8") as f:
        f.write(html_diff)

def generate_list_pairwise_score(expected_result_list, ocr_result_list, ocr_name):
    scores = []
    if len(expected_result_list) != len(ocr_result_list):
        return
    print("generating scores for " + ocr_name + "...")
    lists_len = len(expected_result_list)
    for i in range (lists_len):
        scores.append(generate_pairwise_score(expected_result_list[i], ocr_result_list[i]))
    return scores

def generate_list_difflib_score(expected_result_list, ocr_result_list, ocr_name):
    if len(expected_result_list) != len(ocr_result_list):
        return
    lists_len = len(expected_result_list)
    total_score_ratios = 0
    for i in range (lists_len):
        total_score_ratios += generate_difflib_score(expected_result_list[i], ocr_result_list[i])
    print(ocr_name, "similarity score:", total_score_ratios/lists_len, "out of 1.0.")

def generate_list_difflib_html_report(expected_result_list, ocr_result_list, html_files_name_list):
    if len(expected_result_list) != len(ocr_result_list):
        return
    lists_len = len(expected_result_list)
    for i in range (lists_len):
        generate_difflib_html_report(expected_result_list[i], ocr_result_list[i], html_files_name_list[i])

expected_result_folder_path = "data/results/pages_concatenate/expected_results_txt/"
kraken_result_folder_path = "data/results/pages_concatenate/kraken_results_txt/"
paddleocr_result_folder_path = "data/results/pages_concatenate/paddleocr_results_txt/"
tesseract_result_folder_path = "data/results/pages_concatenate/tesseract_results_txt/"

expected_result_subfolders = [f for f in listdir(expected_result_folder_path)]
kraken_result_subfolders = [f for f in listdir(kraken_result_folder_path)]
paddleocr_result_subfolders = [f for f in listdir(paddleocr_result_folder_path)]
tesseract_result_subfolders = [f for f in listdir(tesseract_result_folder_path)]

expected_result_list = put_folder_content_in_list(expected_result_folder_path, expected_result_subfolders)
kraken_result_list = put_folder_content_in_list(kraken_result_folder_path, kraken_result_subfolders)
paddleocr_result_list = put_folder_content_in_list(paddleocr_result_folder_path, paddleocr_result_subfolders)
tesseract_result_list = put_folder_content_in_list(tesseract_result_folder_path, tesseract_result_subfolders)

# kraken_html_files_name_list = generate_difflib_html_files_name("kraken", expected_result_subfolders)
# paddleocr_html_files_name_list = generate_difflib_html_files_name("paddleocr", expected_result_subfolders)
# tesseract_html_files_name_list = generate_difflib_html_files_name("tesseract", expected_result_subfolders)

# generate_list_difflib_html_report(expected_result_list, kraken_result_list, kraken_html_files_name_list)
# generate_list_difflib_html_report(expected_result_list, paddleocr_result_list, paddleocr_html_files_name_list)
# generate_list_difflib_html_report(expected_result_list, tesseract_result_list, tesseract_html_files_name_list)

# generate_list_difflib_score(expected_result_list, kraken_result_list, "kraken")
# generate_list_difflib_score(expected_result_list, paddleocr_result_list, "paddleocr")
# generate_list_difflib_score(expected_result_list, tesseract_result_list, "tesseract")

kraken_scores = generate_list_pairwise_score(expected_result_list, kraken_result_list, "kraken")
paddleocr_scores = generate_list_pairwise_score(expected_result_list, paddleocr_result_list, "paddleocr")
tesseract_scores = generate_list_pairwise_score(expected_result_list, tesseract_result_list, "tesseract")
