import threading, sys

A = int(sys.argv[1])  # number of child threads
B = int(sys.argv[2])  # number of increments per thread

# the shared variable
x = 0

def increment():
    # If we want to modify a global variable from inside
    # a function, we have to add a special declaration for it.
    global x     
    x = x + 1

class MyThread(threading.Thread):
    def run(self):
        for i in range(B):
            increment()

threads = []
for i in range(A):
    t = MyThread()
    t.start()
    threads.append(t)

# Wait for all the threads to complete. The .join() method instructs the calling thread 
# (the main program thread) to block until the target thread (t) completes. This loop
# effectively makes the main program thread block until all child threads are complete.
for t in threads:
    t.join()

print("Done. Final value of x:", x)