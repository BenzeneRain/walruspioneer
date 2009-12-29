#!/usr/bin/python

###########################################################################
#  Walrus Pioneer, provide easy access to the Walrus service of Eucalyptus#
#  project.                                                               #
#  Copyright (C) 2009, Wen ZHANG                                          #
#                                                                         #
#  This program is free software: you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful,        #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
########################################################################### 

import os

import urllib2
import urlparse

import datetime

import hmac
import base64
from hashlib import sha1

class WalrusPioneerLib:
    '''
    This is the Walrus Pioneer library class, which provide interfaces to all
    kinds of operations to Walrus. 
    The operations are:
        ls --- List the contents of specific location, if no location is 
               spicified, the it will output the resources on the resources
               under user's root
        Others are still underconstuction
    '''

    def __init__(self, access_key = "", secret_key = "", \
                 walrus_url = "", verbose_level = 0):
        '''
            access_key --- the access key to the eucalyptus, the default value
                           is retrieved from the environment variable 
                           $EC2_ACCESS_KEY which can be found in the file eucarc
            secret_key --- the secret key to the eucalyptus, the default value
                           is retrieved from the environment variable 
                           $EC2_SECRET_KEY which can be found in the file eucarc
            walrus_url --- The Walrus service URL, should be given in full path.
                           For example, http://localhost:8773/services/Walrus
        '''
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

    ######################  Public  ##################################
    def executecmd(self, cmd, args = None):

        if self._check_provide_access_info() == False:
            print "Please provide the ACCESS KEY, SECRET KEY and\
                   Walrus service URL first"
            return None 
        
        if cmp(cmd, 'ls') == 0:
            self._update_time_header()

            visit_path = self._walrus_url
            if visit_path[-1] == '/':
                visit_path = visit_path[:-2] 

            if args != None:
                for item in args:
                    if item[0] != '/':
                        visit_path += '/'
                    visit_path += item

            self._update_StringToSign(urlparse.urlparse(visit_path).path)
            self._update_Signature()
            self._update_auth_header()
            ret = self._send_request(visit_path)
            return ret
        else:
            pass

    ################### Private #####################################
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

    # Functions below are used to generate the REST header for the request #
    def _update_time_header(self):
        self._time_header = datetime.datetime.utcnow().\
                            strftime('%a, %d %b %Y %H:%M:%S +0000')
        self._print_verbose_info("####Time Header####",self._time_header)

    def _update_StringToSign(self, path):
        self._StringToSign = 'GET\n\n\n' + self._time_header + '\n' + path 
        self._StringToSign = self._StringToSign.encode('utf-8')
        self._print_verbose_info("####String to Sign####",self._StringToSign)

    def _update_Signature(self):
        hmac_sha1 = hmac.new(self._secret_key, self._StringToSign, sha1)
        self._Signature = base64.b64encode(hmac_sha1.digest())

    def _update_auth_header(self):
        self._auth_header = 'AWS ' + self._access_key + ':' + self._Signature
        self._print_verbose_info("####Authority Header####",self._auth_header)

    ##### Function for sending the request #######################
    def _send_request(self, fullpath):
        theaders = {'User-Agent':'Python-urllib/2.6',\
                    'Accept':'*/*',\
                    'Date':self._time_header,\
                    'Authorization':self._auth_header}
        request = urllib2.Request(fullpath, headers = theaders)
        self._print_verbose_info("####Request Header####", request.headers)

        opener = urllib2.build_opener()
        feeddata = opener.open(request).read()

        self._print_verbose_info("####Feed back data####", feeddata)

        return feeddata

    ###### Check if all necessary information has been provided #########
    def _check_provide_access_info(self):
        '''
        If access key, secret key and walrus service url have been provided
        then return true, else return false
        '''
        if cmp(self._access_key, "") == 0 or\
           cmp(self._secret_key, "") == 0 or\
           cmp(self._walrus_url, "") == 0:
            return False
        else:
            return True


################ Self run test #################################
if __name__ == "__main__":
    wpl = WalrusPioneerLib(verbose_level = 2);
    print "Test case 1:\n"
    ret = wpl.executecmd(cmd = 'ls')
    print "Test case 2:\n"
    ret = wpl.executecmd(cmd = 'ls', args = ["wayne"])

