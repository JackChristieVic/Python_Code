import sys, socket, time, random, hashlib

# log function that flushes stdout, to help with
# buffering of stdout.
def log(s):
    print(time.time(), name + ": " + s)
    sys.stdout.flush()

# only port and client "name" are included on command-line; assume
# 'localhost' for host.
port = int(sys.argv[1])
name = sys.argv[2]

# we want a 'random' delay, but it has to be predictable, as well,
# for grading purposes. So we seed the random number generator with
# a hash of the name. (We could have just hand-picked a different delay
# for each of the 10 clients, but then what if we decide to run it later
# with 100 clients??
m = hashlib.md5(name.encode())
i = 0
for x in m.digest(): i += x
random.seed(i)
delay = random.randint(2, 6)

# The rest is just the GET protocol hard-coded, with some log
# output so we know when the client goes through certain milestones.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", port))
ready = sock.recv(1024)

log("READY (%d delay)." % delay)

sock.send("GET test.txt".encode("UTF-8"))
ok = sock.recv(1024)
sock.send("READY".encode("UTF-8"))
totalBytes = int.from_bytes(sock.recv(1024), byteorder='big', signed=False)
sock.send("OK".encode("UTF-8"))
f = open("test.txt", "wb")
bytesLeft = totalBytes

log("receiving")

# An artificial delay, so we can see the effect of having multiple clients
# actually waiting in the server's queue.
time.sleep(delay)
while(bytesLeft > 0):
	data = sock.recv(min(1024, bytesLeft))
	bytesLeft -= len(data)
	f.write(data)
f.close()
done = sock.recv(1024)

log("DONE")

sock.close()
	
