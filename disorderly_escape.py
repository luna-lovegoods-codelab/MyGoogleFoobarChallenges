# This problem boils down to an application of Polya's enumeration theorem
# to count the number of unique permutations given that a grouping function is applied.
# The grouping function in this case is any transposition of rows or columns in the given matrix.
# Transpositions can be done 1 row/column at a time or even groups of multiple rows/columns at a time.
# Hence, to implement this algorithm we first calculate the different ways in which rows and columns can be
# partitioned, so that the parts are swapped/transposed.
# For each part, we calculate the number of cycles, which is based on the size of the partition.

# The number of states given can be considered as the colors, corresponding to this theorem. We calculate
# the total number of cycles for a combination of a grouping of row parts and a grouping of column parts and
# raise the colors to the power of the total number of cycles. By Polya's theorem, we further sum these
# values and divide by the total number of symmetries, which is all possible row and column swappings. This gives us
# the count of unique configurations by grouping.

from math import factorial
from fractions import gcd


def solution(w, h, s):

    partitions = list()
    for lists in get_partitions(w, h):
        to_add = list()
        for lst in lists:
            to_add.append(Partition(lst, get_cycles(lst)))
        partitions.append(to_add)

    summation = 0
    total_row_column_permutations = factorial(w)*(factorial(h))

    for parts_of_columns in partitions[0]:
        for parts_of_rows in partitions[1]:
            prod = 1
            for col_part_idx in range(0, len(parts_of_columns.part)):
                col_part_cycles = parts_of_columns.part[col_part_idx]
                if col_part_cycles != 0:
                    for row_part_idx in range(0, len(parts_of_rows.part)):
                        row_part_cycles = parts_of_rows.part[row_part_idx]
                        if row_part_cycles != 0:
                            prod = prod*((s**(gcd(col_part_idx+1, row_part_idx+1)))**(col_part_cycles*row_part_cycles))

            prod = prod*(total_row_column_permutations/(parts_of_columns.perms*parts_of_rows.perms))

            summation = summation + prod

    return str(summation/total_row_column_permutations)


def get_partitions(w, h):
    partitions = list()

    identity_part = list()
    identity_part.append(list([1]))
    partitions.append(identity_part)

    lim = max(w, h)
    for part_num in range(2, lim+1):
        for i in range(1, part_num):
                curr_parts = list()
                for max_part in range(min(i, part_num-i), 0, -1):
                    base = (part_num-i)*(part_num-i-1)/2-1
                    parts = partitions[base + max_part]
                    for part in parts:
                        new_part = list(part)
                        while len(new_part) < i:
                            new_part.append(0);

                        new_part[i-1] = new_part[i-1]+1
                        curr_parts.append(new_part)
                partitions.append(curr_parts)

        parts = list()
        part = list()
        while len(part) < part_num-1:
            part.append(0)

        part.append(1)
        parts.append(part)
        partitions.append(parts)

    col_parts = list()  # width wise
    row_parts = list()  # height wise

    base = w*(w-1)/2
    for i in range(0, w):
        col_parts.extend(partitions[base+i])

    if h == w:
        row_parts = col_parts
    else:
        row_parts = list()
        base = h*(h-1)/2
        for i in range(0, h):
            row_parts.extend(partitions[base+i])

    return [col_parts, row_parts]


def get_cycles(part):
    count = 1
    for idx in range(1, len(part)+1):
        permutations = part[idx-1]
        count = count*(factorial(permutations))
        count = count*(idx**permutations)
    return count


class Partition:
    def __init__(self, part, perms):
        self.part = part
        self.perms = perms
