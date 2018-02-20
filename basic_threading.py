#!/usr/bin/python3
"""
    A more conventional threading approach.
"""
import time

from threading import Thread

q = queue.Queue

urls = ['http://www.microsoft.com', 'http://www.microsoft.org', 'http://www.microsoft.net', 'http://www.microsoft.co.uk', 'http://www.microsoft.nl', 'http://www.microsoft.co', 'http://www.microsoft.dk', 'http://www.outlook.dk', 'http://www.skype.dk', 'http://www.live.dk', 'http://www.hotmail.dk', 'http://www.hotmail.se', 'http://www.microsoft.se', 'http://www.live.se', 'http://www.outlook.se', 'http://www.skype.se', 'http://www.microsoft.fr', 'http://www.outlook.fr', 'http://www.skype.fr', 'http://www.live.fr', 'http://www.hotmail.fr', 'http://www.microsoft.it', 'http://www.outlook.it', 'http://www.skype.it', 'http://www.live.it', 'http://www.hotmail.it', 'http://www.microsoft.de', 'http://www.outlook.de', 'http://www.skype.de', 'http://www.live.de', 'http://www.hotmail.de', 'http://www.outlook.com.au', 'http://www.askapolitician.net']

def long_running_search(url, q):
    try:
        r = requests.get(url, timeout=2)
        q.put(r.status_code)
        return r.status_code, r.url
    except:
        pass

thread_list = [Thread(target=long_running_search, args=(url, q)) for url in urls]

for thread in thread_list:
    thread.start()
    
while True:
    alive = sum(thread.is_alive() for thread in thread_list)
    if not alive:
        break
    print(f'{alive} threads running')
    
    # Consume items from queue here.
    
    time.sleep(1)

for thread in thread_list:
    thread.join()
