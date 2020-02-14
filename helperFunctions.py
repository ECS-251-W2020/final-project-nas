import socket

#
# Pad a request string to REQUEST_MAX_LENGTH
#
def pad_string(message):
    return message + ((REQUEST_MAX_LENGTH - len(message)) * ' ')

#
# Find the local IP address of a host
#
def find_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = str(s.getsockname()[0])
    s.close()
    return ip;


print(find_ip())