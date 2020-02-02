import socket

BYTES_TO_SEND = 1024

# Creates a socket that has a connection with the specied host and port
def run_client(host, port):

    #creates a new socket
    s = socket.socket()

    #connect the socket to the given host
    s.connect((host, port))
    print("Connected to host")

    #return the socket once created
    return s

# Function to send out bytes of data from filename
def send_file(filename, s):

	# opening a file
	f = open(filename, 'rb')

	# read bytes and set up counter
	l = f.read(BYTES_TO_SEND)
	byte = BYTES_TO_SEND

	# a forever loop untill file gets sent
	while (l):
\
		# send the bytes
		s.send(l)

		# read more bytes and incrementing counter
		l = f.read(BYTES_TO_SEND)
		byte += BYTES_TO_SEND

	print(byte, "bytes sent")

	# Close the connection with the client
	s.close()

# Receives a file
def receive_file(s):

    #open a temporary file to store the received bytes
    file = open("receivedFile", 'wb')

    while True:

        #receive 1024 bytes at a time and write them to a file
        bytes = s.recv(1024)
        file.write(bytes)

        #break infinite loop once all bytes are transferred
        if not bytes:
            break

    #close the file once transfer is complete
    file.close()

s = run_client("10.0.0.160", 12347)
send_file('receivedFile.mp4', s)
s.close()
