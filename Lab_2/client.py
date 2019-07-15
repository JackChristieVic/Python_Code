
import socket, sys

#--line 6 to 9 are on explanation for the cmd line when run client.py
# client.py = sys.argv[0]  # <---1st on cmd line, Python knows, so no initiation needed
host = sys.argv[1]         # <---2nd on cmd line
port = int(sys.argv[2])    # <---3rd on cmd line, 
operator = sys.argv[3]     # <---4th on cmd line
counter = len(sys.argv)-4  # <---NOT on cmd line, but it's one of packet in the packet bytearray   

# create the socket using DGRAM
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# establish connection between server.py and client.py
client_socket.connect((host, port))

client_packet = bytearray( 2 + (counter+1)//2 ) 
# ----------------start at 2,coz client_packet[0] -> operator
# -------------------------------client_packet[1] -> counter    
# -------------------------------counter = length of the sys.argv list - 4
# ex: python client.py localhost + 1 2 3 4 5, then I have 5 operands,  so counter == 5
# then, 2 + (5 + 1) // 2 --> 2 + 2 = 4, if we pass more operands, lets say 6 operands,
# then, 2 + (6 + 1) // 2 --> 2 + 3 = 5, if more
# then, 2 + (7 + 1) // 2 --> 2 + 4 = 6, if more ....

# the server doesn't recognize the "+", "-", or "*" signs, so we need a way to tell what
# calculations we want it to do. but then we can't pack "+" sign into a bytearray. 
# the following way tells the server what to do when client.py receives parameters from cmd line
if operator == "+":         # if the 3rd parameter from cmd line is a "+" sign
    client_packet[0] = 1    # then we pack an integer 1 in the 1st byte of bytearray "client_packet"   
elif operator == "-":
    client_packet[0] = 2
elif operator == "*":
    client_packet[0] = 4 

client_packet[1] = counter 

op_index = 2     # <--index of the list of operands 
argv_index = 4   # <--index of the list of the operands from cmd line   
total = 0        # <--for de-bugging only.

for i in range (4, len(sys.argv), op_index):  # range is between 4 and length of sys.argv list  
    # print("I_index -->      ",i)
    # print("op_index:        ", op_index)  
    
    # so at sys.argv[4], we store operand "1" in temp varable "A", 
    # and increment to the length of sys.argv. Let's say we have operands 1 2 3 4 5
    # then 1, 3, 5 is stored in A, 
    A = int(sys.argv[i])
    # print("        A:         ",A)

    # store 2, 4 in temp variable B when the i < the length of the sys.argv list
    if (i+1) < len(sys.argv) :
        B = int(sys.argv[i+1])
    else:
        B = 0  # else, we make B to be "0", so the imaginary 6th operand 6 is f 0
    # print("       B:          ",B)

    # in our example case, A = 1, A is shifted 4 bits to the left, and then OR'ed with B(it's 2 here)    
    packet_data = (A << 4) | B               # 1 = 0000 0001, shifted -> 1 = 0001 0000, 2 = 0000 0010(not shifted)
    client_packet[op_index] = packet_data    # OR 1 and 2, 0000 0010, we get 0001 0010, store it in packet_date as one byte
                                             # transfer the byte to client_packet[2, 3, 4.....]

    op_index += 1                            # move client_packet[2] to client_packet[3] by incrementing op_index by 1  

    # print("packet_data:    ", packet_data)
    # print("packet_date:    ", str(bin(packet_data)))
    
# print("numbers packed in: ", (client_packet))
# send the bytearray "client_packet" to the server
client_socket.send(client_packet)

# receive the result from the server , packet is what received and it's created on SERVER, 
server_packet, addr = client_socket.recvfrom(1024)

final_result = int.from_bytes(server_packet, byteorder='big', signed=True)
print(final_result)











# FIRST few step according to the instructions in Lab 2
#--------------------1, Test Connection Only-------------------------
'''
msg = bytes('Hello there.','utf-8')
client_socket.connect((host, port))
client_socket.send(msg)
data, addr = client_socket.recvfrom(1024)
print(data)
'''
#--------------------1, Test Connection Only-------------------------

#--------------------2, Test Simple Addition----------------------
'''
# after connection, send a bytearray
client_socket.connect((host, port))
buffer = bytearray([11])
client_socket.send(buffer)
result, addr = client_socket.recvfrom(1024)
print(result[0])
'''
#-------------------2, Test Simple Addition----------------------
