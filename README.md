# Evolution of the HyperLogLog Estimator
The popular HyperLogLog estimator is part of a larger family of LogLog algorithms. The HyperLogLog estimator is most closely based on the LogLog estimator as you will see. However, all of the LogLog algorithms are based on the intuition of the Flajolet-Martin algorithm.

This repo contains implementations and testing of the Flagolet-Martin, LogLog, SuperLogLog, and HyperLogLog algorithms.

You will find in main the parameters set to a default of:
```
TESTS = 5
ITEMS = 1000000
BUCKETS = 16
PRINT_ALL = True
```
Where "TESTS" controls the number of tests done, "ITEMS" controls the number of hashes per tests, "BUCKETS" controls the amount of bits to use for the buckets (discussed below), and "PRINT_ALL" controls weather or not to print the results from every test or not.

To note these implementations are not the most effecient implementations in terms of memory nor time. They serve primarly to demonstrate how these algorithms work and how they compare. If you are looking for a cardinality estimation algorithm you should look for implementations of the HyperLogLog++ algorithm.

## Flajolet-Martin
The Flajolet-Martin algorithm is based on the intuition that if you flip a coin you have a 2^-q probability of seeing k tails in a row. Thus if we flip coins some unknown number of sessions and record a maximum number of tails in a row k. We will expect 2^k = q sessions to have occured where q is the cardinality of the sessions.

The way the algorithm works is to create a hash of the data that you want to estimate the cardinality of and treat its binary as a series of coin flips. For example "0100" would be 2 tails in a row. We record this information by taking the rank of the first "1" in the hash. In this case it would be a rank of 2 (Flajolet-Martin uses 0 based indexing).

In order to combat variance Flajolet-Martin requires that all previous ranks must have been found in order for a higher rank to be counted. It does this by tracking the recorded ranks in a bitmap. First we initialize a bitmap to all zeros say "0000 0000". Then as we record ranks we set the corresponding index of the bitmap to a 1. For example "0010 1010" has a rank of 1 and we record this onto our bitmap as "0000 0010". We repeat this for all the hashes and take for example that if at the end our bitmap is as follows "1001 1111". The highest rank we have recorded is 7, however it does not have all previous ranks before recorded and thus we do not count it. Instead we take the highest rank recorded as 4. However, we increase this by 1 to account for using 0 based indexing. Thus, in practice finding the rank of the first 0 is equivelent to finding the rank + 1 of the first 1 and this is often the strategy employed.

Lastly, due to only taking the highest consequtive rank, as well as expected collisions in the hashing function, we divide by a constant bias correction factor. This factor is calculated in Flajolet-Martin's paper to be around 0.77351. If you are interested in the derivation of this I suggest reading the original paper on this algorithm which I have linked to below.

The Flajolet-Martin algorithm despite only taking the highest consecutive rank is still highly variable. In practice one would run the algorithm multiple times with different hashing functions and take either the mean or the mode of all the runs. However, this is costly and the problem of variance has been better solved in the LogLog algorithms as will be discussed later.

The asymptotic time complexity of this algorithm is simply O(n) where n is our number of hashes. We process each hash once and the processing is clearly constant O(1) work giving us n * O(1) = O(n). 

## LogLog
The LogLog algorithm is based on the same coin flipping logic as the Flajolet-Martin algorithm, however in order to combat the high variance it divides the hashes into buckets and then takes the average of the buckets at the end. These buckets essentially allows us to treat one hash function as multiple in the same run. As well, the LogLog algorithm moves away from the consecutive rule of the bitmap strategy and just takes the max rank of each bucket.

The way we determine the bucket is to take the first k bits of our hash and have this represent our bucket, and then take the rest of the bits and treat that as a hash. Thus when using k bits for our buckets we have 2^k total buckets; the total number of buckets is denoted as m. For example, using a k of 2 the hash "1010 1100" is broken up into a bucket of "10" and a hash of "10 1100". The hash has a rank of 3 (LogLog uses 1 based indexing), and goes into the bucket 3 ("10 base 2" = 3).

So, for running the algorithm we initialize 2^k = m buckets to 0, and run through all the hashes recording the max rank of each bucket. We expect each bucket to encounter q/m hashes so the average of the buckets at the end will correspond to q/m. Thus, at the end after averaging the buckets we take m * 2^(average) to get a correspondence to q, the cardinality of the data set.

Again, there is a predictible bias in the algorithm however this time it is towards larger numbers. We correct for this bias by multiplying by 0.397011808. Again, if you are interested in the derivation of this I suggest reading the original paper which I have linked to below.

In terms of asymptotic time complexity LogLog will run in O(m + n) where m is our number of buckets, and n is that number of hashes. This is because we process each hash once, and the processing is constant O(1) work. We also process the buckets at the end by taking the average this is O(m) time. Thus in total we have O(n) + O(m) = O(n + m) time complexity.

## SuperLogLog
The SuperLogLog algorithm is very similar to the LogLog algorithm. It employs the same exact bucket strategy with one key difference. Before taking the average the SuperLogLog algorithm throws out the top 30% buckets with the highest recorded rank. The idea of this is to eliminate outliers that simply luckily got a high rank as we are no longer using the bitmap strategy. This decreases the variance found in the SuperLogLog algorithm.

The only other difference is that this of course leads to a different bias factor than that of the LogLog algorithm. In Flajolet's paper on LogLog and SuperLogLog the theoretical value of the bias factor for SuperLogLog is never found but rather emperically generated. Unfortunately the paper does not give the emperical bias factor that they used either. As such, I have emperically generated a bias factor myself and got something around 0.764. This lines up with our intuition that the SuperLogLog shouldn't be as biased towards higher numbers that LogLog is.

The asymptotic time complexity of SuperLogLog is a little more complicated. There is O(n) work just the same as LogLog, however the removal of the top 30% buckets isn't so simple. The natural approach is to loop through the bucket array and remove the max value .3 * m times. However, this gives us O(m^2 + n) time complexity. Alternatively we could sort the array and then resize it to remove the last 30% of values. The resizing could be done in constant O(1) time and the sorting could ideally be done in O(m log m) using something like quick sort or O(m) using something like radix sort. This gives a theoretical best time complexity of O(m + n) just like LogLog.

## HyperLogLog
The HyperLogLog algorithm is agian very similar to the LogLog algorithm. It also employs the same bucket strategy, but instead of throwing out the top 30% to elimnate variance, it simply takes the harmonic mean instead of the arithmetic mean. The harmonic mean naturally alleviates the problem of outliers and is a much more effecient solution.

Of course this also leads to a different bias factor. The bias factor can be approximated using the formula 0.7213 / (1 + (1.079 / 2^k)) where k is the number of bits for the buckets and k > 5. There are approximations for lower values of k as well that Flajolet discuesses in his paper, but as we want to be using larger bucket sizes anyways I have ommitted them from the program. If you would like to see these as well as the derivations the original paper is linked below.

The aymptotic time complexity of HyperLogLog is the same as LogLog as the only difference between the algorithms is taking the harmonic mean instead of the arithmetic mean, and taking the harmonic mean is still O(m) time. Thus, the time complexity is simply O(m + n).

## HyperLogLog++ and Others
You may have heard of HyperLogLog++ and other varitaions on the HyperLogLog algorithm that improve accuracy and/or add functionality. There are many implementations of these algorithms you can find online and I have linked to some reading on these further improvements below if you are interested.

## Readings
http://algo.inria.fr/flajolet/Publications/FlMa85.pdf - Original paper on the Flajolet-Martin algorithm
https://en.wikipedia.org/wiki/Flajolet%E2%80%93Martin_algorithm - Wikipedia article on Flajolet-Martin

http://algo.inria.fr/flajolet/Publications/DuFl03-LNCS.pdf - Original paper on LogLog and SuperLogLog

http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf - Original paper on HyperLogLog
https://en.wikipedia.org/wiki/HyperLogLog - Wikipedia article for HyperLogLog

https://stefanheule.com/papers/edbt13-hyperloglog.pdf - Original paper on HyperLogLog++
https://research.neustar.biz/2013/01/24/hyperloglog-googles-take-on-engineering-hll/ - An excelent write up on HyperLogLog++
