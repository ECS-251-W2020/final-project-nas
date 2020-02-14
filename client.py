import socket
import sys
import time
from helperFunctions import pad_string, find_ip
import ledgerFunctions as ledger

BYTES_TO_SEND = 1024
REQUEST_MAX_LENGTH = 100
#
# Creates a socket that has a connection with the specied host and port
#
def run_client(host, port=12345):

    #creates a new socket
    s = socket.socket()
    #connect the socket to the given host
    s.connect((host, port))
    print("Connected to host")

    #return the socket once created
    return s

#
# Function to send out bytes of data from filename
#
def send_file(s, filename):

    # create a push request for the server and encode it to bytes
    cmd = pad_string("push " + filename)
    s.send(cmd.encode())

    # recieve response from server
    recv = s.recv(REQUEST_MAX_LENGTH).decode()
    print(recv)

    # check if the servor responded with an error
    if(recv.split(' ', 1)[0] != "Error"):

        # opening a file
        f = open(filename, 'rb')

        # read bytes and set up counter
        l = f.read(BYTES_TO_SEND)
        byte = BYTES_TO_SEND

        # a forever loop untill file gets sent
        while (l):

            # send the bytes
            s.send(l)

            # read more bytes and incrementing counter
            l = f.read(BYTES_TO_SEND)
            byte += BYTES_TO_SEND

        print(byte, "bytes sent")

    # server did respond with error
    else:
        print("Something went wrong")

#
# Receives a file
#
def receive_file(s, filename):

    # create a pull request for the server and encode it to bytes
    cmd = pad_string("pull " + filename)
    s.send(cmd.encode())

    # recieve confirmation response from server
    receivedMessage = s.recv(REQUEST_MAX_LENGTH).decode()
    print(receivedMessage)

    # check if the servor responded with an error
    if(receivedMessage.split(' ', 1)[0] != "Error"):

        print("Downloading file")
        #open a temporary file to store the received bytes
        file = open(filename, 'wb')
        start = time.time()

        while True:

            #receive 1024 bytes at a time and write them to a file
            bytes = s.recv(1024)
            file.write(bytes)

            #break infinite loop once all bytes are transferred
            if not bytes:
                break

        #close the file once transfer is complete
        file.close()
        end = time.time()
        print("Finished running download of file in %.2f seconds" %  float(end - start))

    # Server responded with an error
    else:
        print("Something went wrong.")

#
# Gets a copy of the current ledger from a known host, adds itself,
# and broadcasts to all servers
#
def get_ledger(s):

    # create a new node request for the server and encode it to bytes
    cmd = pad_string("ledger ledger.json")
    s.send(cmd.encode())

    # recieve confirmation response from server
    receivedMessage = s.recv(REQUEST_MAX_LENGTH).decode()
    print(receivedMessage)

    if(receivedMessage.split(' ', 1)[0] != "Error"):

        print("Downloading ledger")
        #open a new ledger and store the received bytes
        file = open(ledger.LEDGER_PATH, 'wb')
        start = time.time()

        while True:

            #receive 1024 bytes at a time and write them to a file
            bytes = s.recv(1024)
            file.write(bytes)

            #break infinite loop once all bytes are transferred
            if not bytes:
                break

        #close the file once transfer is complete
        file.close()
        end = time.time()
        print("Finished running download of ledger in %.2f seconds" %  float(end - start))

    # Server responded with an error
    else:
        print("Something went wrong while getting the ledger.")

    # Update ledger with ip of client
    ledger.add_node(find_ip())

    # Send updated ledger to all serversin the network
    #for ip in ledger_get_ips():
        #update ledger

#
# Deals with creating the client node as well as providing the main command line interface for the program
#
def main():
    #s = run_client("10.0.0.160", 12345)
    s = run_client("172.20.10.3", 12345)

    if(sys.argv[1] == "push"):
        send_file(s, sys.argv[2])
    if(sys.argv[1] == "pull"):
        receive_file(s, sys.argv[2])
    if(sys.argv[1] == "ledger"):
        get_ledger(s)

    s.close()

main()
