import multiprocessing as mp
import concurrent.futures as cf
import requests
from time import time
import urllib3
from functools import wraps

# Turn off the annoying "Inescure Request" Warnings from SSL request errors
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url_list = ['http://www.microsoft.com',
          'http://www.microsoft.org',
          'http://www.microsoft.net',
          'http://www.microsoft.co.uk',
          'http://www.microsoft.nl',
          'http://www.microsoft.co',
          'http://www.microsoft.dk',
          'http://www.outlook.dk',
          'http://www.skype.dk',
          'http://www.live.dk',
          'http://www.hotmail.dk',
          'http://www.hotmail.se',
          'http://www.microsoft.se']


def timing(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(f'Timing {f.__name__}...')
        start = time()
        result = f(*args, **kwargs)
        elapsed = time() - start
        print(f' took {elapsed:.2f}s')
        return result
    return wrapper


def fetchURLm(url):
    """ Fetch a given URL in a unique 'browser session' and return the request.
    """
    session = requests.Session()
    return session.get(url, timeout=3, verify=False)


@timing
def fetchURL(url):
    """ Print statistics about fetching individual URLs.
        Useful for determining bounds for how long the batch may take.
    """
    r = fetchURLm(url)
    try:
        content_length = len(r.content)
        assert r.status_code == 200
        print(f'\tRetrieved {content_length} bytes from {url}', end='')

    except Exception as e:
        print(f'\tFailed to retrieve {url} with error: {e!r}', end='')

    else:
        return r


@timing
def sequenceFetch(urls, details=False):
    """ Fetch a given list of URLs serially, and print some statistics on how long it took
    """
    if details:
        fetcher = fetchURL
    else:
        fetcher = fetchURLm
    results = [fetcher(url) for url in urls]
    total_fetched = sum([len(r.content) for r in results if r])
    num = len(urls)
    print(f'\tRetrieved a total of {total_fetched} bytes from {num} URLs', end='')


@timing
def asyncFetch(urls):
    """ Fetch a given list of URLs with a thread pool, and print some statistics on how long it took
    """
    results = []
    with cf.ThreadPoolExecutor() as executor:
        results = executor.map(fetchURLm, urls)

    total_fetched = sum([len(r.content) for r in results if r])
    num = len(urls)
    print(f'\tRetrieved a total of {total_fetched} bytes from {num} URLs', end='')


@timing
def parallelFetch(urls):
    """ Fetch a given list of URLs with a process pool, and print some statistics on how long it took
    """
    results = []
    with mp.Pool() as pool:
        results = pool.map(fetchURLm, urls)

    total_fetched = sum([len(r.content) for r in results if r])
    num = len(urls)
    print(f'\tRetrieved a total of {total_fetched} bytes from {num} URLs', end='')


if __name__ == '__main__':

    sequenceFetch(url_list, True)
    sequenceFetch(url_list)
    asyncFetch(url_list)
    parallelFetch(url_list)
