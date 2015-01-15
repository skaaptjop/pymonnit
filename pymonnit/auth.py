from urlparse import urlparse, ParseResult
from posixpath import join
from base64 import b64encode
from requests.auth import AuthBase


class MonnitAuth(AuthBase):
    """
    iMonnit auth class for requests library
    Appends token to URL path before query string
    e.g. https://www.imonnit.com/xml/SomeMethod/TOKEN?param=value&param=value
    """
    def __init__(self, username, password):
        """
        Constructor takes the iMonnit API auth token
        :param username: username
        :param password: password
        """
        self._auth_token = b64encode(username + ":" + password)#.rstrip("=")

    def __call__(self, request):
        """Insert the token after the path element of the URL"""
        url = urlparse(request.url)
        new_url = ParseResult(scheme=url.scheme,
                              netloc=url.netloc,
                              path=join(url.path, self.token),
                              params=url.params,
                              query=url.query,
                              fragment=url.fragment)
        request.url = new_url.geturl()
        return request

    @property
    def token(self):
        """
        Returns iMonnit auth token string
        The token is base64 encoding of username:password without the "=" delimiter
        """
        return self._auth_token
