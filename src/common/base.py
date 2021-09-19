import requests


ALLOWED_METEO_PARAMS = [
    'rain',
    'water',
    'flow',
    'winddir',
    'windlevel',
    'temp',
    'pressure',
    'humidity',
    'sun',
]


class RestAPIerror(Exception):
    pass


class GdaMeteoBase:
    """Base class for connecting to gdanskiewody.pl REST API"""

    _url = 'https://pomiary.gdanskiewody.pl/rest'
    _header = {"Authorization": 'Bearer '}

    def _validate_response(self, response) -> None:
        if response.ok is False:
            raise ConnectionError(
                f'{response.reason} code: {response.status_code}')

    def _validate_api_json(self, json) -> None:
        if json['status'] != "success":
            raise RestAPIerror(json.get('message',
                               'error message not provided by API'))

    def _get_meteo_data(self, meteo_param: str, date: str,
                        outpost_code: int) -> list[list[str, float]]:
        """Query API for meteo data

        Args:
            meteo_param (str): eg. 'temp', 'winddir',
                               see ALLOWED_METEO_PARAMS for more
            date (str): date in isoformat (starting 2016-08-06)
            outpost_code (int): call get_outposts_list() to see avialable codes
        """

        response = requests.get(
            f'{self._url}/measurements/{outpost_code}/{meteo_param}/{date}',
            headers=self._header)

        self._validate_response(response)
        json = response.json()
        self._validate_api_json(json)

        return json['data']

    def get_outposts_list(self):
        """Return outposts list from gdanskiewody.pl API"""

        response = requests.get(f'{self._url}/stations',
                                headers=self._header)

        self._validate_response(response)
        json = response.json()
        self._validate_api_json(json)

        return json['data']

    def print_meteo_outposts(self):
        """Print info about all outposts that gather meteo data."""

        for op in self.get_outposts_list():
            if op['active'] is True and op['temp'] is True:

                print(
                    f"{op.pop('no')}, {op.pop('name')} pomiary:"
                    + str([f'{p}: {v}' for p, v in op.items()
                           if p != 'active']))


class GdaMeteo(GdaMeteoBase):
    """Class for getting hourly values of meteo parameters from gdanskiewody.pl

    Use get methods to query API for meteo data.

    Get methods args:
        date (str): iso format, starting from '2016-08-06'
        outpost_code (int): call get_outposts_lsit to see available codes

    Returns:
        list of 24 lists with datetime and parameter value
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, val):
        self._api_key = val
        self._header.update(Authorization=self._header["Authorization"] + val)

    def get_rain(self, date: str, outpost_code: int):
        return self._get_meteo_data('rain', date, outpost_code)

    def get_winddir(self, date: str, outpost_code: int):
        return self._get_meteo_data('winddir', date, outpost_code)

    def get_windspeed(self, date: str, outpost_code: int):
        return self._get_meteo_data('windlevel', date, outpost_code)

    def get_temperature(self, date: str, outpost_code: int):
        return self._get_meteo_data('temp', date, outpost_code)

    def get_pressure(self, date: str, outpost_code: int):
        return self._get_meteo_data('pressure', date, outpost_code)

    def get_humidity(self, date: str, outpost_code: int):
        return self._get_meteo_data('humidity', date, outpost_code)

    def get_sun(self, date: str, outpost_code: int):
        return self._get_meteo_data('sun', date, outpost_code)
