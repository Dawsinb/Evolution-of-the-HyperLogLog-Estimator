from algorithms import FlajoletMartin, LogLog, SuperLogLog, HyperLogLog
from misc import formatter
import random
import statistics
import sys

###Tests###

#These tests rely on generating random 64 bit integers and treating them as a hash. The 64 bit space is sufficiently large and thus it assumes that there are no duplicates in the generation of these numbers and that the number of hashes is the cardinality.

#test paramaters, # of tests, items per test, bits for buckets, print every test or not
TESTS = 5
ITEMS = 1000000
BUCKETS = 16
PRINT_ALL = True

#create arrays to store results for each algorithm
fm = []
ll = []
sll = []
hll = []

#run tests
for i in range(0, TESTS):
  #print loading message
  sys.stdout.write("Running test " + str(i + 1) + " of " + str(TESTS) + "...")
  sys.stdout.flush()
  
  #Generate test hashes (random 32 bit integer)
  hashes = []
  for i in range(0, ITEMS):
    hashes.append('{:064b}'.format(random.randint(0, 2147483647)))
  
  #add to results array
  fm.append(FlajoletMartin.estimate(hashes))
  ll.append(LogLog.estimate(hashes, BUCKETS))
  sll.append(SuperLogLog.estimate(hashes, BUCKETS))
  hll.append(HyperLogLog.estimate(hashes, BUCKETS))

  #reset line
  sys.stdout.write('\r')
  
#print results
formatter.printTest("Flajolet-Martin", ITEMS, fm, PRINT_ALL)
formatter.printTest("LogLog", ITEMS, ll, PRINT_ALL)
formatter.printTest("SuperLogLog", ITEMS, sll, PRINT_ALL)
formatter.printTest("HyperLogLog", ITEMS, hll, PRINT_ALL)