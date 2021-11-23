"""H1st IoT Data Management Utilities."""


import re
import sys

if sys.version_info >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence


__all__: Sequence[str] = (
    'MAX_CHAR_LEN',
    '_JSON_FMT', '_JSON_EXT',
    '_PARQUET_FMT', '_PARQUET_EXT',
    'clean_lower_str', 'clean_upper_str',
)


MAX_CHAR_LEN = 255


_JSON_FMT = 'json'
_JSON_EXT = f'.{_JSON_FMT}'

_PARQUET_FMT = 'parquet'
_PARQUET_EXT = f'.{_PARQUET_FMT}'


# pylint: disable=invalid-name


def _clean_str(s: str) -> str:
    return re.sub('_{2,}', '_', re.sub(r'[^\w]+', '_', s).strip('_'))


def clean_lower_str(s: str) -> str:
    """Clean & lower-case a string."""
    return _clean_str(s).lower()


def clean_upper_str(s: str) -> str:
    """Clean & upper-case a string."""
    return _clean_str(s).upper()
