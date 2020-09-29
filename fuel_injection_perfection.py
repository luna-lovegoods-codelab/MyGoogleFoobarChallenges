# Based on the possible operations given in the problem (+1, -1 or divide by 2), it becomes easier
# to look at the number in a binary format.

# If the number is divisible by 2 (binary ending in 0), it makes sense to always
# divide by 2 first as this drastically reduces the number (it becomes half) and thus reduces the steps
# to take.

# If the number is not divisible by 2, it's binary representation has 2 options - it either
# ends in 01 or ends in 11 (we look at only the last 2 digits as these are the only ones affected by
# adding or subtracting 1, which are the only possible operations here).
# Our aim is to increase the number of halving steps as much as possible, because it reduces the total
# number of steps by reducing the number drastically.

# For a binary number ending in 01, subtracting 1 creates a number that ends in 00. This means we can
# divide by 2 twice, once for each 0 at the end. But if we add 1, the resulting number ends in 10, which
# only lets us divide by 2 once. Hence for a number ending in 01, we subtract 1.

# For a binary number ending in 11, subtracting 1 creates a number ending in 10, which we can only divide
# by 2 once. But adding 0 creates a number ending in 00, which can be divided by 2 twice. Hence, we choose
# to add 0.

# Translating these back into decimal terms (to avoid the redundancy of converting the number to binary
# and back), a binary number ending in 01 translates to a decimal number which leaves reminder 1
# when divided by 4. Similarly a binary number ending in 11 translates to a decimal number which leaves
# reminder 3 when divided by 4. A binary number ending in 0 is divisible by 2. Hence, these are the checks
# we will use in place to conversion to binary, in order to decide our operation. The divison by 4 leaves
# us with a corner case of 3 though, which leaves a reminder of 3 but we need to subtract 1 instead of add
# for optimum steps. Hence, we add a condition for this.


def solution(m):
    m = int(m)
    if m == 0:
        return 0
    steps = 0
    while m != 1:
        if m % 2 == 0:
            m = m/2
        elif m == 3 or m % 4 == 1:
            m -= 1
        else:
            m += 1
        steps += 1
    return steps
