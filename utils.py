import json

def get_file_content(file_path):
    file = open(file_path, 'r')
    content = file.read()
    return content

def get_json_file_content(file_path):
    file = open("data/dictionary/morphalouV3.json", 'r')
    content = json.load(file)
    return content

def write_content_in_file(file_path, content, open_mode):
    file = open(file_path, open_mode)
    file.write(content)

def string_contains_digit(string):
    for char in string:
            if char.isdigit():
                    return True
    return False
