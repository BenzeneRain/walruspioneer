#!/usr/bin/python

import urllib2
import os
import datetime
import hashlib
from hashlib import sha1
import hmac
import base64

class WalrusPioneerLib:

    def __init__(self, access_key = "", secret_key = "", \
                 walrus_url = "", verbose_level = 0):
        if cmp(access_key, "") == 0:
            try:
                self._access_key = os.getenv('EC2_ACCESS_KEY').encode('utf-8')
            except:
                print "Please provide the ACCESS KEY before use"
        else:
            self._access_key = access_key

        if cmp(secret_key, "") == 0:
            try:
                self._secret_key = os.getenv('EC2_SECRET_KEY').encode('utf-8')
            except:
                print "Please provide the ACCESS KEY before use"
        else:
            self._secret_key = secret_key

        if cmp(walrus_url, "") == 0:
            try:
                self._walrus_url = os.getenv('S3_URL').encode('utf-8')
            except:
                print "Please provide the URL of Walrus Service before use"
        else:
            self._walrus_url = walrus_url

        self._time_header = ""
        self._StringToSing = ""
        self._Signature = ""
        self._auth_header = ""
        self._verbose_level = verbose_level;

    def _set_secret_key(self, secret_key):
        self._set_secret_key = secret_key;

    def _set_access_key(self, access_key):
        self._set_access_key = access_key;

    def _set_walrus_url(self, walrus_url):
        self._walrus_url = walrus_url;

    def _print_verbose_info(self, header, data):
        if self._verbose_level >= 2:
            print header
        if self._verbose_level >= 1:
            print data
            print

    def _update_time_header(self):
        self._time_header = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
        self._print_verbose_info("####Time Header####",self._time_header)

    def _update_StringToSign(self):
        self._StringToSign = 'GET\n\n\n' + self._time_header + '\n' + '/services/Walrus'
        self._StringToSign = self._StringToSign.encode('utf-8')
        self._print_verbose_info("####String to Sign####",self._StringToSign)

    def _update_Signature(self):
        hmac_sha1 = hmac.new(self._secret_key, self._StringToSign, sha1)
        self._Signature = base64.b64encode(hmac_sha1.digest())

    def _update_auth_header(self):
        self._auth_header = 'AWS ' + self._access_key + ':' + self._Signature
        self._print_verbose_info("####Authority Header####",self._auth_header)

    def _send_request(self):
        theaders = {'User-Agent':'Python-urllib/2.6',\
                    'Accept':'*/*',\
                    'Date':self._time_header,\
                    'Authorization':self._auth_header}
        request = urllib2.Request(self._walrus_url, headers = theaders)
        self._print_verbose_info("####Request Header####", request.headers)

        opener = urllib2.build_opener()
        feeddata = opener.open(request).read()

        self._print_verbose_info("####Feed back data####", feeddata)

        return feeddata

    def _check_provide_access_info(self):
        if cmp(self._access_key, "") == 0 or cmp(self._secret_key, "") == 0:
            return False
        else:
            return True

    def executecmd(self, cmd, args = None):
        if cmp(cmd, 'ls') == 0:
            if self._check_provide_access_info() == False:
                print "Please provide the ACCESS KEY and SECRET KEY first"
                return 0
            else:
                self._update_time_header()
                self._update_StringToSign()
                self._update_Signature()
                self._update_auth_header()
                ret = self._send_request()
                return ret
        else:
            pass

if __name__ == "__main__":
    wpl = WalrusPioneerLib(verbose_level = 2);
    ret = wpl.executecmd(cmd = 'ls')

