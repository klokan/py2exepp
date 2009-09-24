#!/usr/bin/env python
# File: sum_primes.py
# Author: Vitalii Vanovschi
# Desc: This program demonstrates parallel computations with pp module
# It calculates the sum of prime numbers below a given integer in parallel
# Parallel Python Software: http://www.parallelpython.com

import math
import sys
import pp


# Let's move the functionality to external module - to avoid "could not get source" error for .pyc only
# You have to run: "zip -u dist\library.zip primes.py"

from primes import sum_primes, isprime 

# If you don't want to distribute the source code of your function you can move the functionality to another external module and add it to the list of dependent module names in job_server.submit() - last argument. 

print """Usage: python sum_primes.py [ncpus]
    [ncpus] - the number of workers to run in parallel,
    if omitted it will be set to the number of processors in the system"""

# tuple of all parallel python servers to connect with
ppservers = ()
#ppservers = ("10.0.0.1",)

if len(sys.argv) > 1:
    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus, ppservers=ppservers)
else:
    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)

print "Starting pp with", job_server.get_ncpus(), "workers"

# Submit a job of calulating sum_primes(100) for execution.
# sum_primes - the function
# (100,) - tuple with arguments for sum_primes
# (isprime,) - tuple with functions on which function sum_primes depends
# ("math",) - tuple with module names which must be imported before
#             sum_primes execution
# Execution starts as soon as one of the workers will become available
job1 = job_server.submit(sum_primes, (100, ), (isprime, ), ("math", ))

# Retrieves the result calculated by job1
# The value of job1() is the same as sum_primes(100)
# If the job has not been finished yet, execution will
# wait here until result is available
result = job1()

print "Sum of primes below 100 is", result


# The following submits 8 jobs and then retrieves the results
inputs = (100000, 100100, 100200, 100300, 100400, 100500, 100600, 100700)
jobs = [(input, job_server.submit(sum_primes, (input, ), (isprime, ),
        ("math", ))) for input in inputs]

for input, job in jobs:
    print "Sum of primes below", input, "is", job()

job_server.print_stats()

# Parallel Python Software: http://www.parallelpython.com
