import json
from os import path
from random import randint

# macros
LEDGER_PATH = "ledger.json"


# 
# Function to get a new random id
#
def get_new_id(data):

	# get a random number
	newID = str(randint(10000, 99999))

	# go through the data and check if it is a duplicate
	for node in data:

		# if matched then run again
		if (node["ID"] == newID):
			return get_new_id(data)

	# if all good
	return newID


#
# Function to add a node to the ledger file
#
def add_node(ip):

	# checks if ledger file exists
	if (path.exists(LEDGER_PATH) == False):
		return False

	# read the ledger file into a dictionary
	with open(LEDGER_PATH) as f:
		ledger = json.load(f)

	# create a new id for the user
	newID = get_new_id(ledger["Nodes"])

	# new node variable
	node = { "ID" : newID, "IP" : ip }

	# add it to the ledger
	ledger["Nodes"].append(node)

	# Serializing json  
	ledger_object = json.dumps(ledger, indent = 4) 

	# Writing to sample.json 
	with open(LEDGER_PATH, "w") as outfile: 
		outfile.write(ledger_object)


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
