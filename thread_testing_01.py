!#/usr/bin/python3
"""
    Objective:
    Fire off several threads, and start processing their return values as they
    come in - instead of waiting for all of them to complete.
"""

import threading, requests, queue
from multiprocessing.dummy import Pool as ThreadPool 

urls = ['http://www.microsoft.com', 'http://www.microsoft.org', 'http://www.microsoft.net', 'http://www.microsoft.co.uk', 'http://www.microsoft.nl', 'http://www.microsoft.co', 'http://www.microsoft.dk', 'http://www.outlook.dk', 'http://www.skype.dk', 'http://www.live.dk', 'http://www.hotmail.dk', 'http://www.hotmail.se', 'http://www.microsoft.se', 'http://www.live.se', 'http://www.outlook.se', 'http://www.skype.se', 'http://www.microsoft.fr', 'http://www.outlook.fr', 'http://www.skype.fr', 'http://www.live.fr', 'http://www.hotmail.fr', 'http://www.microsoft.it', 'http://www.outlook.it', 'http://www.skype.it', 'http://www.live.it', 'http://www.hotmail.it', 'http://www.microsoft.de', 'http://www.outlook.de', 'http://www.skype.de', 'http://www.live.de', 'http://www.hotmail.de', 'http://www.outlook.com.au', 'http://www.askapolitician.net']

q = queue.Queue
pool = ThreadPool(10) 

def long_running_search(url):
    """Simulates getting a batch of IPs that will later be processed."""
    try:
        r = requests.get(url, timeout=2)
        print(r.status_code)
        return r.status_code, r.url
    except:
        print(f'url failed: {url}')

results = pool.map(long_running_search, urls)

print('This does not print until after all threads return :(')

pool.close() 
pool.join()

def break_up_batch_of_ips(batch):
    """Takes a batch from 'long_running_search' and spits out individual IPs."""
    for ip in batch:
        yield ip

def process_ip(ip):
    """Screen IPs"""
    pass

def block_ip(ip):
    """Sent a POST request to an API to block IP address."""
    pass
