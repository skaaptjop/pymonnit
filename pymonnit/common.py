from urlparse import urlparse, ParseResult
from posixpath import join
from datetime import datetime
from base64 import b64encode
import ssl

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.auth import AuthBase


from .xml import MonnitXML

class SSLv3Adapter(HTTPAdapter):
    "Transport adaptor for SSL (when it doesn't work normally)"
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_SSLv3)



class MonnitAuth(AuthBase):
    """
    Requests library auth module
    Inserts token to URL path e.g.
      https://www.imonnit.com/xml/SomeMethod/TOKEN?param=value&param=value
    The token is grabbed from the GetAuthToken method on the iMonnit API
    or, alternatively, it is base64 encoded username:password
    """
    def __init__(self, token):
        """
        Constructor takes the iMonnit API auth token
        :param token:
        """
        self._token = token

    def __call__(self, r):
        """Insert the token after the path element of the URL"""
        url = urlparse(r.url)
        new_url = ParseResult(scheme=url.scheme,
                              netloc=url.netloc,
                              path=join(url.path, self._token),
                              params=url.params,
                              query=url.query,
                              fragment=url.fragment)
        r.url = new_url.geturl()
        return r




class MonnitBase(object):
    """
    Base class for iMonnit API classes.
    Provides authentication and resolving API method calls
    """
    def __init__(self, username, password, url = "https://www.imonnit.com/"):
        self.username = username
        self.password = password
        self._monnit_auth = MonnitAuth(self.auth_token)
        self._base_url = join(url, "xml")
        #DateTime format for API requests
        self.datetime_format = '%m/%d/%Y %H:%M:%S %p'


    @property
    def auth_token(self):
        """
        Returns iMonnit auth token string
        The token is based on a hash of the username and password
        """
        return b64encode(self.username + ":" + self.password).rstrip("=")


    def _get_method_url(self, method):
        """
        Build base URL path
        :param method: Name of iMonnit API method. e.g. "Logon" or "SensorList"
        :return: Root URL path. e.g. https://www.imonnit.com/xml/Logon
        """
        "Returns URL for specific method calls"
        return join(self._base_url, method)


    def _call_api(self, method, params = None):
        """
        Makes the iMonnit API call based on the method required and query string
        :param method: API method, e.g. "Logon" or "SensorList"
        :param params: Query string parameters
        :return: requests.Response object
        """
        return requests.get(self._get_method_url(method), params = params, auth = self._monnit_auth)


    def logon(self):
        """
        Test authentication
        :return: True if logon successful, else False
        """
        r = self._call_api("Logon")
        xml = MonnitXML(r.content)
        return xml.is_success_result




class Monnit(MonnitBase):

    def get_sensor_data(self, sensor_id, start, end):
        ret = []
        for i in self.iter_sensor_data(sensor_id, start, end):
            ret.append(i)
        return ret


    def iter_sensor_data(self, sensor_id, start, end):
        params = {"fromDate":start, "toDate":end, "sensorID":sensor_id}
        r = self._call_api("SensorDataMessages", params=params)
        xml = MonnitXML(r.content)

        for msg_data in xml.root.iter("APIDataMessage"):
            dt = datetime.strptime(msg_data.get("MessageDate"), self.datetime_format)
            yield (msg_data.get("PlotValue"), dt)


    def get_sensor_list(self):
        r = requests.get(self._build_url_path("SensorList"), auth = MonnitAuth(self.auth_token))
        return json.loads(r.text)["Result"]



