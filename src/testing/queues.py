import queue, threading, time

def get_twice(q):
    for i in range(2):
        print(q.get())

def do_once(q):
    q.put(1)

def other_get(g):
    print(g.get())

q = queue.Queue()
threading.Thread(target=do_once, args=(q,)).start()
threading.Thread(target=get_twice, args=(q,)).start()
threading.Thread(target=other_get, args=(q,)).start()
time.sleep(3)
threading.Thread(target=do_once, args=(q,)).start()