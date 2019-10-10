#!/usr/bin/python3

import socket
import sys
import time

class IRC:
	irc = socket.socket()

	def __init__(self):
		# Define the socket
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def send(self, chan, msg):
		# Transfer data
		self.irc.send(bytes("PRIVMSG " + chan + " " + msg + "\r\n", "UTF-8"))

	def connect(self, SERVER, PORT, CHANNEL, BOTNICK, BOTPASS, BOTNICKPASS):
		# Connect to the server
		print("Connecting to: "+SERVER+":"+str(PORT))
		self.irc.connect((SERVER, PORT))

		# Perform user authentication
		self.irc.send(bytes("USER " + BOTNICK + " " + BOTNICK +" " + BOTNICK+ " :This is a fun bot!\n", "UTF-8"))
		time.sleep(1)
		self.irc.send(bytes("NICK " + BOTNICK + "\r\n", "UTF-8"))
		self.irc.send(bytes("NICKSERV IDENTIFY " + BOTNICKPASS + " " + BOTPASS + "\r\n", "UTF-8"))

		# join the channel
		self.irc.send(bytes("JOIN " + CHANNEL + "\r\n", "UTF-8"))

	def get_text(self):
		text=self.irc.recv(2040).decode("UTF-8")

		if text.find('PING') != -1:
			self.irc.send(str('PONG ' + text.split(':')[1] + '\r\n').encode())

		return text

