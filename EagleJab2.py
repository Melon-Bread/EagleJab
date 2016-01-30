#!/usr/bin/env python2
import os, argparse, socket, sys, struct
import tkMessageBox
from io import open
import tkSimpleDialog, SimpleDialog
import tkFileDialog, FileDialog

# New & improved args parsing
parser = argparse.ArgumentParser(description=u'Sends .CIA files to the 3DS via FBI')
parser.add_argument(u'-c', u'--cia', help=u'.CIA rom file', metavar=u'FILE', required=False, nargs=1)
parser.add_argument(u'-i', u'--ip', help=u'The IP address of the target 3DS (e.g. 192.168.1.123)', metavar=u'STRING',
                    required=False, nargs=1)
args = parser.parse_args()

# Ask for the desired .CIA file if none is given
if args.cia:
    cia = args.cia[0]
else:
    cia = tkFileDialog.askopenfilename(title=u"Falcon Punch - Choose CIA to Send", initialdir=u"/",
                                             defaultextension=u".cia", filetypes=[(u"CIA File", u"*.cia")], multiple=False)

statinfo = os.stat(cia)
fbiinfo = struct.pack(u'!q', statinfo.st_size)

# Asks for the IP address of the 3DS if none is given
if args.ip:
    dsip = args.ip[0]
else:
    dsip = tkSimpleDialog.askstring(u"Falcon Punch", u"Enter 3Ds' IP:")

file = open(cia, u"rb")
sock = socket.socket()
sock.connect((dsip, 5000))

sock.send(fbiinfo)

# Sends the each chunk of the .CIA till there is nothing left
while True:
    chunk = file.read(16384)
    if not chunk:
        # Prints or displays a confirmation based on how the program is given info
        confirmation = u"Sent: \n" + cia + u"\n to the 3DS (" + dsip + u")"
        if args.cia and args.ip:
            print confirmation
        else:
            tkMessageBox.showinfo(u"Falcon Punch", confirmation)
        break  # EOF
    sock.sendall(chunk)

sock.close()
sys.exit()
