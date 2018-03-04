# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import logging
import requests
from os import path
from requests.exceptions import HTTPError
from requests.utils import cookiejar_from_dict

from .json_file import JsonFile

logger = logging.getLogger(__name__)
config_dir = path.join(path.dirname(__file__), 'config')
default_headers_file = path.join(config_dir, 'headers.json')
default_cookies_file = path.join(config_dir, 'cookies.json')
default_login_file = path.join(config_dir, 'login.json')


class SessionAPI(object):
    def __init__(self, headers_file=default_headers_file, cookies_file=default_cookies_file):
        self.headers_jsonfile = JsonFile(headers_file)
        self.cookies_jsonfile = JsonFile(cookies_file)
        self._sess = None

    def _get_sess(self):
        sess = requests.Session()
        sess.headers.update(self.headers_jsonfile.load())
        sess.cookies.update(self.cookies_jsonfile.load())
        logger.info('Session init headers %s', sess.headers)
        logger.info('Session init cookies %s', sess.cookies)
        return sess

    @property
    def sess(self):
        if not self._sess:
            self._sess = self._get_sess()
        return self._sess

    def update_headers(self, headers):
        self.sess.headers.update(headers)
        logger.info('Session updated headers %s', self.sess.headers)

    def update_cookies(self, cookies):
        self.sess.cookies.update(cookies)
        logger.info('Session updated cookies %s', self.sess.cookies)

    def set_headers(self, headers):
        self.sess.headers = headers
        logger.info('Session new headers %s', self.sess.headers)

    def set_cookies(self, cookies):
        # Session.cookies should be class of CookieJar instead of dict
        self.sess.cookies = cookiejar_from_dict(cookies)
        logger.info('Session new cookies %s', self.sess.cookies)

    def get(self, *args, **kwargs):
        logger.info('HTTP GET request %s, %s', args, kwargs)
        res = self.sess.get(*args, **kwargs)
        self.cookies_jsonfile.save(self.sess.cookies.get_dict())
        res.raise_for_status()
        return res.json()

    def post(self, *args, **kwargs):
        logger.info('HTTP POST request %s, %s', args, kwargs)
        res = self.sess.post(*args, **kwargs)
        self.cookies_jsonfile.save(self.sess.cookies.get_dict())
        res.raise_for_status()
        return res.json()


class LoginSessionAPI(SessionAPI):
    def __init__(self, *args, login_url='', login_file=default_login_file, **kwargs):
        self.login_url = login_url
        self.login_jsonfile = JsonFile(login_file)
        super(LoginSessionAPI, self).__init__(*args, **kwargs)

    @property
    def login_data(self):
        """
            1. load json from file
            2. if missing some values, get it from user input
            3. save json to file
            4. return a dict of login data
        """
        raise NotImplementedError

    def login(self, extra_data={}):
        """ extra_data for optional vcode (sms code) """
        data = self.login_data
        data.update(extra_data)
        # login failed will raise HTTPError and stop the program
        return super(LoginSessionAPI, self).post(url=self.login_url, data=data)

    def get(self, *args, **kwargs):
        try:
            return super(LoginSessionAPI, self).get(*args, **kwargs)
        except HTTPError as e:
            if e.response.status_code != 403:
                raise
        # got 403 Client Error: FORBIDDEN for url, login again
        self.login()
        return super(LoginSessionAPI, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        try:
            return super(LoginSessionAPI, self).post(*args, **kwargs)
        except HTTPError as e:
            if e.response.status_code != 403:
                raise
        # got 403 Client Error: FORBIDDEN for url, login again
        self.login()
        return super(LoginSessionAPI, self).post(*args, **kwargs)
