import socket
REQUEST_MAX_LENGTH = 100

#
# Pad a request string to REQUEST_MAX_LENGTH
# message => String
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


# 
# Returns an array of split up byte strings into 
# data => ByteString
# nodes => Int
# eg splitData("abcd", 2) = ["ac", "bd"]
#
def splitData(data, nodes):

	# declaring the output array
	outputArray = []

	# going over the number of nodes to create each string
	for num in range(nodes):

		# temporary byte string
		temp_string = "".encode()

		# going over the byte string skipping nodes num of characgers
		for byte_num in range(num, len(data), nodes):

			# adding this byte slice or byte char
			temp_string += data[byte_num:(byte_num + 1)]

		# appending to the array
		outputArray.append(temp_string)

	# array of length, nodes
	return outputArray

# 
# Returns a byte string from a split up array
# data_array => ByteString Array
# eg retrieveData(["ac", "bd"]) = "abcd" 
#
def retrieveData(data_array):

	# declaring the output bytestring
	outputData = "".encode()

	# going over each byte char
	# first element will always be the longest
	for byte_num in range(len(data_array[0])): 

		# going over the array
		for byte_string in data_array:

			# checking if length not exceeded
			if(byte_num < len(byte_string)):

				# add it to the output
				outputData += byte_string[byte_num:byte_num+1]

	# byte string with all the data
	return outputData

