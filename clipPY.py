#! /usr/bin/env python
# clipPY - Clipboard Manager Using Python
# Ron Egli - github.com/smugzombie
# Version 0.0.2
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
 
def loadClippings():
	global clipping1, clipping2
	f=open(clipboardFile)
	lines=f.readlines()
	clipping0.setText(pyperclip.paste())
	try: clipping1.setText(lines[1])
	except: clipping1.setText("")
	try: clipping2.setText(lines[2])
	except: clipping2.setText("")
	try: clipping3.setText(lines[3])
        except: clipping3.setText("")
	try: clipping4.setText(lines[4])
        except: clipping4.setText("")

def loadClippings2(x):
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
#		response = urllib2.urlopen(req, data)
        except urllib2.HTTPError, err:
                print err.code
		return
        except:
                print "Timeout"
		return
	output = response.read()
#	print output
	try:
		output = json.loads(output)
	except:
		print "Cannot read json"
		return

#	print output[0]

	clipping0.setText(output[0])
	clipping1.setText(output[1])
        clipping2.setText(output[2])
        clipping3.setText(output[3])
        clipping4.setText(output[4])

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
			loadClippings2(x)
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
w.resize(240, 150)
 
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

loadClippings2("")

# Show window
w.show() 

# Watch Clipboard
watchClipboard() 

sys.exit(a.exec_())
