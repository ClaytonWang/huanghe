# {b'gpus': b'8'} -> {'gpus': 8}
def bytes_dict_to_str_dict(d: dict):
    return {
        key.decode('utf-8'): d.get(key).decode('utf-8')
        if isinstance(d.get(key), int)
        else int(d.get(key).decode('utf-8'))
        for key in d.keys()
    }
