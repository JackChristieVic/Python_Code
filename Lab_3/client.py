#!/usr/bin/python
import socket, sys, time, os
from shutil import copyfile

# The port used by the server  
host = sys.argv[1]
port = int(sys.argv[2])
cmd = sys.argv[3]
f_name = sys.argv[4]


# socket.AF_INET: IPv4, ocket.AF_INET6: IPv6
c_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# c_soc is a socket used to send data to the server
c_soc.connect( (host, port) )

# when the connection is established, server sends out "READY" to clienb, 
# and client receives it from server
response = ( c_soc.recv(1024).decode("utf-8") )
#print( str(response) )

if(response == "READY"):
    # if it's "READY", then client will be sending cmd & file name to server
    cmd_out = (cmd + " " + f_name).encode("utf-8")
    c_soc.send(cmd_out)

    # client receives data from server, creates a file and write date to it
    if cmd == 'GET':
        c_OK = c_soc.recv(1024).decode("utf-8") 
        if c_OK == "OK":
            d_ready = ('READY').encode('utf-8')
            c_soc.send(d_ready)
            
            f_size = int.from_bytes(c_soc.recv(1024), byteorder='big', signed='False' )
            # print("int(f_size) ====>",int(f_size))
            f_OK = ('OK').encode('utf-8')
            c_soc.send(f_OK)

            print("client receiving file " +  f_name + " (" + str(f_size) + " bytes)" )
            
            content_to_file = open(f_name,"wb")
            f_size_counter = 0
            
            while f_size_counter < int(f_size):
                content_remainder = int(f_size) - f_size_counter
                if content_remainder < 1024:
                    content = c_soc.recv(content_remainder)
                    # content_to_file.write(content)
                else:
                    content = c_soc.recv(1024)
                content_to_file.write(content)
                f_size_counter = f_size_counter + len(content)
            content_to_file.close()

            DONE = c_soc.recv(1024).decode()
            if DONE == 'DONE':
               print("Complete")

    elif cmd == 'PUT':
        c_OK = c_soc.recv(1024).decode("utf-8")
        if c_OK == 'OK':
            cur_dir = os.getcwd()
            file_dir = os.path.join(cur_dir, f_name)
            f_size = str(os.path.getsize(file_dir))
            print("client sending file " +  f_name + " (" + str(f_size) + " bytes)" )
            c_soc.send(f_size.encode())
            #print("C, ===> f_size:", f_size)

            e_OK = c_soc.recv(1024).decode('utf-8')
            #print("E, ===> e_OK", e_OK)
            if e_OK == 'OK':
                a_file = open(file_dir, "rb")
                #print("E, ===> e_OK", e_OK)

                f_size_counter = 0
                
                while f_size_counter < int(f_size):
                    #print("0, ===> client sending file " +  f_name + " (" + str(f_size) + " bytes)" )
                    content_remainder = int(f_size) - f_size_counter
                    #print("1, ===> content_remainder: ", content_remainder)
                    if content_remainder < 1024:
                        content = a_file.read(content_remainder) 
                        #print( "2, ===> size of content: ",len(content) )
                    else:
                        content = a_file.read(1024)
                        #print("3, ===> content", len(content) )
                    c_soc.send(content)
                    f_size_counter = f_size_counter + len(content)
                    #print("4, ===> f_size_counter", f_size_counter)
                
                a_file.close()
                #print("a_file is close")

            DONE = c_soc.recv(1024).decode('utf-8')
            if DONE == "DONE":
                print("Complete")
    elif cmd == 'DEL':
        c_soc.send(cmd_out)
        print("client deleting file " +  f_name )

        DONE = c_soc.recv(1024).decode('utf-8')
        if DONE == "DONE":
            print("Complete")

c_soc.close()
