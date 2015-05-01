#!/usr/bin/env python
import os, argparse, socket, sys, struct
import tkinter.messagebox, tkinter.filedialog, tkinter.simpledialog

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
    cia = tkinter.filedialog.askopenfilename(title="Falcon Punch - Choose CIA to Send", initialdir="/",
                                             defaultextension=".cia", filetypes=[("CIA File", "*.cia")], multiple=False)

statinfo = os.stat(cia)
fbiinfo = struct.pack('!q', statinfo.st_size)

# Asks for the IP address of the 3DS if none is given
if args.ip:
    dsip = args.ip[0]
else:
    dsip = tkinter.simpledialog.askstring("Falcon Punch", "Enter 3Ds' IP:")

file = open(cia, "rb")
sock = socket.socket()
sock.connect((dsip, 5000))

sock.send(fbiinfo)

# Sends the each chunk of the .CIA till there is nothing left
while True:
    chunk = file.read(16384)
    if not chunk:
        # Prints or displays a confirmation based on how the program is given info
        confirmation = "Sent: \n" + cia + "\n to the 3DS (" + dsip + ")"
        if args.cia and args.ip:
            print(confirmation)
        else:
            tkinter.messagebox.showinfo("Falcon Punch", confirmation)
        break  # EOF
    sock.sendall(chunk)

sock.close()
sys.exit()
