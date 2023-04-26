import socket

IP = socket.gethostbyname(socket.gethostname())
print(IP)
PORT = 95
ADDRESS = (IP, PORT)
FORMAT = "utf-8"
SIZE = 1024
limit = 4
user = 0

def main():

    # IP = "10.7.85.113"
    username = input("Enter username: ")
    ADDRESS = (IP, PORT)   # contains the IP and Port no. of the client
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDRESS)

    while True:
        data = client.recv(SIZE).decode(FORMAT)
        func, msg = data.split("?")
        
        # for closing the connection
        if func == "DISCONNECTED":
            print(f"[SERVER]: {msg}")
            break
        # for displaying the message from the server on the 
        # client side
        elif func == "OK":
            print(f"{msg}")

        data = input("==> ")
        data = data.split(" ")
        func = data[0]

        if func == "touch" :
            client.send(f"{func}?{data[1]}".encode(FORMAT))

        elif func == "rm" : 
            client.send(f"{func}?{data[1]}".encode(FORMAT))

        elif func == "mkdir" :
            client.send(f"{func}?{data[1]}".encode(FORMAT))

        elif func == "cd" :
            client.send(f"{func}?{data[1]}".encode(FORMAT))

        elif func == "mv" :
            client.send(f"{func}?{data[1]}?{data[2]}".encode(FORMAT))

        elif func == "open" :
            client.send(f"{func}?{data[1]}?{data[2]}?{username}".encode(FORMAT))

        elif func == "close" :
            client.send(f"{func}?{data[1]}?{username}".encode(FORMAT))

        elif func == "append" :
            client.send(f"{func}?{data[1]}".encode(FORMAT))

        elif func == "write" : 
            client.send(f"{func}?{data[1]}?{data[2]}".encode(FORMAT))

        elif func == "cat":
            client.send(func.encode(FORMAT))

        elif func == "catfrom":
            client.send(f"{func}?{data[1]}?{data[2]}".encode(FORMAT))

        elif func == "truncate":
            client.send(f"{func}".encode(FORMAT))

        elif func == "mmap\n" or func == "mmap" : 
            client.send(func.encode(FORMAT))

        elif func == "exitserver":
            client.send(func.encode(FORMAT))
            break
            

    print("Server Disconnected")
    client.close()
        

if __name__ == "__main__":
    main()