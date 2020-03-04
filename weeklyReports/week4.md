# NAS: Week 4

Last Week:

* Implemented reads from sharded files across the network (N)
	* Files are now requested from each server by the client and downloaded one at a time.
	* Updated lock library to allow for reads even while a write is occurring.


* UI changes (A)
	* Allowed files to be read from the system to add to the network
	* Integrated UI with client functions


* Ledger Function changes (A)
	* Allowed for public key to be added to the ledger
	* Easy reads for the public keys from the client


* Encryption fixes
  * Encryption library now allows for:
    * creating and storing keys,
    * encrypting a message using a provided public key
    * decrypting an encrypted message using a private key stored locally on a system

Next Week:

* Start work on load balancing (N, A)
* Integrate encryption into the rest of the codebase (S)
* Work further on UI to account for all updates to the codebase


Problems Faced:

* Saving keys was slightly awkward because of the way the RSA library works

Trello: https://trello.com/b/g4gOwG0G/nas

**Note : N = Neil, A = Aakaash, S = Sutej**
