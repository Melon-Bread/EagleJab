#!/usr/bin/env python
import os, socket, sys, struct, easygui

statinfo = os.stat(sys.argv[1])
fbiinfo = struct.pack('!q', statinfo.st_size)
p = sys.argv[1]
dsip = easygui.enterbox("Enter 3DS' IP:", "FalconPunch", "192.168.1.1")

file = open(p, "rb")
sock = socket.socket()
sock.connect((dsip, 5000))

sock.send(fbiinfo)

while True:
    chunk = file.read(16384)
    if not chunk:
        easygui.msgbox("Sent " + p + " to the 3DS", "FalconPunch")
        break  # EOF
    sock.sendall(chunk)

sock.close()
sys.exit()
