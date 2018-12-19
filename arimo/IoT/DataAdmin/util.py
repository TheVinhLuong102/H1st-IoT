import re


MAX_CHAR_LEN = 255


_JSON_FMT = 'json'
_JSON_EXT = '.{}'.format(_JSON_FMT)

_PARQUET_FMT = 'parquet'
_PARQUET_EXT = '.{}'.format(_PARQUET_FMT)

_YAML_FMT = 'yaml'
_YAML_EXT = '.{}'.format(_YAML_FMT)


def _clean_str(s):
    return re.sub('[^\w]+', '_', s).strip('_')


def clean_lower_str(s):
    return _clean_str(s).lower()


def clean_upper_str(s):
    return _clean_str(s).upper()
