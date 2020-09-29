# This problem is at its core a graph theory problem.
# Consider the given matrix's rows - the bunnies, start, bulkhead and
# any checkpoints - as vertices in a graph. The transitions between the
# vertices would be the edges of the graph, with the time taken for the
# transition being the weight of the edge. This would be a directional
# graph (digraph)since the time taken can be different for the reverse transition.
# Negative weights (adding time; eg. checkpoints) and negative weight
# cycles are possible. The goal is to find the path through the graph
# from start to the bulkhead, whose cumulative weight is less than the
# given time limit and covers the maximum number of vertices.

# If the graph has at least one negative cycle, we can keep going through
# the negative cycle to keep adding the required time to get to every bunny
# and thus reach all the bunnies. Hence, the solution is all bunnies.

# If the graph does not have a negative cycle, we take the following approach.
# We find all possible paths in the graph with only 2 vertices, 3 vertices etc.,
# up to the paths with all vertices. For each of these paths, we calculate the
# the time taken (cumulative weight), and we consider the path as valid only if
# time taken is less than the time limit. As our goal is to maximize the number
# of bunnies, as we increment the number of vertices, we consider the possible
# paths for the maximum number of vertices where weight is less than the time limit.
# If there are multiple such max. vertices paths, we sort them to return the one
# starting with the lowest bunny. To get all possible n vertex paths efficiently,
# we use the logic that every n-vertex path whose weight "could" be lesser than max time,
# can be represented as the sum of an (n-1)-vertex path whose weight is definitely
# lesser than max time, and an additional vertex. Hence, we can recursively calculate
# n-vertex paths by caching the valid (n-1)-vertex paths and their weights, and combining
# them with every other additional vertex possible and adding shortest time to reach
# that vertex.
#
# We get the shortest time to reach the vertex using the Bellman-Ford
# algorithm. This algorithm iterates over all edges and "relaxes" an edge
# if it decreases the distance from start to the second point of the edge, i.e. update
# the shortest distance to the second point of the edge. We do this iteratively
# over all edges n times, where n is number of vertices - 1. This ensures
# all vertices are accounted for in finding the shortest distance (the -1 is because
# an edge has 2 vertices and thus last vertex is accounted for by virtue of counting the
# edges of the rest). We use the Bellman-Ford algorithm as opposed to other algorithms
# here as this algorithm also provides the flexibility of detecting negative weight
# cycles. When we iterate over the edges for all vertices, when optimal distances
# for all vertices are reached, no edges are relaxed in the next iteration. After
# all the iterations, if no such optimal solution is reached and edge relaxation
# is still possible (i.e. possible to calculate a shorter distance), then
# a negative cycle is detected in the graph which can potentially endlessly reduce
# the distance. This is useful for the trivial case mentioned above.


def solution(matrix, max_time):

    # This function implements the Bellman Ford Algorithm to return
    # the shortest distance to every vertex in the graph, given a source
    # vertex (starting vertex). It also returns a boolean for whether
    # a negative cycle is detected in the graph.
    def bellman_ford(start):
        # Initialize distance to all vertices from start as infinity.
        distances = [float('inf')]*len(matrix)

        # Distance of start to itself is 0.
        distances[start] = 0

        for i in range(len(matrix) - 1):
            num_edges_relaxed = 0
            for x, y, distance in edges:
                if distances[x] + distance < distances[y]:
                    num_edges_relaxed += 1
                    distances[y] = distances[x] + distance

            # If the number of edges relaxed in this iteration is 0,
            # we can terminate the loop prematurely as no vertex was updated
            # and all distances are optimal.
            if num_edges_relaxed == 0:
                break

        return distances, True if num_edges_relaxed > 0 else False

    # Get list of edges for the given matrix in graph form.
    # Each edge is a tuple of first vertex, second vertex and distance - (x,y,distance)
    def get_edges():
        edges = []
        for x, row in enumerate(matrix):
            for y, distance in enumerate(row):
                edges.append([x, y, distance])
        return edges


    # This function recursively gets all possible paths with number
    # of vertices n.
    def generate_all_paths(n):
        # If n is 1, return the sorted list of vertices.
        if n == 1:
            return sorted(bunny_vertices)
        else:
            # Construct all n-paths using the cached (n-1)-paths.
            paths = list()
            valid_path_keys = valid_paths.keys()
            for path in valid_path_keys:
                for index in bunny_vertices:
                    # A vertex can only appear once in a path.
                    if index in path:
                        continue
                    current_path = path + index
                    if current_path[1:] in valid_path_keys:
                        paths.append(current_path)
            return paths

    # Cache to hold the valid paths
    valid_paths = dict()

    # Generate the list of bunny IDs from the matrix.
    bunny_vertices = [str(bunny + 1) for bunny in range(len(matrix) - 2)]

    # Generate the list of edges from the graph.
    edges = get_edges()

    # Use the Bellman-Ford implementation to test for negative
    # cycles and compute the shortest times from every vertex
    # to every other vertex.
    shortest_time_matrix = []
    negative_cycle = False
    for vertex in range(len(matrix)):
        distances, negative_cycle = bellman_ford(vertex)
        shortest_time_matrix.append(distances)

    # If there is a negative cycle, all bunnies can be rescued.
    if negative_cycle > 0:
        return range(len(matrix) - 2)

    # Set the start and end vertices.
    start = 0
    end = len(matrix) - 1

    # Iterate over all possible path lengths.
    for path_length in range(1, len(bunny_vertices) + 1):
        valid_paths_new = {}

        # Generate all possible paths for the current number of vertices.
        paths = generate_all_paths(path_length)

        # If there are no valid paths for the current length, there will be no
        # further valid paths of greater length either. Hence we can end the loop.
        if len(paths) <= 0:
            break

        # Test every path to see if it is still within the time limit. We do
        # this by using the cached weight of the sub path and adding the shortest
        # time to reach the additional vertex (pre-computed from the Bellman-Ford).
        for path in paths:
            if len(path) >= 2:
                sub_path = path[:-1]
                sub_path_time = valid_paths[sub_path]
                path_time = sub_path_time - \
                            shortest_time_matrix[int(sub_path[-1])][end] + \
                            shortest_time_matrix[int(sub_path[-1])][int(path[-1])] + \
                            shortest_time_matrix[int(path[-1])][end]
            else:
                path_time = shortest_time_matrix[start][int(path[0])] + \
                            shortest_time_matrix[int(path[0])][end]

            if path_time <= max_time:
                valid_paths_new[path] = path_time

        # If there are no valid paths for the current length, there will be no
        # further valid paths of greater length either. Hence we can end the loop.
        if len(valid_paths_new) <= 0:
            break

        # Replace the cached paths with the newly computed paths. We only
        # need to cache the results of 1 previous iteration as we are working
        # towards path with maximum vertices and we don't need anything other
        # than 1 iteration prior, to do so.
        valid_paths = valid_paths_new

    # Sort the final paths with maximum number of vertices to get the path starting
    # with minimum ID bunny.
    sorted_paths = sorted([sorted(path) for path in valid_paths.keys()])

    # The first element of the array is our final answer.
    return [int(a) - 1 for a in sorted_paths[0]]