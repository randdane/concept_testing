# concept_testing

## Thread Testing

* basic_threading.py
    * Using the normal style of threading to allow work while other threads have not returned.

* dummy_threading.py
    * Using the threading map method within multiprocessing.dummy.
    * Simple, yet prevents processing until results are collected.
    * [Reference](http://chriskiehl.com/article/parallelism-in-one-line/)
  
* fork_and_thread.py
    * "Fork and then thread" - forks a dynamic number of processes, spawns a number of threads, and sends results to a queue.
    
* multiple_threading_examples.py
    * ThreadPoolExecutor example.

## Resources
* [Multiprocessing Basics](https://pymotw.com/2/multiprocessing/basics.html) - from PyMOTW
