from os import listdir

ocr_result_folder_path = "data/results/page_by_page/tesseract_results_txt/"
ocr_concanate_result_folder_path = "data/results/pages_concatenate/tesseract_results_txt/"

ocr_result_subfolders = [f for f in listdir(ocr_result_folder_path)]

def get_file_content(file_path):
    file = open(file_path, 'r')
    content = file.read()
    return content

def write_content_in_file(file_path, content):
    file = open(file_path, 'a')
    file.write(content)

def remove_unwanted_chars(txt_content):
    txt_content = txt_content.replace('\n', ' ')
    txt_content = txt_content.replace("¬ ", '')
    txt_content = txt_content.replace("¬", '-')
    return txt_content

def concatenate_results(ocr_result_subfolders, ocr_result_folder_path, ocr_concanate_result_folder_path):
    for subfolder in ocr_result_subfolders:
        file_to_write = ocr_concanate_result_folder_path + subfolder + '/' + subfolder + ".txt"
        open(file_to_write, "w").close()
        for index in range(10):
            txt_path = "00" + str(index + 30) + ".txt"
            final_txt_path = ocr_result_folder_path + subfolder + '/' + txt_path
            txt_content = get_file_content(final_txt_path)
            # txt_content = remove_unwanted_chars(txt_content)
            write_content_in_file(file_to_write, txt_content)

concatenate_results(ocr_result_subfolders, ocr_result_folder_path, ocr_concanate_result_folder_path)