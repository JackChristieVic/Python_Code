import sys, socket
port = int(sys.argv[1]) # 1st input on cmd line
operator = str(sys.argv[2]) # 2nd input on cmd line
counter = int(sys.argv[3]) # 3rd input on cmd line
total = 0 # used to store the sum of the operands

operands = bytearray(len(sys.argv) - 4)
print("BYTEARRAY LENTH:",len(operands))
lenth = (len(sys.argv))
index = 4
for i in range( 4, len(sys.argv) ): # start from 4, exits at the last one of array
  # operands.append( int(sys.argv[i]) )
  for index in range (len(sys.argv) - 4):
    if index < len(sys.argv):
      operands[index] = int(sys.argv[i])
  total = total + operands[index]
print("the total is",total)
print("Operands are",operands)

print("THE LENTH OF OPERANADS IS-------->",len(operands))

print("===========================================================")






'''
packet_test = bytearray(len(sys.argv))
for i in range (1, 5):
    packet_test[i] = (sys.argv[i])
    # packet_test.append( int(i) )
    print(packet_test[i])
print("elements in packet_test:",(packet_test) )
print(0x14)
'''