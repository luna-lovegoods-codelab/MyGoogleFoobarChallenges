# This problem, at its core, is a partition problem in Number theory.
# The problem can be defined as the number of partitions of a number n
# in which there are atleast 2 non-zero parts and the parts are all distinct.
# From Euler's generating function for the infinite
# sequence of the number of partitions of n, a recurrence relation
# for the number of partitions can be derived as follows:
#       p(n) = (1/n)*sum(sigma(k)*p(n-k))
# where sigma(k) is the number of divisors of k, p(n-k) is the number of
# partitions of the number n-k and the sum is over k from 1 to n.
# But in this problem, we are interested in the partitions of n with distinct parts only.
# By a property of integer partitions, the number of partitions with distinct parts
# is always equal to the number of partitions with odd parts.
# We can derive a recurrence relation for the number of partitions with odd parts
# where the sum of divisors in the above relation is relaced with the sum of odd
# divisors only. This gives us the total  number of partitions with distinct parts as follows:
#      q(n) = (1/n)*sum(sigma_(k)*q(n-k))
# where q(n) is number of partitions with distinct parts,
# sigma_(k) is sum of odd divisors of k and sum is over k from 1 to n.
# Finally, we subtract 1 for the trivial case of the partition with
# only 1 element - the number itself.

import numpy as np

#Global lookup table to cache the number of partitions of a number
lookup = dict()


def solution(n):
    #Subtracting 1 for the trivial case of partition with only 1 part
    return number_of_partitions(n) - 1


def number_of_partitions(n):
    # Check lookup table first to avoid recalculation
    if n in lookup.keys():
        return lookup[n]

    #Initialize summation
    summation = 0

    #Initializing q(0) = q(1) = 1
    if n == 0:
        return 1

    if n == 1:
        return 1

    #Loop for summation over k from 1 to n
    for k in range(1, n+1):
        #Recursive call for q(n-k)
        num_parts_n_minus_k = number_of_partitions(n-k)
        #Incremental summation
        summation = summation + sum_of_odd_divisors(k)*num_parts_n_minus_k

    #Multiplying the sum by 1/n
    num_parts = summation/n

    #Adding value to lookup table for faster retrieval
    lookup[n] = num_parts

    return num_parts

#Function to calculate sum of odd divisors
def sum_of_odd_divisors(k):
    i = 1
    sm = 0

    while i <= np.sqrt(k):
        #If number of divisible by i and i is odd, add i to sum
        if k % i == 0:
            if i % 2 == 1:
                sm = sm+i
            #Since i is a factor of k, k/i is also a factor of k
            #If k/i is different from i and it is odd, ass k/i to sum
            #By adding k/i here, the loop can stop at sqrt(k) and we
            #need not check for i upto k.
            if k/i != i and (k/i) % 2 == 1:
                sm = sm+(k/i)

        i = i+1
    return sm
