#!/usr/bin/python3
"""
    More dangerous example...
    
    Fork 4 - 8 processes for different databases
    that each limit concurrent connections to 20.
    
    Each process with then spawn less than 20 threads.
    
    All results will be collected on a queue.
"""

from multiprocessing import Process, Queue
from multiprocessing.dummy import Pool as thread_pool
from threading import Thread
import requests
import time
import urllib3

urllib3.disable_warnings()
q = Queue()
root_instances = ['a', 'b', 'c', 'd', 'e']  # Start a process for each instance.
url_dict = {'a': ['http://www.microsoft.com', 'http://www.microsoft.org'], 'b': ['http://www.microsoft.net', 'http://www.microsoft.co.uk'], 'c': ['http://www.microsoft.nl', 'http://www.microsoft.co'], 'c': ['http://www.microsoft.dk', 'http://www.outlook.dk'], 'd': ['http://www.skype.dk', 'http://www.live.dk'], 'e': ['http://www.hotmail.dk', 'http://www.hotmail.se', 'http://www.microsoft.se']}

def search_instances(name, q):
    """worker function"""
    global url_dict
    urls = url_dict[name]
    print(f'Worker {name} started...')
    thread_list = [Thread(target=long_running_search, args=(url, q)) for url in urls]
    for thread in thread_list:
        thread.start()
    while True:
        alive = sum(thread.is_alive() for thread in thread_list)
        if not alive:
            break
        print(f'{alive} threads running')
        time.sleep(1)
    for thread in thread_list:
        thread.join()
    print(q.get())  # Proof of queue working as expected.
    print(f'Worker {name} done.')


def long_running_search(url, q):
    try:
        r = requests.get(url, timeout=2, verify=False)
        q.put(r)
        #print(url)
    except Exception as e:
        print(f'{e}')


if __name__ == '__main__':
    jobs = []
    for root_name in root_instances:
        p = Process(target=search_instances, args=(root_name, q))
        jobs.append(p)
        p.start()
    print(f'Jobs: {jobs}')
    for job in jobs:
        print(job)
        job.join()  # Wait until all processes have exited.
        print('Finished joining processes.')  # <-- Not reached.
        
    while not q.empty():
        print(q.get())
        
    print('Fin')
