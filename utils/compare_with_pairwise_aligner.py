from os import listdir
from Bio import Align
from typing import List

def get_file_content(file_path):
    file = open(file_path, 'r')
    content = file.read()
    return content

def get_pairwise_score(target_content, query_content):
    aligner = Align.PairwiseAligner(match_score=1.0, mismatch_score=-5.0, gap_score=-0.5)
    score = aligner.score(target_content, query_content)
    score_ratio = score / len(target_content)
    print("similarity score:", score_ratio, "out of 1.0.")
    return score_ratio

def put_folder_content_in_list(folder_path, subfolders):
    content_list = []
    for subfolder in subfolders:
        file_to_read = folder_path + subfolder + '/' + subfolder + ".txt"
        content_list.append(get_file_content(file_to_read))
    return content_list

def get_list_pairwise_scores(expected_result_list, ocr_result_list, ocr_name):
    if len(expected_result_list) != len(ocr_result_list):
        return
    lists_len = len(expected_result_list)
    total_score_ratios = 0
    for i in range (lists_len):
        total_score_ratios += get_pairwise_score(expected_result_list[i], ocr_result_list[i])
    print(ocr_name, "similarity score:", total_score_ratios/lists_len, "out of 1.0.")

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

get_list_pairwise_scores(expected_result_list, kraken_result_list, "kraken")
get_list_pairwise_scores(expected_result_list, paddleocr_result_list, "paddleocr")
get_list_pairwise_scores(expected_result_list, tesseract_result_list, "tesseract")
