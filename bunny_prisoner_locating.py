
def solution(x, y):
    # Consider the structure as a pyramid (from a different angle)
    # The corner would be the top of the pyramid, with increasing levels going down
    # Each level has increasing IDs from left to right

    level_number = x+y-1
    first_id_of_level = (((level_number - 1)*level_number)/2) + 1
    id_of_given_coordinates = first_id_of_level + x - 1
    return str(id_of_given_coordinates)
