import logging
import random
import threading
import time

logging.basicConfig(level=logging.DEBUG,
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',)

# def worker():
#     logging.debug('Starting')
#     time.sleep(2)
#     logging.debug('Exiting')
#
# def my_service():
#     logging.debug('Starting')
#     time.sleep(3)
#     logging.debug('Exiting')
#
# t = threading.Thread(name='my_service', target=my_service)
# w = threading.Thread(name='worker', target=worker)
# w2 = threading.Thread(target=worker)  # use default name
#
# w.start()
# w2.start()
# t.start()



# def daemon():
#     logging.debug('Starting')
#     time.sleep(2)
#     logging.debug('Exiting')
#
# d = threading.Thread(name='daemon', target=daemon)
# d.setDaemon(True)
#
# def non_daemon():
#     logging.debug('Starting')
#     logging.debug('Exiting')
#
# t = threading.Thread(name='non-daemon', target=non_daemon)
#
# d.start()
# t.start()
# d.join(1)
# print 'd.isAlive()', d.isAlive()



# def worker():
#     """thread worker function"""
#     # t = threading.currentThread()
#     pause = random.randint(1, 5)
#     logging.debug('sleeping %s', pause)
#     time.sleep(pause)
#     logging.debug('ending')
#     return
#
# for i in range(3):
#     t = threading.Thread(name=i+1, target=worker)
#     t.setDaemon(True)
#     t.start()
#
# main_thread = threading.currentThread()
# for t in threading.enumerate():
#     if t is main_thread:
#         continue
#     logging.debug('joining %s', t.getName())
#     t.join()



# def delayed():
#     logging.debug('worker running')
#     return
#
# t1 = threading.Timer(3, delayed)
# t1.setName('t1')
# t2 = threading.Timer(3, delayed)
# t2.setName('t2')
#
# logging.debug('starting timers')
# t1.start()
# t2.start()
#
# logging.debug('waiting before canceling %s', t2.getName())
# time.sleep(2)
# logging.debug('canceling %s', t2.getName())
# t2.cancel()
# logging.debug('done')



# def wait_for_event(e):
#     """Wait for the event to be set before doing anything"""
#     logging.debug('wait_for_event starting')
#     event_is_set = e.wait()
#     logging.debug('event set: %s', event_is_set)
#     logging.debug('processing event')
#
#
# def wait_for_event_timeout(e, t):
#     """Wait t seconds and then timeout"""
#     while not e.isSet():
#         print e.isSet()
#         logging.debug('wait_for_event_timeout starting')
#         event_is_set = e.wait(t)
#         logging.debug('event set: %s', event_is_set)
#         if event_is_set:
#             logging.debug('processing event')
#         else:
#             logging.debug('doing other work')
#
#
# e = threading.Event()
# t1 = threading.Thread(name='block',
#                       target=wait_for_event,
#                       args=(e,))
# t1.start()
#
# t2 = threading.Thread(name='non-block',
#                       target=wait_for_event_timeout,
#                       args=(e, 2))
# t2.start()
#
# logging.debug('Waiting before calling Event.set()')
# time.sleep(3)
# e.set()
# logging.debug('Event is set')



# class Counter(object):
#     def __init__(self, start=0):
#         self.lock = threading.Lock()
#         self.value = start
#
#     def increment(self):
#         logging.debug('Waiting for lock')
#         self.lock.acquire()
#         try:
#             logging.debug('Acquired lock')
#             self.value = self.value + 1
#         finally:
#             self.lock.release()
#
#
# def worker(c):
#     for i in range(2):
#         pause = random.random()
#         logging.debug('Sleeping %0.02f', pause)
#         time.sleep(pause)
#         c.increment()
#     logging.debug('Done')
#
# counter = Counter()
# for i in range(2):
#     t = threading.Thread(target=worker, args=(counter,))
#     t.start()
#
# logging.debug('Waiting for worker threads')
# main_thread = threading.currentThread()
# for t in threading.enumerate():
#     if t is not main_thread:
#         t.join()
# logging.debug('Counter: %d', counter.value)


# def lock_holder(lock):
#     logging.debug('Starting')
#     while True:
#         with lock:
#             logging.debug('Holding')
#             time.sleep(0.5)
#         time.sleep(0.5)
#     return
#
# def worker(lock):
#     logging.debug('Starting')
#     num_tries = 0
#     num_acquires = 0
#     while num_acquires < 3:
#         time.sleep(0.5)
#         logging.debug('Trying to acquire')
#         have_it = lock.acquire(0)
#         try:
#             num_tries += 1
#             if have_it:
#                 logging.debug('Iteration %d: Acquired',  num_tries)
#                 num_acquires += 1
#             else:
#                 logging.debug('Iteration %d: Not acquired', num_tries)
#         finally:
#             if have_it:
#                 lock.release()
#     logging.debug('Done after %d iterations', num_tries)
#
#
# lock = threading.Lock()
#
# holder = threading.Thread(target=lock_holder, args=(lock,), name='LockHolder')
# holder.setDaemon(True)
# holder.start()
#
# worker = threading.Thread(target=worker, args=(lock,), name='Worker')
# worker.start()



# def consumer(cond):
#     """wait for the condition and use the resource"""
#     logging.debug('Starting consumer thread')
#     t = threading.currentThread()
#     with cond:
#         cond.wait()
#         logging.debug('Resource is available to consumer')
#
# def producer(cond):
#     """set up the resource to be used by the consumer"""
#     logging.debug('Starting producer thread')
#     with cond:
#         logging.debug('Making resource available')
#         cond.notifyAll()
#
# condition = threading.Condition()
# c1 = threading.Thread(name='c1', target=consumer, args=(condition,))
# c2 = threading.Thread(name='c2', target=consumer, args=(condition,))
# p = threading.Thread(name='p', target=producer, args=(condition,))
#
# c1.start()
# time.sleep(2)
# c2.start()
# time.sleep(2)
# p.start()



# class ActivePool(object):
#     def __init__(self):
#         super(ActivePool, self).__init__()
#         self.active = []
#         self.lock = threading.Lock()
#     def makeActive(self, name):
#         with self.lock:
#             self.active.append(name)
#             logging.debug('Running: %s', self.active)
#     def makeInactive(self, name):
#         with self.lock:
#             self.active.remove(name)
#             logging.debug('Running: %s', self.active)
#
# def worker(s, pool):
#     logging.debug('Waiting to join the pool')
#     with s:
#         name = threading.currentThread().getName()
#         pool.makeActive(name)
#         time.sleep(0.1)
#         pool.makeInactive(name)
#
# pool = ActivePool()
# s = threading.Semaphore(2)
# for i in range(4):
#     t = threading.Thread(target=worker, name=str(i), args=(s, pool))
#     t.start()



# def show_value(data):
#     try:
#         val = data.value
#     except AttributeError:
#         logging.debug('No value yet')
#     else:
#         logging.debug('value=%s', val)
#
#
# def worker(data):
#     show_value(data)
#     data.value = random.randint(1, 100)
#     show_value(data)
#
# local_data = threading.local()
# show_value(local_data)
# local_data.value = 1000
# show_value(local_data)
#
# for i in range(2):
#     t = threading.Thread(target=worker, args=(local_data,))
#     t.start()



def show_value(data):
    try:
        val = data.value
    except AttributeError:
        logging.debug('No value yet')
    else:
        logging.debug('value=%s', val)

def worker(data):
    show_value(data)
    data.value = random.randint(1, 100)
    show_value(data)

class MyLocal(threading.local):
    def __init__(self, value):
        logging.debug('Initializing %r', self)
        self.value = value

local_data = MyLocal(1000)
show_value(local_data)

for i in range(2):
    t = threading.Thread(target=worker, args=(local_data,))
    t.start()