import json
from os import path
from random import randint

# macros
LEDGER_PATH = "ledger.json"

#
# Function to add a node to the ledger file
#
def add_node(ip, pubKey):

	# checks if ledger file exists
	if (path.exists(LEDGER_PATH) == False):
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# new node variable
	node = {"IP" : ip, "Key" : pubKey}

	# add it to the ledger
	ledger["Nodes"].append(node)

	# Serializing json
	ledger_object = json.dumps(ledger, indent = 4)

	# Writing to sample.json
	with open(LEDGER_PATH, "w") as outfile:
		outfile.write(ledger_object)

#
# Function to add a node to the ledger file
#
def add_first_node(ip, pubKey):

	# read the ledger file into a dictionary
	ledger = {}

	# new node variable
	node = {"IP" : ip, "Key" : pubKey}

	# add it to the ledger
	ledger["Nodes"] = [node]

	# add en empty files list to the ledger
	ledger["Files"] = []

	# Serializing json
	ledger_object = json.dumps(ledger, indent = 4)

	# Writing to sample.json
	with open(LEDGER_PATH, "w") as outfile:
		outfile.write(ledger_object)


#
# Function to add a file to the ledger file
#
def add_file(filename, ownerIP):

	# checks if ledger file exists
	if (path.exists(LEDGER_PATH) == False):
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# new node variable
	file = { "Filename" : filename, "Owner IP" : ownerIP, "Shards" : get_ips()}

	# add it to the ledger
	ledger["Files"].append(file)

	# Serializing json
	ledger_object = json.dumps(ledger, indent = 4)

	# Writing to sample.json
	with open(LEDGER_PATH, "w") as outfile:
		outfile.write(ledger_object)

#
# Function that returns the shard fiename as stored on the server
#
def get_shard(filename, IP):

	# checks if ledger file exists
	if path.exists(LEDGER_PATH) == False:
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	return filename + str(get_ips().index(IP))


#
# Function to check if the filename is owned by the IP
#
def check_owner(filename, IP):

	# checks if ledger file exists
	if path.exists(LEDGER_PATH) == False:
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# check if client is the atual owner of the file
	for file in ledger["Files"]:
		if file["Filename"] == filename and file["Owner IP"] == IP:
			return True

	return False

#
# Function to get the list of ips from the ledger
#
def get_ips():

	# checks if ledger file exists
	if (path.exists(LEDGER_PATH) == False):
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# a list of just the ips
	ips = []

	# going through the data and getting all the ips
	for node in ledger["Nodes"]:
		ips.append(node["IP"])

	# returns the new list of ips
	return ips

