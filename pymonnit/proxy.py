from posixpath import join
from datetime import datetime
import requests

from .auth import MonnitAuth

DEFAULT_HOST = "https://www.imonnit.com/"



class MonnitProxy(object):
    """
    iMonnit class for working with remote API calls
    """

    _no_auth_methods = ("TimeZones", "SMSCarriers", "GetAuthToken")  #TODO: update this with all methods

    def __init__(self, username, password, host=DEFAULT_HOST):
        """
        Constructor
        :param username: username
        :param password: password
        :param base_url: API base url (excluding "xml" or "json" part)
                         Just the scheme and netloc
        """
        self._host = host
        self._monnit_auth = MonnitAuth(username, password)

    @property
    def datetime_format(self):
        """
        DateTime format for API requests
        :return: format string
        """
        return '%m/%d/%Y %H:%M:%S %p'

    def _build_method_url(self, method):
        """
        Build base URL path for the method API signature
        :param method: Name of iMonnit API method. e.g. "Logon" or "SensorList"
        :return: Root URL path. e.g. https://www.imonnit.com/xml/Logon
        """
        return join(self._host, "xml", method)

    def execute(self, method, params=None):
        """
        Makes the iMonnit API call based on the method required and query string
        :param method: API method, e.g. "Logon" or "SensorList"
        :param params: Query string parameters
        :return: requests.Response object
        """
        if method in self._no_auth_methods:
            response = requests.get(self._build_method_url(method), params=params)
        else:
            response = requests.get(self._build_method_url(method), params=params, auth=self._monnit_auth)
        return response

    def logon(self):
        """
        Test authentication
        :return: True if logon successful, else False
        """
        r = self.execute("Logon")
        xml = MonnitXML(r.content)
        return xml.is_success_result






# class Monnit(MonnitBase):
#
#     def get_sensor_data(self, sensor_id, start, end):
#         ret = []
#         for i in self.iter_sensor_data(sensor_id, start, end):
#             ret.append(i)
#         return ret
#
#
#     def iter_sensor_data(self, sensor_id, start, end):
#         params = {"fromDate":start, "toDate":end, "sensorID":sensor_id}
#         r = self._call_api("SensorDataMessages", params=params)
#         xml = MonnitXML(r.content)
#
#         for msg_data in xml.root.iter("APIDataMessage"):
#             dt = datetime.strptime(msg_data.get("MessageDate"), self.datetime_format)
#             yield (msg_data.get("PlotValue"), dt)
#
#
#
#
#
