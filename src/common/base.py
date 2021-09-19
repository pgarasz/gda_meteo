import requests

from typing import Any

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

    def _validate_api_json(self, json) -> None:
        if json['status'] != "success":
            raise RestAPIerror(json.get('message',
                               'error message not provided by API'))

    def _validate_response_and_get_data(self, response: requests.Response) -> list[Any]:
        response.raise_for_status()
        json = response.json()
        self._validate_api_json(json)

        return json['data']

    def _get_meteo_data(self, param: str, date: str,
                        outpost_code: int) -> dict[str, dict[str, float]]:
        """Query API for meteo data

        Args:
            param (str): meteo parameter name to get from API, eg. 'rain', 'winddir',
                         see ALLOWED_METEO_PARAMS for more
            date (str): date in isoformat (starting 2016-08-06)
            outpost_code (int): call get_outposts_list() to see available codes

        Returns:
            dict (str: dict[str: float]): 2d dict, each key holds a dict with param_name: value
        """

        response = requests.get(
            f'{self._url}/measurements/{outpost_code}/{param}/{date}',
            headers=self._header)

        raw_data = self._validate_response_and_get_data(response)

        data = {dt: dict.fromkeys([param], val)
                for dt, val in raw_data}

        return data

    def get_outposts_list(self):
        """Return outposts list from gdanskiewody.pl API"""

        response = requests.get(f'{self._url}/stations',
                                headers=self._header)

        return self._validate_response_and_get_data(response)

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
        outpost_code (int): call get_outposts_list to see available codes

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

    def get_meteo_params(self, date: str, outpost_code: int,
                         params: list[str] = ALLOWED_METEO_PARAMS) -> dict[str, dict[str, float]]:

        """Get multiple meteo parameters from one outpost.

        Args:
            date (str): date in isoformat (starting 2016-08-06)
            outpost_code (int): call get_outposts_list() to see available codes
            params (list[str]): list of meteo parameters to get from API, eg. ['rain', 'winddir'],
                                defaults to all ALLOWED_METEO_PARAMS

        Returns:
            dict (str: dict[str: float]): 2d dict, each key holds a dict with param_name: value
        """

        if set(params).difference(set(ALLOWED_METEO_PARAMS)):
            raise ValueError('Incorrect meteo parameter name')

        data = {}

        for param in params:

            result = self._get_meteo_data(param, date, outpost_code)

            for key in result:
                if key not in data:
                    data[key] = result[key]
                else:
                    data[key].update(result[key])

        return data
