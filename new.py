# import dateutil.parser
# print dateutil.parser.parse("2014-01-28T05:18:15.878Z")
# import xlwt
# from datetime import datetime
# from tempfile import TemporaryFile
# book = xlwt.Workbook()
# sheet1 = book.add_sheet('sheet1')
# out = [['a', 'b', 'c'], [1, 2, 3], [4, 5, 6]]
# for i, doc in enumerate(out):
#     for j, val in enumerate(doc):
#         sheet1.write(i, j, val)
# fileName = 'Documents ' + str(datetime.now()) + '.xls'
# book.save(fileName)
# # book.save(TemporaryFile())

# import xlwt
# import datetime
#
# workbook = xlwt.Workbook()
# worksheet = workbook.add_sheet('Sheet1')
#
# style = xlwt.XFStyle()
# style.num_format_str = 'mm/dd/yyyy'
#
# alignment = xlwt.Alignment()  # Create Alignment
# alignment.horz = xlwt.Alignment.HORZ_CENTER
#
# style.alignment = alignment
#
# worksheet.write(0, 0, datetime.datetime.now(), style)
# workbook.save('date_format.xls')



# import itertools
#
# A = [[7, 5, 1],
#      [8, 9, 3],
#      [0, 10, 20]]
#
# B = [4, 5, 6]
# C = [7, 8]
#
# print list(((x, y) for x in A for y in B))
#
# print list(itertools.product(*A))
#
# print list(itertools.product(A, A))
#
# print zip(B, C)
# print list(itertools.izip(B, C))
# print zip(*zip(B, C))
#
# print list(itertools.imap(pow, (2,3,10), (5,2,3)))



# import Queue
# import threading
# import urllib2
#
# worker_data = ['http://google.com', 'http://yahoo.com', 'http://bing.com']
#
# #load up a queue with your data, this will handle locking
# q = Queue.Queue()
# for url in worker_data:
#     q.put(url)
#
#
# #define a worker function
# def worker(queue):
#     queue_full = True
#     while queue_full:
#         try:
#             #get your data off the queue, and do some work
#             url = queue.get(False)
#             data = urllib2.urlopen(url).read()
#             print len(data)
#
#         except Queue.Empty:
#             queue_full = False
#
# #create as many threads as you want
# thread_count = 5
# for i in range(thread_count):
#     t = threading.Thread(target=worker, args=(q,))
#     t.start()


