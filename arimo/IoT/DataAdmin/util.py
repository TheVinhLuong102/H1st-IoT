import re


def clean_lower_str(s):
    return re.sub('[^\w]', '_', s).strip('_').lower()
