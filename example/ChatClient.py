from time import sleep
from sys import stdin, exit

from limugali.Connection import *

# This example uses Python threads to manage async input from sys.stdin.
# Don't ever do this. (I'm doing it for simplicity's sake)
from thread import *

class Client(ConnectionListener):
	def __init__(self):
		self.lock = allocate_lock()
		self.Connect(('localhost', 31425))
		print "Chat client started"
		print "Ctrl-C to exit"
		print "Enter your nickname: ",
		connection.Send({"action": "nickname", "nickname": stdin.readline().rstrip("\n")})
		# launch our threaded input loop
		t = start_new_thread(self.InputLoop, ())
	
	def Loop(self):
		connection.Pump()
		self.Pump()
	
	def InputLoop(self):
		# horrid threaded input loop
		while 1:
			self.Send({"action": "message", "message": stdin.readline().rstrip("\n")})
	
	def Send(self, data):
		# put a lock around our connection.Send
		self.lock.acquire()
		connection.Send(data)
		self.lock.release()

	###############################
	### Network event callbacks ###
	###############################
	
	def Network_players(self, data):
		print "*** players:", ", ".join([p[0] + (p[1] and "(away)" or "") for p in data['players']])
	
	def Network_message(self, data):
		print data['who'] + ": " + data['message']
	
	def Network_connected(self, data):
		print "You are now connected to the server"
	
	def Network_error(self, data):
		print 'error:', data
		connection.Close()
	
	def Network_disconnected(self, data):
		print 'Server disconnected'
		exit()

c = Client()
while 1:
	c.Loop()
	sleep(0.001)
