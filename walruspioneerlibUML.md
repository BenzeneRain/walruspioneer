# Introduction #

Here is the simple UML structure of the Walrus Pioneer Lib


# Details #

There are several classes here. **WalrusPioneerLib** is in charge of processing and dispatchping the command. **WalrusPioneerDebug** is in charge of output the verbose information. **DataPacket** contains the packet headers and contents to send to Walrus, and different commands have their own data packet classes derived from the **DataPacket**.

![http://walruspioneer.googlecode.com/svn/wiki/walruspioneerlibUML.attach/WalrusPioneerLibUML.jpeg](http://walruspioneer.googlecode.com/svn/wiki/walruspioneerlibUML.attach/WalrusPioneerLibUML.jpeg)