import re


def get_title(file_content):
    title_pattern = re.compile(r'\\title\{([^\}]+)\}')    
    # Extract title and abstract
    title = re.search(title_pattern, file_content)
    title_text = title.group(1) if title else 'test'
    return title_text