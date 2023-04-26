# Client-Server-FMS

A file management server used in a distributed file management system, which has been constructed through the use of both threads and socket programming. The system is designed to accommodate multiple users and it has been properly synchronized. Measures have been taken to protect the files from any reader-writer conflicts.

## About the Program

The server program will receive the message through socket, execute the task and return the response. The client side program will provide an interface to the user where different operations can be executed and results shown.

-> Multiple users can access the system. <br>
-> Any user may not be able to access more than 5 files at one time. <br>
-> If more than 5 requests are placed then the requesting thread must wait. <br>
-> Each file can only be accessed by 3 users, be it for read or write. <br>

## Program Functionalities

-> We have two programs, a server and a client.
-> The client allows the user to specify the IP address of the server at the time of connection.
-> The client allows the user to first specify the user name at the connection setup time and all communication should display it.
-> The client provides an interface to apply the operations like create, delete, move, open, close, truncate, change directory, make directory etc.
-> The client gives errors when the server is not available.
-> The client displays the response of the actions performed.
-> The server responds to multiple requests at the same time using threads.
-> The server binds to port 95 whereas the client port can be any number higher than 1024. 
-> The server and clients can run on different machines.

## Group Members

● Hafsa Malik (341303) <br>
● Syeda Fatima Shahid (337346)

