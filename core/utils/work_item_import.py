def get_parent_index(index_code):
    if '.' not in index_code:
        return None
    return '.'.join(index_code.split('.')[:-1])
