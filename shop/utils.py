from typing import Dict, Union


def snake_to_camel(s):
    words = s.split('_')
    return words[0] + ''.join(x.title() for x in words[1:])


def snake_to_camel_in_dict(
        data: Dict[str, Union[str, int]]) -> Dict[str, Union[str, int]]:
    new_data = {}
    for k, v in data.items():
        if type(v) == dict:
            data[k] = snake_to_camel_in_dict(v)
        elif type(v) == list:
            for i, item in enumerate(v):
                if type(item) == dict:
                    data[k][i] = snake_to_camel_in_dict(item)
        new_data[snake_to_camel(k)] = data[k]

    return new_data
