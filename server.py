import socket
import threading
import json
import random

memory_map = {}  # creating dict datastructure
currentDir = ""  # stores the current directory name
fileObj1 = [5]
fileObj = ""  # stores the opened file name
fmode = ""  # stores the mode in which the file is opened (r, w)
PageSize = 4096  # page table size = 4K bytes
Address = 12986

IP = ""  # keeping empty string for server
PORT = 95  # required port
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
SERVER_DATA_PATH = "server_data"

# Creating 2 counting Semaphores
""" this semaphore is used to make sure user can access only 2 files at a time"""
file_access = threading.Semaphore(5)
""" user_access semaphore is used to allow only 3 users to access a file"""
user_access = threading.Semaphore(5)

user = ["", "", ""]  # user list to store the names of active users
count = 0
count_user = 0

# Create File Method
def create(fName):

    global currentDir, Address, PageTSize, obj

    addr = Address * random.randint(1, 99)
    p_no = addr / PageSize
    p_no = round(p_no)

    offset = addr % PageSize
    starting_address = addr - offset

    # check if the file already exists
    if currentDir == '':
        if memory_map.get(fName, 0) != 0:
            return "Ok? File " + fName + " already exists!"

        else:
            memory_map[fName] = {
                "File Size": 0,
                "File Data": "",
            }
            return "OK? File " + fName + " created Successfully!\n"

    else:
        if memory_map[currentDir].get(fName, 0) != 0:
            return "Ok? File " + fName + " already exists!"

        else:
            memory_map[currentDir][fName] = {
                "File Size": 0,
                "File Data": "",
            }
            return "OK? File " + fName + " created Successfully!\n"
        

# Delete File Method
def delete(fName):
    global fileObj, currentDir
    y = None

    if currentDir == "":
        x = memory_map.get(fName, 0)
    else:
        x = memory_map[currentDir].get(fName, 0)
        y = 0

    if x == 0:
        return "OK? File " + fName + " not Found!"
    else:
        if y == 0:
            del memory_map[currentDir][fName]
        
        else:
            del memory_map[fName]  # deletes the given file
        
        fileObj = ""
        return "OK? File " + fName + " deleted Successfully!\n"


# Make Directory Method
def mkDir(dirName):
    if currentDir == "":
        memory_map[dirName] = {}  # creating an empty directory
        return "OK? Directory " + dirName + " created Successfully!\n"
    else:
        memory_map[currentDir] = {
            dirName: {}
        }  # creating an empty directory (nested dictionary)
        return "OK? Directory " + dirName + " created Successfully!\n"


# Change Directory Method
def chDir(dirName):
    global currentDir
    
    currentDir = dirName
    return "OK? Current Directory -> " + currentDir + '\n'


# Move file method: Moving a file from main structure to some other directory and hence not in its sub directory
def move(fName, dirname):
    if currentDir == "":
        memory_map[dirname][fName] = memory_map.pop(
            fName
        )  # by removing from original memory map and putting in desired directory
        return "OK? File " + fName + " moved Successfully!"
    
    else:
        memory_map[dirname][fName] = memory_map[currentDir].pop(
            fName
        )  # by removing from original memory map and putting in desired directory
        return "OK? File " + fName + " moved Successfully!"


# Open FIle Method
def Open(fName, mode, username):
    # while True:
    global user_access, file_access, count, count_user, user
    global fileObj, fmode

    temp = "OK? "  # used to print output on client side

    # if its the first user
    if fileObj == "":
        if user[0] == "":
            # initializing 1st user
            user[0] = username
            count_user += 1

    # if the other user wants to access the same file
    if fName == fileObj:
        if user[1] == "":
            # initializing 2nd user
            user[1] = username
            count_user += 1

        elif user[2] == "":
            # initializing 5RD user
            user[2] = username
            count_user += 1

    if count_user <= 5:
        user_access.acquire()  # wait()
        temp = open_func(fName, mode, temp)

    return temp


def open_func(fName, mode, temp):
    global count, file_access, fileObj, fmode, currentDir

    # get() method will return 0 if fName (given as key) does not exist,
    # else it will return the values of fName(key)
    y = None
    if currentDir == "":
        x = memory_map.get(fName, 0)
    else:
        x = memory_map[currentDir].get(fName, 0)
        y = 0
    # temp = 'OK? '

    count += 1
    if count <= 5:
        file_access.acquire()  # wait()

        # check if the file exists
        if x == 0:
            temp += fName + " not Found!!"
        else:

            if mode == "r":
                fileObj = fName  # initialize the file object
                fmode = mode  # initialize the fmode
                temp += fName + " is opened in Read Mode!\n"

            elif mode == "w":
                fileObj = fName  # initialize the file object
                fmode = mode  # initialize the fmode
                temp += fName + " is opened in Write Mode!\n"

            else:
                # file is not opened
                temp += "Error: Invalid Mode"
    else:
        temp += "Error: cannot access more than 5 files\n"
    return temp


# CLose File Method
def close(fName, username):
    global fileObj, user_access, file_access, count, count_user, user

    # file object is empty, then it is not initialized by open method,
    # which means that the file is not opened
    if fileObj == "":
        return "OK? No File opened"
    else:
        if fileObj == fName:
            count_user -= 1  # decrement user count
            user_access.release()
            user[count_user - 1] = ""

        # if the file is opened, close it by empting the fileObj
        fileObj = ""

        file_access.release()  # releasing the file
        count -= 2
        return "OK? " + fileObj + " closed Successfully!\n"


# Write to File Method (Append Mode)
def write_to_file(text):
    global fileObj, fmode, currentDir

    # check if a file is opened
    if fileObj == "" or fmode == "r":
        return "OK? Error: Invalid file mode or Deleted file"

    else:
        if currentDir == '':
            # append the text at the end
            # the file's index 1 stores the file content/data
            memory_map[fileObj]["File Data"] += text

            # the file's index 0 stores the file size
            memory_map[fileObj]["File Size"] += len(text)
            # print("File Written Successfully\n")
            return "OK? File Written Successfully\n"

        else:
            # append the text at the end
            # the file's index 1 stores the file content/data
            memory_map[currentDir][fileObj]["File Data"] += text

            # the file's index 0 stores the file size
            memory_map[currentDir][fileObj]["File Size"] += len(text)
            # print("File Written Successfully\n")
            return "OK? File Written Successfully\n"


# Write to File Method (At Specified Location)
def Write_to_file(write_at, text):
    global fileObj
    write_at = int(write_at)

    # check if a file is opened
    if fileObj == "" or fmode == "r":
        return "OK? Error: No file is Opened for writing"

    else:
        # overwrite the text at specified location
        # the file's index 1 stores the file content/data
        if currentDir == '':
            temp = memory_map[fileObj]["File Data"]
        else:
            temp = memory_map[currentDir][fileObj]['File Data']
        x = ""
        # creating new string
        for i in range(0, int(write_at)):
            x += temp[i]

        for i in range(0, len(text)):
            x += text[i]

        if currentDir == '':
            # re-assigning new content to the file
            memory_map[fileObj]["File Data"] = x

            #  stores the file size
            memory_map[fileObj]["File Size"] = len(x)
            return "OK? File Written Successfully\n"
        
        else:
            # re-assigning new content to the file
            memory_map[currentDir][fileObj]["File Data"] = x

            #  stores the file size
            memory_map[currentDir][fileObj]["File Size"] = len(x)
            return "OK? File Written Successfully\n"


# Read from File (Sequential Access)
def read_from_file():
    global fileObj

    # check if a file is opened
    if fileObj == "" or fmode == "w":
        return "OK? Error: No file is Opened for reading"
    else:
        if currentDir == '':
            # read the whole content of file
            print(memory_map[fileObj]["File Data"])
            return memory_map[fileObj]["File Data"]
        else:
            print(memory_map[currentDir][fileObj]["File Data"])
            return memory_map[currentDir][fileObj]["File Data"]


# Read from File (Specified # of bytes)
def Read_from_file(start, size):
    global fileObj
    file_bytes = int(memory_map[fileObj]["File Size"]) if currentDir == '' else int(memory_map[currentDir][fileObj]["File Size"])
    size = int(size)
    start = int(start)

    # checks to ensure user enters valid size and starting location
    if (abs(size - start) > file_bytes) or (size < 0) or (size > file_bytes):
        return "OK? Error: Invalid Size"

        if (start > file_bytes) or (start < 0):
            return "OK? Error: Invalid Starting address"
    else:
        # check if a file is opened
        if fileObj == "" or fmode == "w":
            return "OK? Error: No file is Opened for reading"
        else:
            if currentDir == '':
                temp = memory_map[fileObj]["File Data"]
            else:
                temp = memory_map[currentDir][fileObj]["File Data"]
            
            return 'OK? ' + temp[start:start+size]

# truncate file method
def truncateFile(size=0):
    global fileObj, currentDir
    size = int(size)

    # check if a file is opened
    if fileObj == "":
        return "OK? Error: No file is Opened"
    else:
        if currentDir == '':
            temp = memory_map[fileObj]["File Data"]
        
        else:
            temp = memory_map[currentDir][fileObj]['File Data']

        x = ""

        for i in range(0, size):
            x += temp[i]

        if currentDir == '':
            # re-assigning new content to the file
            memory_map[fileObj]["File Data"] = x

            # the file's index 0 stores the file size
            memory_map[fileObj]["File Size"] = len(x)
        
        else:
            # re-assigning new content to the file
            memory_map[currentDir][fileObj]["File Data"] = x

            # the file's index 0 stores the file size
            memory_map[currentDir][fileObj]["File Size"] = len(x)
    
        print("Success: File Truncated\n")
        return "OK? Success: File Truncated\n"


# Show Memory Map
def show_memory_map():
    formatted = json.dumps(memory_map, indent=4)
    return formatted


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    conn.send("OK?Welcome to Distributed File Management System".encode(FORMAT))

    while True:
        line = conn.recv(SIZE).decode(FORMAT)
        line = line.split("?")
        func = line[0]

        if func == "touch":
            fName = line[1]
            data = create(fName)
            conn.send(data.encode(FORMAT))

        elif func == "rm":
            fName = line[1]
            data = delete(fName)
            conn.send(data.encode(FORMAT))
        elif func == "mkdir":
            dirName = line[1]
            data = mkDir(dirName)
            conn.send(data.encode(FORMAT))
        elif func == "cd":
            dirName = line[1]
            data = chDir(dirName)
            conn.send(data.encode(FORMAT))

        elif func == "mv":
            # For moving the file from src to dest.
            fname = line[1]
            dirName = line[2]
            data = move(fname, dirName)
            conn.send(data.encode(FORMAT))

        elif func == "open":
            fName = line[1]
            mode = line[2]
            username = line[3]
            data = Open(fName, mode, username)
            conn.send(data.encode(FORMAT))

        elif func == "close":
            fName = line[1]
            username = line[2]
            data = close(fName, username)
            conn.send(data.encode(FORMAT))

        elif func == "append":
            text = line[1]
            data = write_to_file(text)
            conn.send(data.encode(FORMAT))

        elif func == "write":
            pos = line[1]
            text = line[2]
            data = Write_to_file(pos, text)
            conn.send(data.encode(FORMAT))

        elif func == "cat":
            data = "OK? "
            data += read_from_file()
            conn.send(data.encode(FORMAT))

        elif func == "catfrom":
            start = line[1]
            size = line[2]
            data = Read_from_file(start, size)
            conn.send(data.encode(FORMAT))

        elif func == "truncate":
            data = truncateFile()
            conn.send(data.encode(FORMAT))

        elif func == "mmap\n" or func == "mmap":
            datax = "OK?" + show_memory_map()
            conn.send(datax.encode(FORMAT))
        elif func == "exitserver":
            break

        j = json.dumps(memory_map)
        with open("file1.dat", "w", encoding="utf-8") as f:
            f.write(j)
            f.close()

    print(f"[DISCONNECTED] {addr} disconnected")
    conn.close()


def main():
    print("[STARTING] Server started")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print(f"[LISTENING] Server listening on {IP}:{PORT}.")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
