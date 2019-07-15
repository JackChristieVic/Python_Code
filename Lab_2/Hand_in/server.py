import socket, sys

port = int(sys.argv[1])      

# Create the socket object using DGRAM
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_socket.bind( ("", port) )

while True:
	client_packet, addr = server_socket.recvfrom(1024)

	# this counter is not the same counter as that on client.pyf, just happen to be the same name
	counter = client_packet[1]    # counter is created and packed in client_packet[1] on client.py
	server_packet = bytearray(4)  # we only have 4 bytes in the server_packet bytearray
	result = 0
	
	for i in range (2, len(client_packet)  ):
		#           REMINDER
		# client_packet[0] --> operator
		# client_packet[1] --> counter
		# print("1, len(client_packet)-->", len(client_packet))
		# print("1, client_packet ------>", client_packet)
		
		combined = int(client_packet[i])  # (1 & 2), (3 & 4), (5 & 0), (n & n+1) in this byte in our case
		a = combined & 0b11110000         # get 1 out
		a = a >> 4                        # move 1 to left for 4 bits and put in server_packet[0]
		# print("1,	   a------------>",a)

	
		b = combined & 0b00001111        # get 2 out


		# print("1,	   b------------>", b)
		# print("1, a + b = result------->", result)

		if client_packet[0] == 1:
			result = result + a + b
		elif client_packet[0] == 2:
			if i == 2:
				result = a - b
			else:
				result = result - a - b
		else:
			if i == 2:
				result = a * b
			else:
				if (counter % 2 == 1) and ( i==len(client_packet)-1):
					result = result * a
				else:
					result = result * a * b
				
	# print("1, final ADDITION Result   ===>",result)
	final_result = result.to_bytes(4, byteorder='big', signed=True)
	server_socket.sendto(final_result, addr)


















'''
		print("4 ADD RESULT AFTER shiftting:", result)
		if client_packet[0] == 1:
			result = result + client_packet[i]
			print("3, ADD -->", result)



			
		elif client_packet[0] == 2:
			result -= client_packet[i]
			# print("3,  SUB-->", result)
			a = result & 0b11110000
			packet[0] = a >> 4
			b = result & 0b00001111
			packet[1] = b
			
		elif client_packet[0] == 4:
			result *= client_packet[i]
			# print("3,  SUB-->", result)
			a = result & 0b11110000
			packet[0] = a >> 4
			b = result & 0b00001111
			packet[1] = b	
	print("Cal's done, result -->", result)
	
	#--convert the integer result of the calculation to a bytearray
	#  but store the result in big endian order, and have it signed
	result = result.to_bytes(4, byteorder='big', signed=True)
	print ('result on SERver is:', result)
	server_socket.sendto(result, addr)
'''
'''
	if client_packet[0] == 1:
		for i in range (2, len(client_packet) ): # start from 2, 0->+/-/*(operator), 1->result
			result = result + client_packet[i]
			a = result & 0xff00
			packet[0] = a >> 8
			b = result & 0x00ff
			packet[1] = b
		server_socket.sendto(packet, addr)
		print("3, ADD -->", result)
	elif client_packet[0] == 2:
		for i in range (2, len(client_packet) ): 
			result -= client_packet[i]
			a = result & 0xff00
			packet[0] = a >> 8
			b = result & 0x00ff
			packet[1] = b
		server_socket.sendto(packet, addr)
		print("3,  SUB-->", result)
	elif client_packet[0] == 4:
		for i in range (2, len(client_packet) ): 
			result *= client_packet[i]
			a = result & 0xff00
			packet[0] = a >> 8

			b = result & 0x00ff
			packet[1] = b >> 8
		server_socket.sendto(packet, addr)
		print("3, MULTI -->", result)
'''	
#---------------8, pass multiple 1-byte--------------------------

'''
#----------STEP 1 TO 7--------------------------------------
				__
			   |||| 
			   ||||
			 __||||__
			 \      /
			  \    /
			   \  /
			    \/			
while True:
	# UDP allows only 1 connection. Everything needs to be completed within this 1 connection.
	msg, addr = server_socket.recvfrom(1024)
	print('Got connection from', addr)
	response = bytes('You are successfully connected to the server. ', 'utf-8')
	server_socket.sendto(response, addr)
	'''
#---------------1, Test connection only----------------------

#---------------2, 3, 4, 5, 6 Test Simple Addition----------------------
'''
while True:
	# - receiving data from client, variables client_packet and addr are from adder_client.py
	client_packet, addr = server_socket.recvfrom(1024)

	# - assign the number at index 0 in client_packet bytearray to one
	#   ------------------------------------------------------to two
	# - variables "one" and "two" are created on adder_server.py
	#   but client_packet[0] & client_packet[1] are created on adder_client.py
	#   they are just received by the server for simple calculations
	one = client_packet[0]
	two = client_packet[1]
	# the result could be a of size 2 bytes
	result = one + two


	# - create another bytearray to store the result of the calculation and append the 
	#   result to the bytearray(Note: the result will be at index 0 of the bytearray)
	packet = bytearray(2)

	# using bit shift to 
	a = result & 0xff00
	packet[0] = a >> 8

	b = result & 0x00ff
	packet[1] = b
	
	server_socket.sendto(packet, addr)
'''
#---------------2, 3, 4, 5, 6 Test Simple Addition----------------------

#----------------7, Add support for diff op-----------------------------
'''
while True:
	# - receiving data from client, variables client_packet and addr are from adder_client.py
	client_packet, addr = server_socket.recvfrom(1024)

	# - assign the number at index 0 in client_packet bytearray to one
	#   ------------------------------------------------------to two
	# - variables "one" and "two" are created on adder_server.py
	#   but client_packet[0] & client_packet[1] are created on adder_client.py 
	#   but received by the server for simple calculations
	one = client_packet[1] 
	two = client_packet[2]
	
	#--if the first element(i.e. client_packet[0] = 1) in the received packet is an integer 1,
	#  it means the client wants server to do addition. same logic, 2 for subtraction, 4 for multiplication
	#  We also create a new variable called "result" to store the result of the operations(+, -, *)
	if client_packet[0] == 1:
		result = one + two
	elif client_packet[0] == 2:
		result = one - two
	elif client_packet[0] == 4:
		result = one * two

	#--create another bytearray to store the result of the calculation 
	packet = bytearray(3)
	
	#--the result could be of size 2 bytes, for example: result = 256. so it cannot be store in 1 byte.
	#  if you try: packet.append(result), you'll get an error message saying "result must be in range(0, 256)"
	#  so we need to store the result in 2 bytes, in bytearray, that's two elements.
	#  1st: ANDING result with the binary number 1111 0000, and store the result in variable a
	#  2nd, shift a 8 bits to the right, store the result of the shifting in 2nd element of the bytearray.
	#  say result = 256, in binary: 00000001 00000000
	#                       ANDING: 11111111 00000000, the goal of shifting is to make right side all becomes 0's
	#                      You get: 00000001 00000000, now the space on R is free(all 0's) to shift L over here
	#  shift 8 bits to right, get:  00000000 00000001, put this in packet[1], so in binary, packet[1] = 00000001
	a = result & 0xff00
	packet[1] = a >> 8

	#  say result = 256, in binary: 00000001 00000000  
	#                       ANDING: 00000000 11111111, the goal is to make L side all becomes 0's 
	#                      You get: 00000000 00000000, no shiftting, put in packet[2], packet[2] = 00000000
	b = result & 0x00ff
	packet[2] = b
	
	#--Now in the bytearray packet, we have two elements with values 00000001 00000000
	server_socket.sendto(packet, addr)
'''
#---------------7, Add support for diff op----------------------


