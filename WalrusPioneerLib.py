#!/usr/bin/python

###########################################################################
#  Walrus Pioneer, provide easy access to the Walrus service of Eucalyptus#
#  project.                                                               #
#  Copyright (C) 2009, Walrus Pioneer Project Group                       #
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

#import urllib2
import httplib
import urlparse

import datetime

import hmac
import base64
from hashlib import sha1
from hashlib import md5

####################### Class WalrusPioneerLib ###############################
class WalrusPioneerLib:
    '''
    This is the Walrus Pioneer library class, which provide interfaces to all
    kinds of operations to Walrus.
    The operations are:
        list --- List the contents of specific location, if no location is
                 spicified, the it will output the resources on the resources
                 under user's root
        mkbkt --- Make a bucket with the specific name
        rmbkt --- Remove a bucket with the specific name
        queryacl --- Query the access control list of a bucket or an object 
        putobj --- put an object to the walrus
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

        self._verbose_level = verbose_level;

    ######################  Public  ##################################
    def executecmd(self, cmd, args = None):

        if not self._check_provide_access_info():
            print "Please provide the ACCESS KEY, SECRET KEY and\
                   Walrus service URL first"
            return

        if cmd == 'list':
            return self._execute_cmd_list(args)
        elif cmd == 'mkbkt':
            return self._execute_cmd_mkbkt(args)
        elif cmd == 'rmbkt':
            return self._execute_cmd_rmbkt(args)
        elif cmd == 'queryacl':
            return self._execute_cmd_queryacl(args)
        elif cmd == 'putobj':
            return self._execute_cmd_putobj(args)
        # elif ... other commands

    def set_secret_key(self, secret_key):
        self._set_secret_key = secret_key;

    def set_access_key(self, access_key):
        self._set_access_key = access_key;

    def set_walrus_url(self, walrus_url):
        self._walrus_url = walrus_url;


    ################### Private #####################################
    def _execute_cmd_list(self, args):
        visit_path = self._walrus_url
        if visit_path[-1] == '/':
            visit_path = visit_path[:-2]

        if args != None:
            for item in args:
                if item[0] != '/':
                    visit_path += '/'
                visit_path += item

        packet = DataPacket_list(self._verbose_level)
        packet_headers = packet.generate_header(self._access_key,\
                                                self._secret_key,\
                                                urlparse.urlparse(visit_path).path)
    
        return self._send_request(method   = "GET",          \
                                  fullpath = visit_path,     \
                                  headers  = packet_headers)

    def _execute_cmd_mkbkt(self, args):
        if len(args) != 1:
            print "Invalid argument for mkbkt command!"
            return None

        visit_path = self._walrus_url
        if visit_path[-1] == '/':
            visit_path = visit_path[:-2]

        for item in args:
            if item[0] != '/':
                visit_path += '/'
            visit_path += item

        packet = DataPacket_mkbkt(self._verbose_level)
        packet_headers = packet.generate_header(self._access_key,\
                                                self._secret_key,\
                                                urlparse.urlparse(visit_path).path)
    
        return self._send_request(method   = "PUT",          \
                                  fullpath = visit_path,     \
                                  headers  = packet_headers)
        
    def _execute_cmd_rmbkt(self, args):
        if len(args) != 1:
            print "Invalid argument for rmbkt command!"
            return None

        visit_path = self._walrus_url
        if visit_path[-1] == '/':
            visit_path = visit_path[:-2]

        for item in args:
            if item[0] != '/':
                visit_path += '/'
            visit_path += item

        packet = DataPacket_rmbkt(self._verbose_level)
        packet_headers = packet.generate_header(self._access_key,\
                                                self._secret_key,\
                                                urlparse.urlparse(visit_path).path)
    
        return self._send_request(method   = "DELETE",       \
                                  fullpath = visit_path,     \
                                  headers  = packet_headers)

    def _execute_cmd_queryacl(self, args):
        visit_path = self._walrus_url
        if visit_path[-1] == '/':
            visit_path = visit_path[:-2]

        if args != None:
            for item in args:
                if item[0] != '/':
                    visit_path += '/'
                visit_path += item

        packet = DataPacket_queryacl(self._verbose_level)
        packet_headers = packet.generate_header(self._access_key,\
                                                self._secret_key,\
                                                urlparse.urlparse(visit_path).path\
                                                + "?acl")
    
        return self._send_request(method   = "GET",          \
                                  fullpath = visit_path + "?acl",     \
                                  headers  = packet_headers)

    def _execute_cmd_putobj(self, args):
        visit_path = self._walrus_url
        if visit_path[-1] == '/':
            visit_path = visit_path[:-2]

        if len(args) != 2:
            return None
        
#        if args[0][-1] == '/':
#            print "Do not suppot upload a directory yet"
#            return None

        packet = DataPacket_putobj(self._verbose_level)
        packet_content = packet.generate_body(args[0])

        item = args[1]
        if item[0] != '/':
            visit_path += '/'
        if item[-1] == '/':
            item += (args[0].split("/"))[-1]
        visit_path += item

        packet_headers = packet.generate_header(self._access_key,\
                                                self._secret_key,\
                                                urlparse.urlparse(visit_path).path)
    
        return self._send_request(method   = "PUT",          \
                                  fullpath = visit_path,     \
                                  headers  = packet_headers, \
                                  contents = packet_content)

    ##### Function for sending the request #######################
    def _send_request(self, method = "", fullpath = "", headers = {}, contents = None):

        WalrusPioneerDebug.print_verbose("####Request Method ####", \
                                         method,                    \
                                         self._verbose_level)
        
        WalrusPioneerDebug.print_verbose("####Request Header####", \
                                         headers,                  \
                                         self._verbose_level)

        WalrusPioneerDebug.print_verbose("####Request Content####", \
                                         contents,                  \
                                         self._verbose_level)

        urldetails = urlparse.urlparse(fullpath)
        conn = httplib.HTTPConnection(urldetails.netloc)
        conn.set_debuglevel(self._verbose_level)

        resource = urldetails.path
        if urldetails.query != "":
            resource += "?" + urldetails.query

        conn.putrequest(method,         \
                        resource,\
                        skip_accept_encoding = True)
        for header in headers:
            conn.putheader(header, headers[header])

        conn.endheaders()
        
        if contents != None:
            conn.send(contents)
            contents.close()
        print "\n#########Send Data ###########\n"
        response = conn.getresponse()
        feeddata = response.read()

        WalrusPioneerDebug.print_verbose("####Feed back data####", \
                                         feeddata,                 \
                                         self._verbose_level)

        return feeddata

    ###### Check if all necessary information has been provided #########
    def _check_provide_access_info(self):
        '''
        If access key, secret key and walrus service url have been provided
        then return true, else return false
        '''
        return self._access_key  \
            and self._secret_key \
            and self._walrus_url

####################### Class DataPacket  ###############################
class DataPacket:
    def __init__(self, verbose_level = 0):
        self._verbose_level = verbose_level

    #################### Private Methods ##########################

    def _get_time_header(self):
        time_header = datetime.datetime.utcnow().\
                            strftime('%a, %d %b %Y %H:%M:%S +0000')

        WalrusPioneerDebug.print_verbose("####Time Header####",\
                                         time_header,          \
                                         self._verbose_level)
        return time_header

    def _get_stringtosign(self                        ,\
                          HTTP_Verb               = "",\
                          Content_MD5             = "",\
                          Content_type            = "",\
                          date                    = "",\
                          CanonicalizedAmzHeaders = "",\
                          CanonicalizedResources  = ""):

        stringtosign = HTTP_Verb               + '\n' +\
                       Content_MD5             + '\n' +\
                       Content_type            + '\n' +\
                       date                    + '\n' +\
                       CanonicalizedAmzHeaders +       \
                       CanonicalizedResources

        stringtosign = stringtosign.encode('utf-8')
        WalrusPioneerDebug.print_verbose("####String to Sign####",          \
                                         stringtosign.replace('\n', r'\n'), \
                                         self._verbose_level)
        return stringtosign

    def _get_signature(self                        ,\
                       secret_key              = "",\
                       HTTP_Verb               = "",\
                       Content_MD5             = "",\
                       Content_type            = "",\
                       date                    = "",\
                       CanonicalizedAmzHeaders = "",\
                       CanonicalizedResources  = ""):

        hmac_sha1 = hmac.new(secret_key,                \
                             self._get_stringtosign     \
                             (                          \
                                HTTP_Verb,              \
                                Content_MD5,            \
                                Content_type,           \
                                date,                   \
                                CanonicalizedAmzHeaders,\
                                CanonicalizedResources  \
                             ),                         \
                             sha1)

        return base64.b64encode(hmac_sha1.digest())


    def _get_authorization_header(self                        ,\
                                  access_key              = "",\
                                  secret_key              = "",\
                                  HTTP_Verb               = "",\
                                  Content_MD5             = "",\
                                  Content_type            = "",\
                                  date                    = "",\
                                  CanonicalizedAmzHeaders = "",\
                                  CanonicalizedResources  = ""):

        auth_header = ""
        auth_header = 'AWS ' + access_key + ':' +\
                      self._get_signature        \
                      (                          \
                         secret_key,             \
                         HTTP_Verb,              \
                         Content_MD5,            \
                         Content_type,           \
                         date,                   \
                         CanonicalizedAmzHeaders,\
                         CanonicalizedResources  \
                      )                          \

        WalrusPioneerDebug.print_verbose("####Authority Header####",\
                                         auth_header,               \
                                         self._verbose_level)
        return auth_header

##################### Class DataPacket_list ##########################
class DataPacket_list(DataPacket):

    #################### Public Methods ##########################

    def generate_header(self                        ,\
                        access_key              = "",\
                        secret_key              = "",\
                        CanonicalizedResources  = ""):

        headers = {}
        headers['User-Agent'] = r"Python-urllib/2.6"
        headers['Accept'] = r"*/*"
        headers['Date'] = self._get_time_header()
        headers['Authorization'] = self._get_authorization_header    \
                                   (                                 \
                                      access_key = access_key,       \
                                      secret_key = secret_key,       \
                                      HTTP_Verb  = 'GET',            \
                                      date       = headers['Date'],  \
                                      CanonicalizedResources =       \
                                      CanonicalizedResources         \
                                   )
        return headers

class DataPacket_mkbkt(DataPacket):

    #################### Public Methods ##########################

    def generate_header(self                        ,\
                        access_key              = "",\
                        secret_key              = "",\
                        CanonicalizedResources  = ""):

        headers = {}
#        headers['x-amz-acl'] = r"public-read-write"
        headers['User-Agent'] = r"Python-urllib/2.6"
        headers['Accept'] = r"*/*"
        headers['Date'] = self._get_time_header()
        headers['Authorization'] = self._get_authorization_header    \
                                   (                                 \
                                      access_key = access_key,       \
                                      secret_key = secret_key,       \
                                      HTTP_Verb  = 'PUT',            \
                                      date       = headers['Date'],  \
#                                      CanonicalizedAmzHeaders = "x-amz-acl:public-read-write\n", \
                                      CanonicalizedResources =       \
                                      CanonicalizedResources         \
                                   )
        return headers

class DataPacket_rmbkt(DataPacket):

    #################### Public Methods ##########################

    def generate_header(self                        ,\
                        access_key              = "",\
                        secret_key              = "",\
                        CanonicalizedResources  = ""):

        headers = {}
        headers['User-Agent'] = r"Python-urllib/2.6"
        headers['Accept'] = r"*/*"
        headers['Date'] = self._get_time_header()
        headers['Authorization'] = self._get_authorization_header    \
                                   (                                 \
                                      access_key = access_key,       \
                                      secret_key = secret_key,       \
                                      HTTP_Verb  = 'DELETE',         \
                                      date       = headers['Date'],  \
                                      CanonicalizedResources =       \
                                      CanonicalizedResources         \
                                   )
        return headers

class DataPacket_queryacl(DataPacket):

    #################### Public Methods ##########################

    def generate_header(self                        ,\
                        access_key              = "",\
                        secret_key              = "",\
                        CanonicalizedResources  = ""):

        headers = {}
        headers['User-Agent'] = r"Python-urllib/2.6"
        headers['Accept'] = r"*/*"
        headers['Date'] = self._get_time_header()
        headers['Authorization'] = self._get_authorization_header    \
                                   (                                 \
                                      access_key = access_key,       \
                                      secret_key = secret_key,       \
                                      HTTP_Verb  = 'GET',         \
                                      date       = headers['Date'],  \
                                      CanonicalizedResources =       \
                                      CanonicalizedResources         \
                                   )
        return headers

class DataPacket_putobj(DataPacket):

    #################### Public Methods ##########################
    def __init__(self, verbose_level = 0):
        DataPacket.__init__(self, verbose_level)
        self._content_length = 0
        self._content_md5 = ""

    def generate_header(self                        ,\
                        access_key              = "",\
                        secret_key              = "",\
                        CanonicalizedResources  = ""):

        headers = {}
        headers['User-Agent'] = r"Python-urllib/2.6"
        headers['Accept'] = r"*/*"
        headers['Date'] = self._get_time_header()
        headers['Content-Length'] = self._content_length
        headers['Content-MD5'] = self._content_md5
        headers['Expect'] = "100-continue"
        headers['Authorization'] = self._get_authorization_header    \
                                   (                                 \
                                      access_key = access_key,       \
                                      secret_key = secret_key,       \
                                      HTTP_Verb  = 'PUT',            \
                                      Content_MD5 = self._content_md5,\
                                      date       = headers['Date'],  \
                                      CanonicalizedResources =       \
                                      CanonicalizedResources         \
                                   )
        return headers
    
    def generate_body(self, filename):
        try:
            bodysrc = file(filename)
            
            #get Content-Length #
            bodysrc.seek(0, 2)
            self._content_length = bodysrc.tell()
            bodysrc.seek(0, 0)

            #get Content-MD5 value #
            m = md5()
            data = bodysrc.read(1024)
            while data != "":
                m.update(data)
                data = bodysrc.read(1024)
            self._content_md5 = base64.b64encode(m.digest())

            bodysrc.seek(0, 0)

            return bodysrc
        except IOError:
            print "Fail to open the %s" % filename
            return None


##################### Class WalrusPioneerDebug #######################
class WalrusPioneerDebug:

    @staticmethod
    def print_verbose(description, data, verbose_level):
        if verbose_level >= 2:
            print description
        if verbose_level >= 1:
            print data
            print 


################ Self run test #################################
if __name__ == "__main__":
    wpl = WalrusPioneerLib(verbose_level = 2);
    print "Test case 1:\n"
    ret = wpl.executecmd(cmd = 'list')
    print "Test case 2:\n"
    ret = wpl.executecmd(cmd = 'mkbkt', args = ["test"])
    print "Test case 3:\n"
    ret = wpl.executecmd(cmd = 'list', args = ["test"])
    print "Test case 4:\n"
    ret = wpl.executecmd(cmd = 'rmbkt', args = ["test"])
    print "Test case 5:\n"
    ret = wpl.executecmd(cmd = 'list')

