# first of all import the socket library
import socket
import signal
import sys
import os
import time
import helperFunctions as helper
import ledgerFunctions as ledger
import lock

import threading
from _thread import *

#
# SERVER ERRORS
# 100 - Invaalid client request
# 102 - File doesnt exist on server
# 123 - Lock failure, server currently locked and cannot perform write/update
# 124 - Lock failure, server already locked by another client
# 125 - Lock failure, server not locked before write
# 126 - Lock failure, server not locked before ledger update
#

# macro for min bytes
BYTES_TO_SEND = 1024
CLIENTS_ALLOWED = 5
REQUEST_MAX_LENGTH = 100

# global socket declaration
s = socket.socket()

#
# Catch the ctrl+c signal
#
def handle_interrupt():
    s.close()
    print("  Server out...")
    sys.exit(0)

#
# Function to establish connection and send or recieve file
#
def run_server():

    # starting up server
    print("Starting up server.....")

    # reserve a port on your computer
    port = 12345

    # get the current hostname and ip
    hostName = socket.gethostname()
    hostIp = socket.gethostbyname(hostName)

    # bind the port with the socket
    s.bind(("", port))
    print("Server running on", port)

    # put the socket into listening mode to connect
    s.listen(CLIENTS_ALLOWED)
    print("Socket is listening")

    # a forever loop until we interrupt it or error occurs
    while True:


        # establish connection with client.
        c, addr = s.accept()

        # terminal output
        print("*************************************")
        print('Got connection from', addr)

        # recieve request and call relevant function
        ip = str(addr[0])
        start_new_thread(get_request, (c,ip))

        # terminal output
        print("*************************************")

#
# Function to check request format
#
def check_request(request):

    # should be able to convert to string
    try:
        str(request)
    except:
        return False

    # have to have at most two strings separated
    if (len(request.split()) != 2):
        return False

    # have only pull or push request
    if (request.split()[0].lower() not in ["pull", "push", "pull_ledger", "update_ledger", "lock"]):
        return False

    return True

#
# Send error to client
#
def send_error(c, errorMessage):
    error = helper.pad_string(errorMessage)
    c.send(error.encode())
    print(error)

#
# Function to recieve requests from the client
#
def get_request(c, ip):

    # read the request from the client
    request = c.recv(REQUEST_MAX_LENGTH).decode()

    # check error and send back if error
    if (check_request(request) == False):
        send_error(c, "Error 100: Invalid request format from client")
        return

    # get type and filename from request
    [requestType, filename] = str(request).lower().split()

    # send request
    if (requestType == "pull"):
        send_file(c, filename)

    # recieve request
    elif (requestType == "push"):
        receive_file(c, filename, ip)

    # send a copy of the ledger to the client
    elif (requestType == "pull_ledger"):
        send_ledger(c, ip)

    # send a copy of the ledger to the client
    elif (requestType == "update_ledger"):
        update_ledger(c, filename, ip)

    elif (requestType == "lock"):
        lock_server(c, ip)

#
# Lock a server to prevent multiple writes from occuring at the same time
#
def lock_server(c, ip):
    if lock.unlocked():
        lock.acquire(ip)
        print("Server locked by ", ip)
        c.send(helper.pad_string("Server locked").encode())
    else:
        send_error("Error 124: Server already locked")

#
# Function to update the ledger with the new stuff to the client
#
def update_ledger(c, filename, ip):

    if(ip == helper.find_ip()):
        print("Same server as client")
        c.send(helper.pad_string("Server doesnt need your ledger").encode())
        if lock.locked():
            lock.release()
        return

    if lock.locked() and not lock.check_lock(ip):
        send_error(c, "Error 123: Server currently busy")
        return

    # start with the time
    start = time.time()

    # open a temporary file to store the received bytes
    file = open(filename, 'wb')
    byte = 0

    # send confirmation
    c.send(helper.pad_string("Server is ready to update its ledger").encode())

    while True:

        # receive 1024 bytes at a time and write them to a file
        bytes = c.recv(BYTES_TO_SEND)
        file.write(bytes)
        byte += BYTES_TO_SEND

        # break infinite loop once all bytes are transferred
        if not bytes:
            break

    # close the file once transfer is complete
    file.close()

    # time and space prints
    end = time.time()
    print("Finished running download of file %s in %.2f seconds" % (filename, float(end - start)))
    print(byte, "bytes sent")

    # Release the lock if one is present
    if lock.locked() and lock.check_lock(ip):
        print("Server lock released by ", lock.return_lock())
        lock.release()

#
# Function to send the ledger to the new client
#
def send_ledger(c, ip):

    start = time.time()

    # open the ledger if it exists
    try:
        f = open(ledger.LEDGER_PATH, 'rb')
    except:
        send_error(c, "Error 176: Ledger doesn't exist on server machine")

        c.close()
        return

    # send confirmation
    c.send(helper.pad_string("Server is ready to send ledger").encode())

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

    # time and space prints
    end = time.time()
    print("Sent ledger in %.2f seconds" %  float(end - start))
    print(byte, "bytes sent")

    # close the connection with the client
    c.close()

#
# Function to send out bytes of data from filename
#
def send_file(c, filename):

    start = time.time()

    # opening a file if possible
    try:
        f = open("fico/" + filename, 'rb')
    except:
        send_error(c, "Error 102: File doesn't exist on server machine")

        c.close()
        return

    # send confirmation
    c.send(helper.pad_string("Server is ready to send file").encode())

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

    # time and space prints
    end = time.time()
    print("Finished running download of file in %.2f seconds" %  float(end - start))
    print(byte, "bytes sent")

    # Close the connection with the client
    c.close()

#
# Receives a file
#
def receive_file(c, filename, ip):

    if lock.locked() and not lock.check_lock(ip):
        send_error(c, "Error 123: Server currently busy")
        return

    if lock.unlocked():
        send_error(c, "Error 125: Server needs to be locked before write")
        return

    start = time.time()

    # open a temporary file to store the received bytes
    try:
        file = open("fico/" + filename, 'wb')
    except:
        os.system("mkdir fico")
        file = open("fico/" + filename, 'wb')

    byte = 0

    # send confirmation
    c.send(helper.pad_string("Server is ready to recieve file").encode())

    while True:

        # receive 1024 bytes at a time and write them to a file
        bytes = c.recv(BYTES_TO_SEND)
        file.write(bytes)
        byte += BYTES_TO_SEND

        # break infinite loop once all bytes are transferred
        if not bytes:
            break

    # close the file once transfer is complete
    file.close()

    # time and space prints
    end = time.time()
    print("Finished running download of file %s in %.2f seconds" % (filename, float(end - start)))
    print(byte, "bytes sent")


try:
    # calls the main function to run the server
    run_server()

# handling the keyboard interrupt
except KeyboardInterrupt:
    handle_interrupt()
