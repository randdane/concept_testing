# concept_testing

## Thread Testing

* thread_testing_01.py
    * Using the threading map method within multiprocessing.dummy.
    * Simple, yet prevents processing until results are collected.
    * [Reference](http://chriskiehl.com/article/parallelism-in-one-line/)

* thread_testing_02.py
    * Using the normal style of threading to allow work while other threads have not returned.
  
* thread_testing_03.py
    * "Fork and then thread" - forks a dynamic number of processes (4-8) and then spawns up to 20 threads to collect results into a queue.
    * Not actually working yet.
