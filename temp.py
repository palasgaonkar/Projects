# from collections import deque
# q = deque(maxlen=3)
# q.append(1)
# q.append(2)
# q.append(3)
# q.append(4)
# print q, q.pop(), q


# from collections import defaultdict
# d = defaultdict(set)
# d['a'].add(1)
# d['a'].add(2)
# d['b'].add(4)
# d['a'].add(2)
# print d


# d = {}
# # A regular dictionary
# d.setdefault('a', []).append(1)
# d.setdefault('a', []).append(2)
# d.setdefault('b', []).append(4)
# print sorted(d.values()), d


# def dedupe(items):
#    seen = set()
#    for item in items:
#        if item not in seen:
#            yield item
#            seen.add(item)
#
# a = [1, 5, 2, 1, 9, 1, 5, 10]
# print list(dedupe(a)), list(set(a))


# rows = [{"a": "asd", "date": "12/21/21"}, {"a": "assdd", "date": "12/21/21"}]
# from collections import defaultdict
# rows_by_date = defaultdict(list)
# for row in rows:
#    rows_by_date[row['date']].append(row)
# for r in rows_by_date['12/21/21']:
#    print r


# from collections import namedtuple
# Subscriber = namedtuple('Subscribe', ['addr', 'joined'])
# sub = Subscriber('jonesy@example.com', '2012-10-19')
# print sub.addr, "joined on", sub.joined


# import os
#files = os.listdir('../')
#if any(name.endswith('.py') for name in files):
#    print('There be python!')
#else:
#    print('Sorry, no python.')


#def t():
#    return [lambda x, i=i: i * x for i in range(5)]
#
#for t in t():
#    print t(2)


# from itertools import dropwhile
# with open('./validate.py') as f:
#    for lineNo, line in enumerate(f):
#        print lineNo, line


# from collections import defaultdict
# word_summary = defaultdict(list)
# with open('./sudoku.py', 'r') as f:
#    lines = f.readlines()
# for idx, line in enumerate(lines):
#    # Create a list of words in current line
#    words = [w.strip().lower() for w in line.split()]
#    for word in words:
#        word_summary[word].append(idx)
# print word_summary


#import webbrowser
#webbrowser.open_new('http://www.python.org')

# from subprocess import call
# call(["ls", "-l"])

#import copy
#a = [[1, 21], [2, 22]]
#b = copy.deepcopy(a)
#a[1][0] = 212
#print id(a), a, id(b), b


# import codecs
# def rot13(string):
#     return codecs.encode(string, 'rot_13')
# print rot13('hi there' ` `)

# =================================================================================================================

# import threading
# import thread
# import time
# exitFlag = 0
#
# class myThread (threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print "Starting " + self.name + '\n'
#         print threading.local()
#         print_time(self.name, self.counter, 5)
#         print "Exiting " + self.name + '\n'
#
# def print_time(threadName, delay, counter):
#     while counter:
#         if exitFlag:
#             thread.exit()
#         time.sleep(delay)
#         print "%s: %s" % (threadName, time.ctime(time.time()))
#         counter -= 1
#
# # Create new threads
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
#
# # Start new Threads
# thread1.start()
# print threading.currentThread()
# thread2.start()
# print threading.currentThread()

# import threading
# import thread
# import time
# class myThread (threading.Thread):
#     def __init__(self, threadID, name, counter):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#     def run(self):
#         print "Starting " + self.name
#         # Get lock to synchronize threads
#         threadLock.acquire()
#         print_time(self.name, self.counter, 5)
#         # Free lock to release next thread
#         threadLock.release()
#
# def print_time(threadName, delay, counter):
#     while counter:
#         time.sleep(delay)
#         print "%s: %s" % (threadName, time.ctime(time.time()))
#         counter -= 1
#
# threadLock = threading.Lock()
# threads = []
#
# # Create new threads
# thread1 = myThread(1, "Thread-1", 1)
# thread2 = myThread(2, "Thread-2", 2)
#
# # Start new Threads
# thread1.start()
# thread2.start()
#
# # Add threads to thread list
# threads.append(thread1)
# threads.append(thread2)
#
# # Wait for all threads to complete
# for t in threads:
#     t.join()



# import Queue
# import threading
# import time
#
# exitFlag = 0
#
# class myThread (threading.Thread):
#     def __init__(self, threadID, name, q):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.q = q
#     def run(self):
#         print "Starting " + self.name
#         process_data(self.name, self.q)
#         print "Exiting " + self.name
#
# def process_data(threadName, q):
#     while not exitFlag:
#         queueLock.acquire()
#         if not workQueue.empty():
#             data = q.get()
#             queueLock.release()
#             print "%s processing %s" % (threadName, data)
#         else:
#             queueLock.release()
#         time.sleep(1)
#
# threadList = ["Thread-1", "Thread-2", "Thread-3"]
# nameList = ["One", "Two", "Three", "Four", "Five"]
# queueLock = threading.Lock()
# workQueue = Queue.Queue(10)
# threads = []
# threadID = 1
#
# # Create new threads
# for tName in threadList:
#     thread = myThread(threadID, tName, workQueue)
#     thread.start()
#     threads.append(thread)
#     threadID += 1
#
# # Fill the queue
# queueLock.acquire()
# for word in nameList:
#     workQueue.put(word)
# queueLock.release()
#
# # Wait for queue to empty
# while not workQueue.empty():
#     pass
#
# # Notify threads it's time to exit
# exitFlag = 1
#
# # Wait for all threads to complete
# for t in threads:
#     t.join()



# from itertools import *
#
# a = [[1, 2], [11, 22], [111, 222, 333]]
# print list(product(*a))
#
# print list(ifilter(lambda x: x % 2, range(10)))
#
# print list(permutations('ABCD', 2))
#
# print list(starmap(pow, [(2, 5), (3, 2), (10, 3)]))
# print list(imap(pow, (2, 3, 10), (5, 2, 3)))

# import urllib2
# import time
# hosts = ["http://yahoo.com", "http://google.com", "http://amazon.com",
#          "http://ibm.com", "http://apple.com"]
# start = time.time()
# #grabs urls of hosts and prints first 1024 bytes of page
# for host in hosts:
#     url = urllib2.urlopen(host)
#     print url.read(1024)
# print "Elapsed Time: %s" % (time.time() - start)


#!/usr/bin/env python
# import Queue
# import threading
# import urllib2
# import time
#
# hosts = ["http://yahoo.com", "http://google.com", "http://amazon.com",
#          "http://ibm.com", "http://apple.com"]
# queue = Queue.Queue()
#
#
# class ThreadUrl(threading.Thread):
#     """Threaded Url Grab"""
#
#     def __init__(self, queue):
#         threading.Thread.__init__(self)
#         self.queue = queue
#
#     def run(self):
#         while True:
#             #grabs host from queue
#             host = self.queue.get()
#             #grabs urls of hosts and prints first 1024 bytes of page
#             url = urllib2.urlopen(host)
#             print url.read(1024)
#             #signals to queue job is done
#             self.queue.task_done()
#
#
# start = time.time()
#
#
# def main():
#     #spawn a pool of threads, and pass them queue instance
#     for i in range(5):
#         t = ThreadUrl(queue)
#         t.setDaemon(True)
#         t.start()
#         #populate queue with data
#         for host in hosts:
#             queue.put(host)
#
#     #wait on the queue until everything has been processed
#     queue.join()
#
# main()
# print "Elapsed Time: %s" % (time.time() - start)


import Queue
import threading
import urllib2
import time
from BeautifulSoup import BeautifulSoup

hosts = ["http://yahoo.com", "http://google.com", "http://amazon.com",
         "http://ibm.com", "http://apple.com"]

queue = Queue.Queue()
out_queue = Queue.Queue()


class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""

    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue

    def run(self):
        while True:
            #grabs host from queue
            host = self.queue.get()

            #grabs urls of hosts and then grabs chunk of web page
            url = urllib2.urlopen(host)
            chunk = url.read()

            #place chunk into out queue
            self.out_queue.put(chunk)

            #signals to queue job is done
            self.queue.task_done()


class DatamineThread(threading.Thread):
    """Threaded Url Grab"""

    def __init__(self, out_queue):
        threading.Thread.__init__(self)
        self.out_queue = out_queue

    def run(self):
        while True:
            #grabs host from queue
            chunk = self.out_queue.get()

            #parse the chunk
            soup = BeautifulSoup(chunk)
            # print soup.prettify()
            print soup.findAll(['title'])

            #signals to queue job is done
            self.out_queue.task_done()


start = time.time()


def main():
    #spawn a pool of threads, and pass them queue instance
    for i in range(5):
        t = ThreadUrl(queue, out_queue)
        t.setDaemon(True)
        t.start()

    #populate queue with data
    for host in hosts:
        queue.put(host)

    for i in range(5):
        dt = DatamineThread(out_queue)
        dt.setDaemon(True)
        dt.start()


    #wait on the queue until everything has been processed
    queue.join()
    out_queue.join()


main()
print "Elapsed Time: %s" % (time.time() - start)

