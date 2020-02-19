# NAS: Week 2

Last Week:
* Added new node functionality to the network (N, A)
    * Created a client and server API for the creation of a new node to synchronize it throughout the entire network. (N)
    * API supports both addition of a new node to the network and also sending updates to the entire network. (N, A)
    * Created a helper library for all ledger related functions, which include local modification and parsing. (A)
* GUI Application that interfaces with the server and client-side libraries (S)
	* Tried to create a GUI using Tkinter Python framework, failed due to a bug in macOS (S)
	*  Created a graphical user interface using PyQT, a python GUI framework, and added features such as submit buttons, time API’s, text entries etc. (S)

Next Week:
* We will focus on allowing sharding of files and allowing a user to send files to every node in the network. (N, S)
* Reading files will be allowed only to the user who owns it (A)
* Maybe allow writes

Problems:
* Tkinter was very buggy and made us change our python framework.
* Design decisions for server client communication took some time to finalize.

Trello:
https://trello.com/b/g4gOwG0G/nas

Commits:
Commits can be accessed in the commits section of the repository

**Note : N = Neil, A = Aakaash, S = Sutej**
