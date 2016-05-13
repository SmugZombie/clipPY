#! /usr/bin/env python
# clipPY - Clipboard Manager Using Python
# Ron Egli - github.com/smugzombie
# Version 0.0.3
# -*- coding: utf-8 -*-
import pyperclip
import sys
import os
import time
import urllib2
import json

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import pyqtSlot

clipboardFile = "clipboard.txt"
clippings = []
lastClip = ""
key = ""
 
def loadClippings(x):
	global clipping1, clipping2, clipping3, clipping4
	url = "https://apt-cyg.com/clipboard/?key="+key
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})

	data = "";
	if x != "":
		data = {}
		data['clipboard'] = x;
		data = json.dumps(data)

        output = {};
        output['url'] = url
        try:
                response = urllib2.urlopen(req, data, timeout = 30)
        except urllib2.HTTPError, err:
                print err.code
		return
        except:
                print "Timeout"
		return
	output = response.read()
	try:
		output = json.loads(output)
	except:
		print "Cannot read json"
		return

	clipping0.setText(output[0])
	clipping1.setText(output[1])
        clipping2.setText(output[2])
        clipping3.setText(output[3])
        clipping4.setText(output[4])
        clipping5.setText(output[5])
        clipping6.setText(output[6])
        clipping7.setText(output[7])
        clipping8.setText(output[8])
        clipping9.setText(output[9])

def sendMessage(title, message):
	os.system('notify-send "'+title+'" "'+message+'"')

def saveClipboard(x):
	global clippings
	clippings.insert(0,x)
	clippings = clippings[0:10]
	saveToFile('\n'.join(clippings))

def saveToFile(x):
	with open("clipboard.txt", "w") as clipboard:
                clipboard.write(x)

def watchClipboard():
	global lastClip
	x = False
	while x is not True:
		x = pyperclip.paste() #.replace('\n', ' ').replace('\r', '')
		if x != lastClip:
			loadClippings(x)
			lastClip = x
		time.sleep(.500)

def watchClipboard2():
	global lastClip
	x = pyperclip.paste().replace('\n', ' ').replace('\r', '')

	if x != lastClip:
#		saveClipboard(x)
		lastClip = x
		loadClippings2(x)
	time.sleep(.500)
	x = "";
	watchClipboard()

# Create an PyQT4 application object.
a = QApplication(sys.argv)       

# The QWidget widget is the base class of all user interface objects in PyQt4.
w = QMainWindow()
 
# Set window size. 
w.resize(240, 270)
 
# Set window title  
w.setWindowTitle("ClipPY") 
 
# Create main menu
mainMenu = w.menuBar()
mainMenu.setNativeMenuBar(False)
fileMenu = mainMenu.addMenu('&File')
 
# Add exit button
exitButton = QAction(QIcon('exit24.png'), 'Exit', w)
exitButton.setShortcut('Ctrl+Q')
exitButton.setStatusTip('Exit application')
exitButton.triggered.connect(w.close)
fileMenu.addAction(exitButton)

# Create textbox
clipping0 = QLineEdit(w)
clipping0.move(20, 20)
clipping0.resize(200,20) 
 
clipping1 = QLineEdit(w)
clipping1.move(20, 45)
clipping1.resize(200,20) 

clipping2 = QLineEdit(w)
clipping2.move(20, 70)
clipping2.resize(200,20) 

clipping3 = QLineEdit(w)
clipping3.move(20, 95)
clipping3.resize(200,20) 

clipping4 = QLineEdit(w)
clipping4.move(20, 120)
clipping4.resize(200,20) 

clipping5 = QLineEdit(w)
clipping5.move(20, 145)
clipping5.resize(200,20) 
 
clipping6 = QLineEdit(w)
clipping6.move(20, 170)
clipping6.resize(200,20) 

clipping7 = QLineEdit(w)
clipping7.move(20, 195)
clipping7.resize(200,20) 

clipping8 = QLineEdit(w)
clipping8.move(20, 220)
clipping8.resize(200,20) 

clipping9 = QLineEdit(w)
clipping9.move(20, 245)
clipping9.resize(200,20) 

loadClippings("")

# Show window
w.show() 

# Watch Clipboard
watchClipboard() 

sys.exit(a.exec_())
