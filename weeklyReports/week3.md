<!-- # Security Stuff

*New Nodes can be added using a known ip address and an id associated to it, already in the network.
		This protects from attackers who connect to the LAN using some form of social engineering.
		They are not able to add themselves as nodes and pollute the network.

	All communication between a server and the client are encrypted.
		We are using a public-private key encryption system, to encrypt communication and files why they are sent
		This allows any non authenticated user to not be able to make requests to any of the nodes
		Also this allows attackers who are reading the data in the network to not be able to make sense dude to encryption



Tasks
	Encryption
	Sharding
		dividing file into parts (1st to 6th)
	Read or write
	Server Threading For Availabilty
	Locking of servers in write for consistency
 -->

# NAS: Week 3

Last Week:

* Implemented sharding (A)
	* File create now distributes files into pieces and sends it to all the Nodes
	* Necessary updates to ledger occurs while this happens

* UI changes (A)
	* Created a file system UI that can read all the files from the directory and show if it has been updated on the network or not

* Work on Encryption (S)
	* Since RSA module operates on bytes and not strings, encoded the message to be sent in UTF-8
	* Performed encryption using public key and decryption using private key on a message

* Implemented server side locking for writes. (N)
	* Created a library for lock related functions that can block server access to additional reads and writes while a write is taking place.
	* Modified server and client code to work with new locking functionality.

* Implemented multithreaded sockets for servers. (N)
	* Now allows servers to accept multiple requests at the same time.
	* Integrated with locks, so clients receive a "server busy" response when another client has locked the server.

Next Week:

* Implement reads from sharding (N)
* Completely incorporate encryption in message sending and as well as file data using public and private keys (S)
* Finish the UI so that it can be used seamlessly (A)
* Maybe start working on load balancing (N, A)


Problems Faced:

* Design implementation was difficult as we had to try and understand which parts of CAP theorem to incorporate. We chose to focus on consistency and availability for our network. Hopefully we know what we are doing.
* RSA can only encrypt messages that are smaller than the key, so have to read data key size at a time and encrypt it.
* Adding custom columns to in our file system UI required class overloading and reading a lot of documentation.


**Note : N = Neil, A = Aakaash, S = Sutej**
