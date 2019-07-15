import sys, socket, threading, collections, time, os

# Create the socket object using STREAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(sys.argv[1])
server.bind( ("", port) )
server.listen(5)

class ClientHandler(threading.Thread):
    def __init__(self, client, addr):
        threading.Thread.__init__(self)
        self.client = client
        self.addr = addr
        
    def run(self):
        # Copy code from Lab 3 server, from first line that sends "READY" to the client. Note that
        # you must use "self.client.send()" instead of "client.send()".
        #_^.^_ ------------------------code from Lab 3------------------------------------------------
        #_^.^_ I used s_soc.send() in Lab 3, so I changed it to self.client.send/recv() in this Lab
        connected = ('Got connection from', addr)
        if (connected):
            response = ('READY').encode("utf-8")
            self.client.send(response)  
    
        cmd = self.client.recv(1024).decode("utf-8")
        cmd_splitted = cmd.split()                      
        cmd_verb = cmd_splitted[0]              #_^.^_ cmd_verb will be GET, PUT, DEL, but from the command line
        cmd_f_name = cmd_splitted[1]            #_^.^_ .. .. .. .. .. ..test.txt, panda.jpg, or whatever

        if cmd_verb == "GET":
            if cmd == cmd_verb  + " " + cmd_f_name:
                c_OK = ('OK').encode('utf-8')
                self.client.send(c_OK)
            
                d_ready = self.client.recv(1024).decode('utf-8')
                
                if d_ready == "READY":
                    cur_dir = os.getcwd()                       #_^.^_ get the current directory
                    file_dir = os.path.join(cur_dir, cmd_f_name)#_^.^_ get file directory by concatenating
                    f_size = (os.path.getsize(file_dir))        #_^.^_ get file size using getsize() from os.path modude
                    
                    # sends the size of file to client in byte array
                    self.client.send(f_size.to_bytes(8, byteorder ='big', signed='False'))
                    f_OK = self.client.recv(1024).decode("utf-8")

                    if f_OK == "OK":   
                        a_file = open(file_dir, "rb")           #_^.^_ open a file, write in binary(ie:rb)
                    
                    f_size_counter = 0
                    
                    while f_size_counter < int(f_size):
                        content_remainder = int(f_size) - f_size_counter 
                        if content_remainder < 1024:
                            content = a_file.read(content_remainder) 
                        else:
                            content = a_file.read(1024)
                        self.client.send(content)
                        f_size_counter = (f_size_counter + len(content))
                    a_file.close()
            
                    DONE = ("DONE").encode()
                    if int(f_size) - f_size_counter == 0: 
                        self.client.send(DONE)

        elif cmd_verb == 'PUT':
            if cmd == cmd_verb  + " " + cmd_f_name:
                c_OK = ('OK').encode('utf-8')
                self.client.send(c_OK)
            
                f_size = self.client.recv(1024).decode('utf-8')
                if(f_size):
                    e_OK = ('OK').encode('utf-8')
                    self.client.send(e_OK)

                content_to_file = open(cmd_f_name,"wb")

                f_size_counter = 0

                while f_size_counter < int(f_size):
                    content_remainder = int(f_size) - f_size_counter
                    if content_remainder < 1024:
                        content = self.client.recv(content_remainder)
                        content_to_file.write(content)
                    else:
                        content = self.client.recv(1024)
                        content_to_file.write(content)
                    f_size_counter = f_size_counter + len(content)
                content_to_file.close()
                DONE = ('DONE').encode('utf-8')
                if int(f_size) - f_size_counter == 0: 
                    self.client.send(DONE)

        elif cmd_verb == 'DEL':
            if cmd == cmd_verb  + " " + cmd_f_name:
                os.remove(cmd_f_name)
                DONE = ('DONE').encode('utf-8')
                self.client.send(DONE)

        self.client.close()
        ##_^.^_------------------------code from Lab 3------------------------------------------------

class Manager(threading.Thread):
    def __init__(self, max_connections):
        threading.Thread.__init__(self)     # ^.^ 
        self.max_connections = max_connections

        # Add data members for the running set and FIFO queue
        #_^.^_ using deque(), which is a method in the collections module. so import collections before using deque()
        #_^.^_ append(): appends items to right, appendleft(): appends items to left
        #_^.^_ popright(): removes items from right, popleft(): removes item from left

        self.q = collections.deque()  #_^.^_ create a data member named "q" and it's a deque object of collections module
        self.running = set()          #_^.^_ create a data member named "running" and it's a set object of collection module
                                      #_^.^_ Mathematically a set is a collection of items not in any particular order. 
                                      #_^.^_ A Python set is similar to this mathematical definition with below additional conditions.
                                      #_^.^_ The elements in the set cannot be duplicates.The elements in the set are immutable
                                      #_^.^_ but the set as a whole is mutable. There is no index attached to any element in
                                      #_^.^_ a python set. So they do not support any indexing or slicing operation.
                                      #_^.^_ set() have set.add() & set.discard() methods

    def add_client(self, t):
        # add t to the end of the FIFO queue
        self.q.append(t)              #_^.^_ append(): appends items to right
        
        
    def run(self):
        while True:
            # remove any finished threads from the running set
            
            # if there are threads waiting, and running set is
            # not full:
            #    - dequeue next threading: use popLeft() to 
            #    - start the threading
            #    - add the thread to the running set: look up add to the set method in python
            
            # wait for 1 second

            # check length of q, if lenggh of it > 0, then it means there is at least one client waiting in the q
            # check to make sure the running set is not full, then, 
            kick = []                       #_^.^_ create a list called kick which is a list of thread we want to remove out of the queue
            for t in self.running:           #_^.^_ if one thread is completed, but it's still in the set and the set is iterating
                if not t.isAlive():          #_^.^_ append it to the right end of kick[] list, and wait for the whole iteration to finish
                    kick.append(t)
            for t in kick:                   #_^.^_ when the iteration is finished, go throug the list of finished threads in the kick kist,
                                            #_^.^_ remove them using for-loop. t is a local variable, it has nothing to do with the t in def addlient.
                self.running.remove(t)      #_^.^_ remove the completed thread from the running set(),
                                            #_^.^_ running set is created above by self.running = set()

            self.lock = threading.Lock()    #_^.^_ Nov 29
            self.lock.acquire()             #_^.^_ Nov 29

            if len(self.running) < self.max_connections and len(self.q) > 0:
                t = self.q.popleft()        #_^.^_ returns the poped item to me, I store it in local variable t
                self.running.add(t)         #_^.^_ add the item to the running set using add() method of set()
                # self.lock.release()
                t.start()
            self.lock.release()             #_^.^_ Nov 29
            
            time.sleep(1)


        
# The main server thread starts here.
#_^.^_ MAIN SERVER THREAD is the server.py thread

# Create and start the manager
manager = Manager( int(sys.argv[2]) )
manager.start()

# Create the socket, bind() and listen()
#_^.^_ I did it at the very beginninb

while True:
    client, addr = server.accept()
    # Create the ClientHandler thread and add it to the manager
    client_handler = ClientHandler(client, addr)
    manager.add_client(client_handler)          #_^.^_ Manager puts its clients in the queue, then in its while loop,
                                                #_^.^_it controls when that client thread gets started


