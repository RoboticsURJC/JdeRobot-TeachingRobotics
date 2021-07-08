# Importing print function from Python3 to allow the overrride
from __future__ import print_function
import threading

# Class for psuedo cosnole functions
class Console:
	# Initialize the websocket and client
	def __init__(self):
		self.lock = threading.Lock()
		self.text_to_be_displayed_buffer = []
		
	# Function to set the websocket data
	def set_websocket(self, websocket, client):
		self.server = websocket
		self.client = client
	
	# Function to send text to psuedo console
	def print(self, text):
		self.text_to_be_displayed_buffer.append(text)
		print(text)

	# Function to flush the text buffer
	def get_text_to_be_displayed(self):
		buffer = self.text_to_be_displayed_buffer
		self.text_to_be_displayed_buffer = []
		return buffer

	# Function to read from psuedo console
	def read(self, text):
		# Print the text
		message = "#cor" + str(text)
		print(text)
		self.server.send_message(self.client, message)
		
		# Set the default
		self.user_input = ""
		
		# Keep running till we are getting
		# nothing from the user
		print("Waiting for User Input")
		while self.user_input == "":
			pass
		
		return self.user_input
	
	# Function to read the message from websocket
	# Gets called when there is an incoming message from the client
	def prompt(self, client, server, message):
		# Input from console
		source_code = message

		if(source_code[:4] == "#con"):
			source_code = source_code[5:]
			self.user_input = source_code
			print("Input from user received")
			print(self.user_input)
		
	
