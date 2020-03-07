# This problem essentially is about finding the probability of reaching an absorbing state,
# given that the starting state is 0, in an Absorbing Markov Chain.

# The transition probability matrix is given and every state is either transient or absorbing.
# By the Total Probability theorem, we can calculate the probability of reaching a particular state
# by multiplying the conditional probabilities of every state transient along the path and adding the
# these products across all possible paths.

# To come up with a solution, let us consider a 3x3 probability matrix of only transient states - T.
# We need to find all possible paths between these states. For this, let us assume,that it is possible to
# transition from every state to every other state and that there are no 0 probabilities in this matrix.
# If the path had only one step, to get the probability of reaching state 3,
# we add P(3|3)+P(3|2)+P(3|1), by the Total Probability theorem. Each of these elements belongs to the
# 3rd column of the matrix T.
# But if the path had 2 steps, we now have:
# P(3|3)*[P(3|1)+P(3|2)+P(3|3)] + P(3|2)*[P(2|1)+P(2|2)+P(2|3)] + P(3|1)*[P(1|1)+P(1|2)+P(1|3)]
# We multiple every prior probability for 3, with the sum of all possible prior probabilities of the
# previous steps. We find that these 3 elements are the elements of the 3rd column in the matrix T^2.
# Similarly we can also calculate the probability of reaching step 2 and step 1 given
# two steps each. We find that these elements are from column 1 and 2 of the matrix T^2 respectively.
# Similarly, the probabilities for a 3 step chain, are the elements of the matrix T^3.
# Now, since there could be upto infinite steps, and we need to add the probabilities (Total probability
# theorem) for 0 step, 1 step, 2 step, 3 step chains etc, up to infinite steps, the probability of reaching
# any transient state j, starting from a transient state i, given infinite possible paths, is given by
# the i,j element of the matrix 1 + T + T^2 + T^3.... up to infinity. This is a geometric progression
# with common ratio T. Hence the sum to infinity adds up to:
#               S = (I - T)^(-1)
# That is, we subtract from identity matrix and take the inverse. This is analogous to geometric progression
# sum for numbers (1/(1-r)) where r is the common ratio.
# Now, if any of the infinite paths are not possible, the prior probability matrix would have a
# 0 entry and the path probability would automatically become nullified in multiplication.

# Our final step is to multiply these prior probabilities of all possible paths, with the probability
# matrix of reaching an absorbing state from a transient state. Once again, by the total probability
# theorem, we get the probability of reaching absorbing state j, starting from transient state i
# as the i,j entry of this product matrix. The special case of starting state i = 0, which is
# the first row of this matrix, is our solution.

# The following algorithm maintains all the probabilities as fractions through out, as the required
# solution is as a fraction.


from fractions import Fraction as f, gcd


def solution(m):
    if sum(m[0]) == 0:
        # If there is only 1 terminal state, return probability 1.
        if len(m) <= 1:
            return [1, 1]
        else:
            # If there are more than 1 states, but the 0th state itself is a terminal state,
            # return 1 for the 0th state and 0 for every other terminal state as they are unreachable.
            result = list()
            for k in range(len(m)):
                if k == 0:
                    result.append(1)
                else:
                    result.append(0)
            result.append(1)
            return result

    absorbing_states = list()
    T = list()
    A = list()

    # Identify all terminal states
    for i in range(len(m)):
        sm = sum(m[i])
        if sm == 0:
            absorbing_states.append(i)

    # Add probabilities of reaching terminal states to the matrix A
    # and all transient state transition probabilities to the matrix T.
    for row in m:
        t_row = list()
        a_row = list()
        sm = sum(row)
        if sm != 0:
            for i in range(len(m)):
                if i in absorbing_states:
                    a_row.append(f(row[i], sm))
                else:
                    t_row.append(f(row[i], sm))
            T.append(t_row)
            A.append(a_row)

    i_minus_t = list()

    # Calulcate I - T. Since we are maintaining all values in fractions, we refrain
    # from using numpy arrays and manually perform matrix operations. Because the maximum size
    # of given transition matrix will only be 10x10 by design of the problem, this is not computationally
    # too expensive.
    for i in range(len(T)):
        row = list()
        for j in range(len(T)):
            if i == j:
                row.append(f(1, 1) - T[i][j])
            else:
                row.append(f(0, 1) - T[i][j])
        i_minus_t.append(row)

    S = inverse(i_minus_t)     # Inverse of I-T
    R = matrix_multiply(S, A)    # Multiplying inverse of I-T by probability of reaching absorbing states

    # Reducing the probabilities in the 0th row to a common denominator and returning result
    result = list()
    common_denominator = lcm([x.denominator for x in R[0]])
    for element in R[0]:
        factor = common_denominator/element.denominator
        result.append(element.numerator*factor)
    result.append(common_denominator)
    return result


def matrix_multiply(X, Y):
    return [[sum(a*b for a, b in zip(X_row, Y_col)) for Y_col in zip(*Y)] for X_row in X]


def transpose(m):
    return map(list, zip(*m))


def matrix_minor(m, i, j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]


def matrix_determinant(m):
    # 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*matrix_determinant(matrix_minor(m, 0, c))
    return determinant


def inverse(m):
    determinant = matrix_determinant(m)

    # 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    # Calculate co-factor matrix
    co_factors = []
    for r in range(len(m)):
        co_factor_row = []
        for c in range(len(m)):
            minor = matrix_minor(m, r, c)
            co_factor_row.append(((-1)**(r+c)) * matrix_determinant(minor))
        co_factors.append(co_factor_row)

    co_factors = transpose(co_factors)
    for r in range(len(co_factors)):
        for c in range(len(co_factors)):
            co_factors[r][c] = co_factors[r][c]/determinant
    return co_factors


def lcm_two_nums(a, b):
    return a*b/gcd(a, b)


def lcm(lst):
    return reduce(lcm_two_nums, lst)
