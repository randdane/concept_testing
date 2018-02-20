#!/usr/bin/env python3

"""
    Fork and Thread
    ---------------

    Fork multiple processes dynamically to handle separate environments.

    Create threads to handle all URLs within each process.

    Send results back to main process using a queue.
"""

from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Process, Queue
import requests
import urllib3

urllib3.disable_warnings()
q = Queue()

root_instances = ['a', 'b', 'c', 'd', 'e']  # Start a process for each instance.
url_dict = {'a': ['http://www.microsoft.com', 'http://www.microsoft.org'],
            'b': ['http://www.microsoft.net', 'http://www.microsoft.co.uk'],
            'c': ['http://www.microsoft.nl', 'http://www.microsoft.co'],
            'd': ['http://www.skype.dk', 'http://www.live.dk'],
            'e': ['http://www.hotmail.dk', 'http://www.hotmail.se', 'http://www.microsoft.se']}


def search_instances(name, q, url_list):
    """worker function"""
    print(f'Worker {name} started...')
    with ThreadPoolExecutor() as executor:
        results = executor.map(long_running_search, url_list)
        q.put([x for x in results])  # Send results to the shared queue.
    print(f'Worker {name} done.')


def long_running_search(url):
    try:
        r = requests.get(url, timeout=2, verify=False)
        return r.status_code
    except Exception as e:
        print(f'{e}')


if __name__ == '__main__':

    jobs = []
    for root_name in root_instances:
        p = Process(target=search_instances, args=(root_name, q, url_dict[root_name]))
        jobs.append(p)
        p.start()

    for job in jobs:
        job.join()  # Ensure each process exits normally.

    while not q.empty():
        print(q.get())  # Retrieve each item from the queue.

    print('Fin')
