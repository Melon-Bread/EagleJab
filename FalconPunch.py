#!/usr/bin/env python
import os, platform, argparse, socket, sys, struct, easygui

# New & improved args parsing
parser = argparse.ArgumentParser(description='Sends .CIA files to the 3DS via FBI')
parser.add_argument('-c', '--cia', help='.CIA rom file', metavar='FILE', required=False, nargs=1)
parser.add_argument('-i', '--ip', help='The IP address of the target 3DS (e.g. 192.168.1.123)', metavar='STRING',
                    required=False, nargs=1)
args = parser.parse_args()

# Ask for the desired .CIA file if none is given
if args.cia:
    cia = args.cia[0]
else:
    cia = easygui.fileopenbox("Choose CIA to Send", "Falcon Punch", default="/", filetypes=["*.cia", "*.*"],
                              multiple=False)

statinfo = os.stat(cia)
fbiinfo = struct.pack('!q', statinfo.st_size)

# Asks for the IP address of the 3DS if none is given
if args.ip:
    dsip = args.ip[0]
else:
    dsip = easygui.enterbox("Enter 3DS' IP:", "FalconPunch", "192.168.1.1")

file = open(cia, "rb")
sock = socket.socket()
sock.connect((dsip, 5000))

sock.send(fbiinfo)

# Sends the each chunk of the .CIA till there is nothing left
while True:
    chunk = file.read(16384)
    if not chunk:
        # Prints or displays a confirmation based on how the program is given info
        confirmation = "Sent " + cia + " to the 3DS (" + dsip + ")"
        if args.cia and args.ip:
            print(confirmation)
        else:
            easygui.msgbox(confirmation, "FalconPunch")
        break  # EOF
    sock.sendall(chunk)

sock.close()
sys.exit()
