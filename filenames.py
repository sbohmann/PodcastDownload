def clean_filename(name):
    result = []
    for char in name:
        if 'A' <= char <= 'Z' or 'a' <= char <= 'z' or '0' <= char <= '9':
            result.append(char)
        elif ord(char) > 128:
            result.append(char)
        else:
            result.append('_')
    return ''.join(result)