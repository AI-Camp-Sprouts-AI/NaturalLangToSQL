import re


def filename_to_tablename(filename):
    name = re.sub(r'(^\./|\.py$)', '', filename)
    return name
    # return ''.join(word.capitalize() for word in name.split('_'))
