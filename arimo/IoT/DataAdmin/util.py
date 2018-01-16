import re


def clean_lower_str(s):
    return re.sub('[^\w]+', '_', s).strip('_').lower()


def _clean_upper_str(s):
    return clean_lower_str(s).replace('_', '-').upper()
