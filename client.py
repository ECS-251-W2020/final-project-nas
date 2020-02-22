import socket
import sys
import time
import helperFunctions as helper
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

    #return the socket once created
    return s

#
# Lock all servers
#
def lock_servers():

    # logging
    print("Locking All Servers")

    # go through the ips and lock them
    for ip in ledger.get_ips():

        # connect to the host you want to send file to
        s = run_client(ip)

        # create a push request for the server and encode it to bytes
        cmd = helper.pad_string("lock " + helper.find_ip())
        s.send(cmd.encode())

        # recieve response from server
        recv = s.recv(REQUEST_MAX_LENGTH).decode()

        # if error then stop
        if(recv.split()[0] == "Error"):

            # return false
            print(recv)
            return False

    # logging that we beginning to write 
    print("Began writing to all the files")
    print("******************************")
    print("******************************")

    # if everything goes smoothly
    return True



#
# Function to send out bytes of data from filename
#
def send_file(filename):

    # going to start locking all servers for a send file
    if(lock_servers() == False):
        return

    # opening a file in binary
    f = open(filename, 'rb')

    # getting all the data in a byte string
    byteString = f.read()

    # seperate it into files
    byteArray = helper.splitData(byteString, len(ledger.get_ips()))

    # going through the list of ips and making the request
    for index, ip in enumerate(ledger.get_ips()):

        # check if the ip is same as our ip
        if(ip == helper.find_ip()):

            # open a file to write
            f = open("fico/" + filename + str(index), "wb")

            # write to it
            f.write(byteArray[index])

            # move forward in the for loop
            continue

        # connect to the host you want to send file to
        s = run_client(ip, 12345)

        # create a push request for the server and encode it to bytes
        cmd = helper.pad_string("push " + filename + str(index))
        s.send(cmd.encode())

        # recieve response from server
        recv = s.recv(REQUEST_MAX_LENGTH).decode()

        # check if the servor responded with an error
        if(recv.split()[0] != "Error"):

            # get the string we want to send
            toSend = byteArray[index]

            # logging
            print("Starting to send", len(toSend),"bytes to", ip)

            # get the range of things to send at a time
            for i in range(0, len(toSend), BYTES_TO_SEND):

                # if its too big then only till the end
                if(i + BYTES_TO_SEND >= len(toSend)):
                    byte = toSend[int(i):]
                else:
                    byte = toSend[int(i):int(i + BYTES_TO_SEND)]

                # send the bytes
                s.send(byte)

            # logging
            print("Finished sending file")
            print("******************************")

        # server did respond with error
        else:
            print("Something went wrong")

        s.close()

    # logging end of command
    print("******************************")

    # updating the ledger locally
    ledger.add_file(filename, helper.find_ip())

    # sending the update ledger command to everyone
    update_ledger()


#
# Receives a file
#
def receive_file(filename):

    # connect to the host

    # create a pull request for the server and encode it to bytes
    cmd = helper.pad_string("pull " + filename)
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
def pull_ledger(ip):

    # connect to the ip
    s = run_client(ip)

    # create a new node request for the server and encode it to bytes
    cmd = helper.pad_string("pull_ledger ledger.json")
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
        s.close()
        return

    s.close()

    # Update ledger with ip of client
    ledger.add_node(helper.find_ip())

    # Send updated ledger to all serversin the network
    update_ledger()


#
# Sends a request to server for updating the ledger
#
def update_ledger():

    # logging
    print("******************************")
    print("******************************")
    print("Beginning to send updated ledger to all servers")

    # going through all the ips
    for ip in ledger.get_ips():

        # as long as is it is not our own ip
        if ip != helper.find_ip():

            # run the client
            s = run_client(ip)

            # create a push request for the server and encode it to bytes
            cmd = helper.pad_string("update_ledger ledger.json")
            s.send(cmd.encode())

            # recieve response from server
            recv = s.recv(REQUEST_MAX_LENGTH).decode()
            print(recv)

            # check if the servor responded with an error
            if(recv.split(' ', 1)[0] != "Error"):

                # opening a file
                f = open(ledger.LEDGER_PATH, 'rb')

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
                print("Something went wrong while updating the ledger to", s.gethostname())

    print("Finished sending the ledger to everyone")
    print("******************************")
    print("******************************")
#
# Deals with creating the client node as well as providing the main command line interface for the program
#
def main():

    if(sys.argv[1] == "push"):
        send_file(sys.argv[2])
    if(sys.argv[1] == "pull"):
        receive_file(sys.argv[2])
    if(sys.argv[1] == "pull_ledger"):
        pull_ledger(sys.argv[2])
    if(sys.argv[1] == "update_ledger"):
        update_ledger()

    # s.close()

main()
