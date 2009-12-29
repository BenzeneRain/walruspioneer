#!/usr/bin/python

import sys
import getopt

from WalrusPioneerLib import WalrusPioneerLib

class WalrusPioneerCmd:
    '''
    WalrusPioneer command line tool
    '''

    _command_list = ("list")

    @staticmethod
    def print_usage():
        print "Usage: ./wpcmd.py [OPTIONS...] COMMAND [COMMAND ARGUMENTS]\n"
        print "  -h, --help       \t\tShow this help"
        print "  -v, --verbose=NUM\t\tOutput verbose level - 0, 1, and 2. 0 is"
        print "                   \t\tthe default value, meaning no verbose at"
        print "                   \t\tat all. 2 indicates giving the most output"
        print ""
        print "Commands:"
        print "  list [COMMAND ARGUMENT]\tThe command receives zero or one argument."
        print "                         \tit will list the content under the root of"
        print "                         \tyour account in Walrus system if no argument"
        print "                         \tfollows. Otherwise the command shows the"
        print "                         \tcontents in the specific path of your account"
        print "                         \tin Walrus system"
        print ""
        print "Examples:"
        print " ./wpcmd.py -v 2 list \t\tList the content under the root of your account"
        print "                      \t\twith most verbose output"
        print " ./wpcmd.py list /test\t\tList the contents under the bucket with name "
        print "                      \t\t\"test\" under the root of your account"

    def execute_cmd(self, raw_args):
        c_opts, c_args = getopt.getopt(raw_args, "v:h", ["verbose=", "help"])

        verbose_level = 0
        for opt, val in c_opts:
            if opt in ("-h", "--help"):
                WalrusPioneerCmd.print_usage()
                sys.exit()
            elif opt in ("-v", "--verbose"):
                verbose_level = int(val)
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

        if c_args[0] == "list":
            if arg_len > 2:
                print "Invalid command usage. Please check help info."
                WalrusPioneerCmd.print_usage()
                sys.exit()
            wpl = WalrusPioneerLib(verbose_level = verbose_level) 
            ret = 0
            try:
                if arg_len == 1:
                    ret = wpl.executecmd(cmd = 'ls')
                else:
                    ret = wpl.executecmd(cmd = 'ls', args = [c_args[1]])
            except:
                print "Command execution failed"

        return ret

if __name__ == "__main__":
    wpc = WalrusPioneerCmd()
    ret = wpc.execute_cmd(sys.argv[1:])
    if ret != 0:
        print "---------------The result is--------------"
        print ret
        
