
def solution(x, y):
    # Consider the structure as a pyramid (from a different angle)
    # The corner would be the top of the pyramid, with increasing levels going down ((1,1) is the first level)
    # Each level has increasing IDs from left to right

    # To calculate the ID of a prisoner, we first calculate the level
    # of the pyramid at which the  given x, y coordinates are. Due to the right triangle nature of
    # the levels with the x and y axes, we can deduce that the level number is always x+y-1
    level_number = x+y-1

    # Now we calculate the ID of the last prisoner of the previous level, the one with the highest ID on that level
    # Every level has as many more prisoners as that level number (1st level has 1, second has 2 and so on)
    # Hence, the ID of the last prisoner of the previous level is sum of the natural numbers up to and
    # including that level
    last_id_of_prev_level = (((level_number - 1)*level_number)/2)

    # ID of given coordinates is now just increasing from left to right, which is the x distance,
    # starting at the last ID of the previous level
    id_of_given_coordinates = last_id_of_prev_level + x
    return str(id_of_given_coordinates)
