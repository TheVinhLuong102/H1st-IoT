import re


MAX_CHAR_LEN = 255


_JSON_FMT = 'json'
_JSON_EXT = '.{}'.format(_JSON_FMT)

_PARQUET_FMT = 'parquet'
_PARQUET_EXT = '.{}'.format(_PARQUET_FMT)

_YAML_FMT = 'yaml'
_YAML_EXT = '.{}'.format(_YAML_FMT)


def _clean_str(s):
    return re.sub('_{2,}', '_', re.sub('[^\w]+', '_', s).strip('_'))


def clean_lower_str(s):
    return _clean_str(s).lower()


def clean_upper_str(s):
    return _clean_str(s).upper()


def missing_date_strs(among_dates):
    import pandas

    return {str(date)
            for date in
            pandas.date_range(
                start=min(among_dates),
                end=max(among_dates),
                periods=None,
                freq='D',
                tz=None,
                normalize=False,
                name=None,
                closed=None).date} \
        .difference(
            str(date)
            for date in among_dates)
