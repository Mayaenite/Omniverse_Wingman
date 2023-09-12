"""
Directions
Add this file to Wing's preferences > IDE Extension Scripting
then add run-in-maya to preferences > User Interface > Keyboard > Custom keybindings

This is a modified version of
https://github.com/raiscui/wing-scripts/blob/master/wingHotkeys.py

Changes include:
*  unifying highlighted text and sending py files to Maya
*  Reloading and importing py files in the namespace of their package


#starting with Pymel 1.3 we no longer need to worry about adding the completion\pi files
#https://dev.to/chadrik/pymels-new-type-stubs-2die


#The outdated way------------------------------------------
#download the devkit

#add the pi interfaces found here:
#devkitBase\devkit\other\pymel\extras\completion\pi

#Note: Maya 2023 is missing the other folder, so download Maya 2022 devkit and copy the other folder into
#the 2023 devkit

#to wing
#This can be added to the Source Analysis > Advanced > Interface File Path preference in Wing.
"""
 

import socket

_socket_ip   = '127.0.0.1'
_socket_port = 6000

def connect_To_Omniverse(code):
	mSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	mSocket.connect((_socket_ip, _socket_port))
	mSocket.send( code.encode() )
	
_ignore_scripts = True