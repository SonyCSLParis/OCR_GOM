def get_file_content(file_path):
    file = open(file_path, 'r')
    content = file.read()
    return content

def write_content_in_file(file_path, content):
    file = open(file_path, 'a')
    file.write(content)