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

import sys
import getopt

from WalrusPioneer.WalrusPioneerLib import WalrusPioneerLib

class WalrusPioneerCmd:
    '''
    WalrusPioneer command line tool
    '''

    # here need a comma to make it a real tuple
    _command_list = ("list","mkbkt","rmbkt","queryacl","putobj","delobj","getobj",)

    ################### Static Method ####################################
    @staticmethod
    def print_usage():
        print "Usage: ./wpcmd.py [OPTIONS...] COMMAND [COMMAND ARGUMENTS]\n"
        print "  -h, --help       \t\tShow this help"
        print "  -v, --verbose=NUM\t\tOutput verbose level - 0, 1, and 2. 0 is"
        print "                   \t\tthe default value, meaning no verbose at"
        print "                   \t\tat all. 2 indicates giving the most output"
        print "  --id=ACCESS_KEY  \t\tUse the specific key as ACCESS_KEY, the"
        print "                   \t\tdefault value is $EC2_ACCESS_KEY which is"
        print "                   \t\tset by eucarc file"
        print "  --secret=SECRET_KEY\t\tUse the specific key as SECRET_KEY, the "
        print "                     \t\tdefault value is $EC2_SECRET_KEY which is"
        print "                     \t\tset by eucarc file"
        print "  --url=SERVICE_URL\t\tUse the specific walrus service url address,"
        print "                   \t\tthe default value is $S3_URL which is set by"
        print "                   \t\teucarc file. It should be a full address, for"
        print "                   \t\texample \"http://localhost:8773/services/Walrus\""
        print ""
        print "Commands:"
        print "  list [COMMAND ARGUMENT]\tThe command receives zero or one argument."
        print "                         \tit will list the content under the root of"
        print "                         \tyour account in Walrus system if no argument"
        print "                         \tfollows. Otherwise the command shows the"
        print "                         \tcontents in the specific path of your account"
        print "                         \tin Walrus system"
        print "  mkbkt <BucketName>     \tThe command receives one argument."
        print "                         \tIt will create the bucket with specific"
        print "                         \tbucket name"
        print "  rmbkt <BucketName>     \tThe command receives one argument."
        print "                         \tIt will delete the bucket with specific"
        print "                         \tbucket name"
        print "  queryacl <ResourceName>\tThe command receives one argument."
        print "                         \tIt will query the access control list of"
        print "                         \tspecific bucket or object"
        print "  putobj <src> <dst>     \tThe command receives two arguments."
        print "                         \tIt will upload the file specified by src"
        print "                         \tto the destination notified by dst. Note"
        print "                         \tthat user needs to specify the name in the"
        print "                         \tremote server. If dst is a bucket name  "
        print "                         \tending with a /, then the name of upload"
        print "                         \tfile will keep the same as the original one."
        print "  getobj <src> [dst]     \tThe command receives two arguments."
        print "                         \tIt will download the file specified by src"
        print "                         \tto the destination notified by dst. Note"
        print "                         \tthat user needs to specify the name in the"
        print "                         \tremote server. If dst is a directory name  "
        print "                         \tending with a /, then the name of download"
        print "                         \tfile will keep the same as the original one."
        print "                         \tIf no dst provided, the default value is the"
        print "                         \tcurrent working directory"
        print "  delobj <ResourceName>  \tThe command receives one argument."
        print "                         \tIt will delete the object with specific"
        print "                         \tpath and object name"
        print ""
        print "Examples:"
        print " ./wpcmd.py -v 2 list \t\tList the content under the root of your account"
        print "                      \t\twith most verbose output"
        print " ./wpcmd.py list /test\t\tList the contents under the bucket with name "
        print "                      \t\t\"test\" under the root of your account"

    ############### Public Methods #################################################
    def execute_cmd(self, raw_args):
        '''
        raw_args are the args get from the commend line except for the program name.
        you can usually get it use sys.argv[1:]
        '''
        verbose_level, c_access_key, c_secret_key, c_args, arg_len, c_url = \
            self._analyse_arguments(raw_args)

        wpl = WalrusPioneerLib(verbose_level = verbose_level,\
                               access_key = c_access_key,\
                               secret_key = c_secret_key,\
                               walrus_url = c_url)

        if c_args[0] == "list":
            return self._execute_list(wpl, c_args, arg_len)
        elif c_args[0] == "mkbkt":
            return self._execute_mkbkt(wpl, c_args, arg_len)
        elif c_args[0] == "rmbkt":
            return self._execute_rmbkt(wpl, c_args, arg_len)
        elif c_args[0] == "queryacl":
            return self._execute_queryacl(wpl, c_args, arg_len)
        elif c_args[0] == "putobj":
            return self._execute_putobj(wpl, c_args, arg_len)
        elif c_args[0] == "getobj":
            return self._execute_getobj(wpl, c_args, arg_len)
        elif c_args[0] == "delobj":
            return self._execute_delobj(wpl, c_args, arg_len)
        # elif ...
        #   return ...
        # else
        #   return ...

        # otherwise it will return None automatically

    ######################### Private Methods ################################
    def _analyse_arguments(self, raw_args):
        try:
            c_opts, c_args = getopt.getopt(raw_args, "v:h",
                                           ["verbose=", "help", "id=", "secret=", "url="])
        except getopt.GetoptError:
            WalrusPioneerCmd.print_usage()
            sys.exit(1)

        verbose_level = 0
        c_access_key = ""
        c_secret_key = ""
        c_url = ""
        for opt, val in c_opts:
            if opt in ("-h", "--help"):
                WalrusPioneerCmd.print_usage()
                sys.exit()
            elif opt in ("-v", "--verbose"):
                verbose_level = int(val)
            elif opt in ("--id"):
                c_access_key = val
            elif opt in ("--secret"):
                c_secret_key = val
            elif opt in ("--url"):
                c_url = val
            else:
                print "Invalid options. Please check help info."
                WalrusPioneerCmd.print_usage()
                sys.exit()

        arg_len = len(c_args)

        if arg_len < 1:
            print "No command found. Please check help info."
            WalrusPioneerCmd.print_usage()
            sys.exit()

        if c_args[0] not in self._command_list:
            print "Invalid command. Please check help info."
            WalrusPioneerCmd.print_usage()
            sys.exit()

        return [verbose_level,\
                c_access_key,\
                c_secret_key,\
                c_args,\
                arg_len,\
                c_url]

    ################# Command execution preprocessing subroutings ###############
    def _execute_list(self, wpl, args, arg_len):
        if arg_len > 2:
            print "Invalid command usage. Please check help info."
            WalrusPioneerCmd.print_usage()
            sys.exit()
        ret = 0
        try:
            if arg_len == 1:
                ret = wpl.executecmd(cmd = 'list')
            else:
                ret = wpl.executecmd(cmd = 'list', args = [args[1]])
        except:
            print "Command execution failed"

        return ret

    def _execute_mkbkt(self, wpl, args, arg_len):
        if arg_len != 2:
            print "Invalid command usage. Please check help info."
            WalrusPioneerCmd.print_usage()
            sys.exit()
        ret = 0
        try:
            ret = wpl.executecmd(cmd = 'mkbkt', args = [args[1]])
        except:
            print "Command execution failed"

        return ret

    def _execute_rmbkt(self, wpl, args, arg_len):
        if arg_len != 2:
            print "Invalid command usage. Please check help info."
            WalrusPioneerCmd.print_usage()
            sys.exit()
        ret = 0
        try:
            ret = wpl.executecmd(cmd = 'rmbkt', args = [args[1]])
        except:
            print "Command execution failed"

        return ret

    def _execute_queryacl(self, wpl, args, arg_len):
        if arg_len != 2:
            print "Invalid command usage. Please check help info."
            WalrusPioneerCmd.print_usage()
            sys.exit()
        ret = 0
        try:
            ret = wpl.executecmd(cmd = 'queryacl', args = [args[1]])
        except:
            print "Command execution failed"

        return ret

    def _execute_putobj(self, wpl, args, arg_len):
        if arg_len != 3:
            print "Invalid command usage. Please check help info."
            WalrusPioneerCmd.print_usage()
            sys.exit()
        ret = 0
        try:
            ret = wpl.executecmd(cmd = 'putobj', args = args[1:])
        except:
            print "Command execution failed"

        return ret

    def _execute_getobj(self, wpl, args, arg_len):
        if arg_len < 1:
            print "Invalid command usage. Please check help info."
            WalrusPioneerCmd.print_usage()
            sys.exit()
        ret = 0
        try:
            ret = wpl.executecmd(cmd = 'getobj', args = args[1:])
        except:
            print "Command execution failed"

        return ret

    def _execute_delobj(self, wpl, args, arg_len):
        if arg_len != 2:
            print "Invalid command usage. Please check help info."
            WalrusPioneerCmd.print_usage()
            sys.exit()
        ret = 0
        try:
            ret = wpl.executecmd(cmd = 'delobj', args = [args[1]])
        except:
            print "Command execution failed"

        return ret


if __name__ == "__main__":
    wpc = WalrusPioneerCmd()
    ret = wpc.execute_cmd(sys.argv[1:])
    if ret != 0:
        print "---------------The result is--------------"
        print ret

