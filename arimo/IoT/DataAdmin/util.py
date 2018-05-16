import re


MAX_CHAR_LEN = 255


_JSON_FMT = 'json'
_JSON_EXT = '.{}'.format(_JSON_FMT)

_PARQUET_FMT = 'parquet'
_PARQUET_EXT = '.{}'.format(_PARQUET_FMT)

_YAML_FMT = 'yaml'
_YAML_EXT = '.{}'.format(_YAML_FMT)


def clean_lower_str(s):
    return re.sub('[^\w]+', '_', s).strip('_').lower()


def _clean_upper_str(s):
    return clean_lower_str(s).replace('_', '-').upper()
