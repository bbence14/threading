import threading

counter = 0
lock = threading.Lock()

# Forcing sequential behaviour in case of writing
# lock.acquire()
# lock.release()


def increment():
    global counter
    for i in range(10**6):
        #lock.acquire()
        #counter += 1
        #lock.release()
        with lock:
            counter += 1


threads = []
for i in range(4):
    x = threading.Thread(target=increment)
    threads.append(x)

for t in threads:
    t.start()

for t in threads:
    t.join()

print('Counter val: ', counter)
# Multiple threads checks the same memory value and multiple calculations may return with the same result
