#!/usr/bin/python3
"""
    More dangerous example...
    
    Fork 4 - 8 processes for different databases
    that each limit concurrent connections to 20.
    
    Each process with then spawn less than 20 threads.
    
    All results will be collected on a queue.
"""

from multiprocessing import Pool as multi_pool
from multiprocessing.dummy import Pool as thread_pool
import queue

q = queue.Queue

root_instances = ['a', 'b', 'c', 'd', 'e']  # Start a process for each instance.
url_dict = {'a': ['http://www.microsoft.com', 'http://www.microsoft.org'], 'b': ['http://www.microsoft.net', 'http://www.microsoft.co.uk'], 'c': ['http://www.microsoft.nl', 'http://www.microsoft.co'], 'c': ['http://www.microsoft.dk', 'http://www.outlook.dk'], 'd': ['http://www.skype.dk', 'http://www.live.dk'], 'e': ['http://www.hotmail.dk', 'http://www.hotmail.se', 'http://www.microsoft.se']}

def search_instances(root_name):
    global url_dict
    t_pool = thread_pool(15)
    urls = url_dict[root_name]
    print(t_pool.map(long_running_search, urls))
    t_pool.close() 
    t_pool.join()
    
def long_running_search(url):
    try:
        r = requests.get(url, timeout=2)
        print(r.status_code)
        return r.status_code, r.url
    except:
        pass
    
with multi_pool(5) as m_pool:
    print(m_pool.map(search_instances, root_instances))
