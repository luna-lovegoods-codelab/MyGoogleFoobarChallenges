def solution(l):
    # -Split every version number by '.' to get individual major,
    # minor and revision numbers
    # -Sort by integer value of the revision first, then minor, then major,
    # using key functions which return the integer value for each
    # Join the major,minor and revision in the sorted list by '.' and return the string
    return ['.'.join(x) for x in sorted(sorted(sorted([x.split('.') for x in l], key=get_revision), key=get_minor), key=get_major)]


# Key Function that returns integer value of major or -1 if not exists
def get_major(x):
    if len(x) > 0:
        return int(x[0])
    else:
        return -1


# Key Function that returns integer value of minor or -1 if not exists
def get_minor(x):
    if len(x) > 1:
        return int(x[1])
    else:
        return -1


# Key Function that returns integer value of revision or -1 if not exists
def get_revision(x):
    if len(x) > 2:
        return int(x[2])
    else:
        return -1
