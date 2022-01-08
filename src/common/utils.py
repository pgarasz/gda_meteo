class Config:
    """Class for loading config from json files"""

    api_key = ''
    db_url = ''
    plotly_theme = ''

    def __init__(self, path: str):
        """Load config from json file to instance attributes"""

        import json

        with open(path) as f:
            dict = json.load(f)

        for k, v in dict.items():
            setattr(self, k, v)

    def __repr__(self):

        params = ', '.join(
            [f'{k}={v}' for k, v in self.__dict__.items()])

        return f'Config({params})'


def sanitize_date(value: str) -> tuple[int, int, int]:
    """Return a tuple (year, month, day) from a date provided as string '2019-06-30'."""

    import re

    value = str(value)
    match = re.findall(r'\d+', value)

    if len(match) == 1 and len(match[0]) >= 8:
        year = int(match[0][:4])
        month = int(match[0][4:6])
        day = int(match[0][6:8])
    elif len(match) >= 3:
        year, month, day, *_ = (int(s) for s in match)
    else:
        raise ValueError('Incorrect date format')

    return (year, month, day)


def dates_generator(start: str, end: str):
    """Yield dates in ISO format."""

    import datetime

    start_date = datetime.date(*sanitize_date(start))
    end_date = datetime.date(*sanitize_date(end))

    for n in range(0, (end_date - start_date).days):

        delta = datetime.timedelta(days=n)
        yield (start_date + delta).isoformat()

    yield (end_date).isoformat()


def print_start_info(code, start_date, end_date):
    print(f"""
DOWNLOADING DATA
    outpost: {code}
       from: {start_date}
         to: {end_date}
            """)
