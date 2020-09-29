# This problem can be solved with a simple concept from optics.
# Any reflected ray from a mirror is a continuing straight line in the mirror world.
# Hence by calculating the coordinates of the guard in the mirror world,
# we can target him by drawing a straight line to him in the mirror world.
# Similarly this can be extrapolated to several mirror worlds by sequentially
# mirroring the room over and over again in every direction to cover the entire radius of
# impact of the laser gun.
# So now the problem boils down to 2 steps
# 1. Calculating the number of required mirror worlds and the coordinates of the captain and the guard in all of them.
# 2. Checking the path from the captain's original position to every one of the guard's coordinates (original and mirrored)
# to verify that the distance is within the range of the laser and that none of the captain's mirrored coordinates
# or shorter guard's mirrored coordinates are falling on this path. If the captain's mirrored coordinates are on this path,
# it means that the captain will get hit before the laser reaches the guard. If any of the other guard's mirrored coordinates
# falls on this path, it means the guard was already hit once when shot in this angle.


import numpy as np


def solution(dimensions, my_pos, guard_pos, distance):
    w = dimensions[0]
    h = dimensions[1]

    # Utility method for distance between points
    def distance_between_points(p, q):
        dstnc = np.sqrt((q[1] - p[1])**2 + (q[0] - p[0])**2)
        return dstnc

    # Handling the edge case of guard being out of range of the laser to begin with
    if distance_between_points(my_pos, guard_pos) > distance:
        return 0

    # Method to generate the grid of mirrored rooms and coordinates of captain and guard within these mirror worlds
    def grow_grid():

        # Calculate size of grid. This is done by making sure the total width or total height of all the mirror worlds
        # minus the the original width or height of the captain's position (since the radius is from the captain) should
        # exceed the radius of impact.
        estimated_width_number = int(np.ceil(distance/float(w)))
        estimated_height_number = int(np.ceil(distance/float(h)))
        width_number = estimated_width_number if estimated_width_number*w - my_pos[0] >= distance else estimated_width_number+1
        height_number = estimated_height_number if estimated_height_number*h - my_pos[1] >= distance else estimated_height_number+1

        # Use the dimensions of the grid of rooms to get the coordinates of captain and guard in each room
        return get_mirrored_points(my_pos, width_number, height_number), get_mirrored_points(guard_pos, width_number, height_number)

    # Method to return coordinates of captain and guard in all the room (original + mirrored)
    # From simple observation of a how coordinates mirror in a 3x3 grid, we can derive the following equations
    # for coordinates of mirrored points in any given mirrored room in the grid. We return a list of all the possible
    # X's and all the possible Y's, whose cross product is essentially the entire grid.
    def get_mirrored_points(point, width_number, height_number):
        bearings = dict()
        xs = list()
        ys = list()
        x1 = point[0]
        y1 = point[1]
        # Calculate bearings
        for n in range(-width_number, width_number+1):
            if n == 0:
                x_pos = x1
            elif n % 2 == 1:
                x_pos = n*w + (w - x1)
            elif n % 2 == 0:
                x_pos = n*w + x1
            xs.append(x_pos)

        for m in range(-height_number, height_number+1):
            if m == 0:
                y_pos = y1
            elif m % 2 == 1:
                y_pos = m*h + (h - y1)
            elif m % 2 == 0:
                y_pos = m*h + y1
            ys.append(y_pos)

        bearings["X"] = xs
        bearings["Y"] = ys
        return bearings

    # Get the coordinates (bearings) of the captain (me) and the guard
    my_bearings, guard_bearings = grow_grid()

    # To verify each of the guards coordinates, whether it is a valid direction to shoot or not, we employ the following
    # logic. We first calculate all the angles to each of the captain's reflections and the distance to the reflection,
    # which tells us the angle and distance at which the captain might get shot (let's call these danger angles).
    # We save these in a dictionary.
    # Then we calculate the angle and distance from the captain's original position to each of the guard's positions
    # one by one. If the distance is within the range of the laser, we check the dictionary to see if this angle matches
    # any of the captain's danger angles. If it is a danger angle, we check to see if the distance of captain getting shot
    # is less than the distance of guard getting shot (i.e. will the laser reach the captain first or the guard first.)
    # If it is not a danger angle or even if it is, if the distance of guard getting shot is less than the captain, i.e.
    # if the guard gets shot first, then it is safe to shoot in this angle. We add this angle to valid angles list.
    # We also add this angle and distance to our dictionary, so that for the next guard's position, we now check against
    # all of the captains positions, as well as for any duplicates with previously verified guard's angles. This is to make
    # sure guard is not already hit in a particular angle, and we don't end up hitting him twice.
    # Finally we return the length of all the valid angles.
    angle_distance_map = dict()
    valid_angles = set()

    for x in my_bearings["X"]:
        for y in my_bearings["Y"]:
            dist = distance_between_points(my_pos, [x, y])
            if [x, y] != my_pos and dist <= distance:
                angle = np.arctan2(my_pos[1]-y, my_pos[0]-x)
                if angle not in angle_distance_map or (angle in angle_distance_map and angle_distance_map[angle] > dist):
                    angle_distance_map[angle] = dist

    for x in guard_bearings["X"]:
        for y in guard_bearings["Y"]:
            dist = distance_between_points(my_pos, [x, y])
            if dist <= distance:
                angle = np.arctan2(my_pos[1]-y, my_pos[0]-x)
                if angle not in angle_distance_map or (angle in angle_distance_map and angle_distance_map[angle] > dist):
                    angle_distance_map[angle] = dist
                    if angle not in valid_angles:
                        valid_angles.add(angle)

    return len(valid_angles)
