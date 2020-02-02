# first of all import the socket library
import socket
import signal
import sys
import time

# macro for min bytes
BYTES_TO_SEND = 1024
CLIENTS_ALLOWED = 5

# global socket declaration
s = socket.socket()

# Catch the ctrl+c signal
def handle_interrupt():
	s.close()
	print("  Server out...")
	sys.exit(0)

#
# Function to establish connection and send or recieve file
def run_server():

	# starting up server        
	print("Starting up server.....")
 
	# reserve a port on your computer
	port = 12347          

	# get the current hostname and ip
	hostName = socket.gethostname() 
	hostIp = socket.gethostbyname(hostName)    

	# bind the port with the socket
	s.bind(("", port))        
	print("Server running on", port)

	# put the socket into listening mode to connect
	s.listen(CLIENTS_ALLOWED)     
	print("Socket is listening")          

	# a forever loop until we interrupt it or error occyrs
	while True:

		# establish connection with client.
		c, addr = s.accept()     
		print('Got connection from', addr)

		# recieve file from the user
		receive_file(c)


#
# Function to send out bytes of data from filename
#
def send_file(filename):
	
	# opening a file
	f = open(filename, 'rb')

	# read bytes and set up counter
	l = f.read(BYTES_TO_SEND)
	byte = BYTES_TO_SEND


	# a forever loop untill file gets sent
	while (l):

		# send the bytes    
		c.send(l)

		# read more bytes and incrementing counter
		l = f.read(BYTES_TO_SEND)
		byte += BYTES_TO_SEND


	print(byte, " bytes sent")

	# Close the connection with the client
	c.close()   

#
# Receives a file
#
def receive_file(c):

	start = time.time()

	# open a temporary file to store the received bytes
	file = open("receivedFile", 'wb')

	while True:
		
		# receive 1024 bytes at a time and write them to a file
		bytes = c.recv(BYTES_TO_SEND)
		file.write(bytes)

		# break infinite loop once all bytes are transferred
		if not bytes:
			break

	# close the file once transfer is complete
	file.close()

	end = time.time()
	print("Finished running download of file in", int(end - start), "seconds")



try:
	# calls the main function to run the server
	run_server()
	
# handling the keyboard interrupt
except KeyboardInterrupt:
	handle_interrupt()