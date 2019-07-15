import socket, sys, os
port = int(sys.argv[1])

# get the full path of current directory
#               cur_dir = os.getcwd()
# get the full path of the file.
#               file_dir = os.path.join(cur_dir, cmd_f_name)
# get the size of the file
 #               f_size = str(os.path.getsize(file_dir)).encode('utf-8')
            

# Create the socket object using STREAM
s_soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_soc.bind( ("", port) )
s_soc.listen(5) # 5 is number of request in the queue

while True:
    c_soc, addr = s_soc.accept()
    connected = ('Got connection from', addr)
    if (connected):
        response = ('READY').encode("utf-8")
        c_soc.send(response)  
   
    cmd = c_soc.recv(1024).decode("utf-8")
    # print("1, cmd ===>",cmd)
    cmd_splitted = cmd.split()
    cmd_verb = cmd_splitted[0]
    # print("2, cmd_verb---", cmd_verb)
    cmd_f_name = cmd_splitted[1]
    # print("3, cmd_f_name===>", cmd_f_name)

    if cmd_verb == "GET":
        if cmd == cmd_verb  + " " + cmd_f_name:
            c_OK = ('OK').encode('utf-8')
            c_soc.send(c_OK)
        
            d_ready = c_soc.recv(1024).decode('utf-8')
            
            if d_ready == "READY":
                cur_dir = os.getcwd()
                file_dir = os.path.join(cur_dir, cmd_f_name)
                f_size = (os.path.getsize(file_dir))
                c_soc.send(f_size.to_bytes(8, byteorder ='big', signed='False'))
                f_OK = c_soc.recv(1024).decode("utf-8")

                if f_OK == "OK":   
                    a_file = open(file_dir, "rb")
                
                f_size_counter = 0
                
                while f_size_counter < int(f_size):
                    content_remainder = int(f_size) - f_size_counter 
                    if content_remainder < 1024:
                        content = a_file.read(content_remainder) 
                    else:
                        content = a_file.read(1024)
                    c_soc.send(content)
                    f_size_counter = (f_size_counter + len(content))
                a_file.close()
        
                DONE = ("DONE").encode()
                if int(f_size) - f_size_counter == 0: 
                    c_soc.send(DONE)

    elif cmd_verb == 'PUT':
        if cmd == cmd_verb  + " " + cmd_f_name:
            c_OK = ('OK').encode('utf-8')
            c_soc.send(c_OK)
            #print("0, cmd --|", cmd)
            #print("1, c_OK ===>")
        
            f_size = c_soc.recv(1024).decode('utf-8')
            if(f_size):
                e_OK = ('OK').encode('utf-8')
                c_soc.send(e_OK)
            #print("2, f_size ----|",f_size)

            content_to_file = open(cmd_f_name,"wb")
            #print("client sending file " +  cmd_f_name + " (" + f_size + " bytes)" )

            f_size_counter = 0

            while f_size_counter < int(f_size):
                content_remainder = int(f_size) - f_size_counter
                #print("4, content_remainder ---->", content_remainder)
                #content_0 = c_soc.recv(content_remainder)
                # print("4.1 content_remainder ------------>", len(content_0) )

                if content_remainder < 1024:
                    content = c_soc.recv(content_remainder)
                    content_to_file.write(content)
                    #print("5, content size =========>", len(content))
                else:
                    content = c_soc.recv(1024)
                    #print("6, content size ------------>", len(content))
                    content_to_file.write(content)
                f_size_counter = f_size_counter + len(content)
            #print("7, f_size_counter ===============>", f_size_counter)
            content_to_file.close()
            #print("8, ------------------------------------>file closed")
            DONE = ('DONE').encode('utf-8')
            if int(f_size) - f_size_counter == 0: 
                c_soc.send(DONE)
            #print("9, =======================================>the whole thing is done")

    elif cmd_verb == 'DEL':
        if cmd == cmd_verb  + " " + cmd_f_name:
            os.remove(cmd_f_name)
            DONE = ('DONE').encode('utf-8')
            c_soc.send(DONE)

    c_soc.close()
    