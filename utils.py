def get_file_content(file_path):
    file = open(file_path, 'r')
    content = file.read()
    return content

def write_content_in_file(file_path, content, open_mode):
    file = open(file_path, open_mode)
    file.write(content)