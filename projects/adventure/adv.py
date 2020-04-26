from room import Room
from player import Player
from world import World

from random import choice
from ast import literal_eval

from statistics import mean

#import mlrose
#import numpy as np

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

optimal_start = ['n', 's', 's', 'w', 'e', 'n', 'w', 'e', 'w', 'w', 's']

class Knowledge():
    def __init__(self, player = None, traversal_path = None, traversal_graph = None, map = None, rooms_by_id = None):
        if player is None:
            self.player = Player(world.starting_room)
        else:
            self.player = player

        if traversal_path is None:
            self.traversal_path = []
        else:
            self.traversal_path = traversal_path

        if traversal_graph is None:
            self.traversal_graph = { self.player.current_room.id : { k:'?' for k in self.player.current_room.get_exits() } }
        else:
            self.traversal_graph = traversal_graph

        if map is None:
            self.map = { (self.player.current_room.x, self.player.current_room.y) : self.player.current_room.id }
        else:
            self.map = map

        if rooms_by_id is None:
            self.rooms_by_id = { self.player.current_room.id : self.player.current_room }
        else:
            self.rooms_by_id = rooms_by_id


# Fill this out with directions to walk
# traversal_path = ['n', 'n']

def fill_in_suroundings(room, knowledge):
    map = knowledge.map
    traversal_graph = knowledge.traversal_graph

    if 'n' in traversal_graph[room.id]:
        if (room.x, room.y+1) in map:
            traversal_graph[room.id]['n'] = map[(room.x, room.y+1)]
            traversal_graph[map[(room.x, room.y+1)]]['s'] = room.id
    if 's' in traversal_graph[room.id]:
        if (room.x, room.y-1) in map:
            traversal_graph[room.id]['s'] = map[(room.x, room.y-1)]
            traversal_graph[map[(room.x, room.y-1)]]['n'] = room.id
    if 'e' in traversal_graph[room.id]:
        if (room.x+1, room.y) in map:
            traversal_graph[room.id]['e'] = map[(room.x+1, room.y)]
            traversal_graph[map[(room.x+1, room.y)]]['w'] = room.id
    if 'w' in traversal_graph[room.id]:
        if (room.x-1, room.y) in map:
            traversal_graph[room.id]['w'] = map[(room.x-1, room.y)]
            traversal_graph[map[(room.x-1, room.y)]]['e'] = room.id

def go_in_direction(d, knowledge):
    player = knowledge.player
    traversal_graph = knowledge.traversal_graph
    traversal_path = knowledge.traversal_path
    rooms_by_id = knowledge.rooms_by_id
    map = knowledge.map

    old_room = player.current_room
    player.travel(d)
    rooms_by_id[player.current_room.id] = player.current_room
    if (player.current_room.x, player.current_room.y) not in map:
        map[(player.current_room.x, player.current_room.y)] = player.current_room.id
    if player.current_room.id not in traversal_graph:
        traversal_graph[player.current_room.id] = { k:'?' for k in player.current_room.get_exits() }
        fill_in_suroundings(player.current_room, knowledge)
    traversal_path.append(d)

# def find_path_to_unknown_depth_first():
    # exhausted = {player.current_room.id}

    # potential_path = [('', player.current_room.id)]

    # while potential_path != [] and potential_path[-1][1] != '?':
      # next_vertices = [ (d, id) for d, id in traversal_graph[potential_path[-1][1]].items()
                         # if (d, id) not in potential_path and id not in exhausted ]
      # if next_vertices == []:
        # exhausted.add(potential_path[-1][1])
        # potential_path.pop()
      # else:
        # potential_path.append(next_vertices[0])

      # if potential_path == []:
        # return None

    # return [ d for d, id in potential_path ][1:]

def find_path_to_unknown_bredth_first(knowledge):
    player = knowledge.player
    traversal_graph = knowledge.traversal_graph
    rooms_by_id = knowledge.rooms_by_id
    

    seen = {player.current_room.id}

    potential_paths = [[('', player.current_room.id)]]

    while potential_paths != [] and '?' not in {p[-1][1] for p in potential_paths}:
        potential_paths = [ p + [(d, e)] for p in potential_paths
                                    for d, e in traversal_graph[p[-1][1]].items()
                                    if e not in seen ]
        seen = seen.union({p[-1][1] for p in potential_paths})

    if potential_paths == []:
        return None

    return_paths = [ p for p in potential_paths if p[-1][1] == '?' ]

    return_path = choice(return_paths)
    #return_path = max(return_paths, key=lambda x: (lambda c: abs(c.x) + abs(c.y))(rooms_by_id[x[-2][1]]))

    return [ d for d, id in return_path ][1:]

def take_path_to_unknown(knowledge):
    path = find_path_to_unknown_bredth_first(knowledge)
    if path == []:
        return None

    for d in path:
        go_in_direction(d, knowledge)

def direction_utility(direction, knowledge, trials=10):
    traversal_path = knowledge.traversal_path
    lengths = []

    for _ in range(trials):
        potential_knowledge = Knowledge()

        for d in traversal_path:
            go_in_direction(d, potential_knowledge)

        go_in_direction(direction, potential_knowledge)

        while len(potential_knowledge.traversal_graph) != 500:
            take_path_to_unknown(potential_knowledge)

        lengths.append(len(potential_knowledge.traversal_path))

    utility = min(lengths)
    print("Utility of", direction, ":", utility)

    return utility

# def direction_utility(direction, knowledge):
    # traversal_path = knowledge.traversal_path

    # potential_knowledge = Knowledge()

    # for d in traversal_path:
        # go_in_direction(d, potential_knowledge)

    # go_in_direction(direction, potential_knowledge)

    # while len(potential_knowledge.traversal_graph) != 500:
        # take_path_to_unknown(potential_knowledge)

    # utility = len(potential_knowledge.traversal_path)

    # return utility

def get_optimized_path(knowledge, n = 10000):
    player = knowledge.player
    traversal_graph = knowledge.traversal_graph

    while len(traversal_graph) != 500:
        print(len(knowledge.traversal_path))
        go_in_direction(min(traversal_graph[player.current_room.id],
                            key=lambda d: direction_utility(d, knowledge, n)),
                        knowledge)
        print("Went with", knowledge.traversal_path[-1], ".")

# def get_optimized_path(knowledge):
    # player = knowledge.player
    # traversal_graph = knowledge.traversal_graph

    # while len(traversal_graph) != 500:
        # print(len(knowledge.traversal_path))
        # go_in_direction(min(traversal_graph[player.current_room.id],
                            # key=lambda d: direction_utility(d, knowledge)),
                        # knowledge)
        # print("Went with", knowledge.traversal_path[-1])

# def tsp_path():
    # distances = set()

    # for r in world.rooms.values():
        # for e in r.get_exit_rooms():
            # if r.id < e.id:
                # distances.add((r.id, e.id, 1.0))
            # else:
                # distances.add((e.id, r.id, 1.0))

    # distances = list(distances)

    # fitness_dists = mlrose.TravellingSales(distances = distances)
    # problem_fit = mlrose.TSPOpt(length = 960, fitness_fn = fitness_dists, maximize=False)
    # best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state = 2)
    # print(best_state)
    # print(best_fitness)

# tsp_path()

# full_knowlege = Knowledge()

# Mathematica path conversion.
# optimal_path = [0, 8, 16, 8, 0, 4, 0, 3, 11, 80, 83, 99, 122, 99, 83, 80, 11, 3, 21, \
              # 36, 41, 76, 41, 69, 72, 89, 104, 105, 129, 190, 222, 274, 222, 190, \
              # 129, 105, 225, 226, 260, 266, 379, 266, 260, 226, 225, 105, 104, 126, \
              # 158, 164, 180, 164, 158, 235, 158, 126, 135, 149, 191, 193, 241, 256, \
              # 279, 323, 279, 256, 327, 362, 469, 362, 395, 423, 395, 362, 327, 256, \
              # 241, 193, 203, 269, 315, 406, 410, 406, 315, 335, 346, 335, 378, 466, \
              # 472, 481, 485, 481, 472, 495, 472, 466, 378, 335, 315, 269, 203, 193, \
              # 191, 149, 156, 209, 213, 216, 236, 263, 299, 312, 347, 375, 413, 478, \
              # 493, 478, 413, 419, 413, 375, 393, 375, 347, 437, 347, 312, 355, 457, \
              # 494, 457, 355, 312, 299, 356, 405, 432, 449, 450, 449, 432, 473, 432, \
              # 405, 356, 299, 263, 372, 433, 372, 263, 236, 258, 236, 216, 213, 217, \
              # 271, 310, 271, 217, 213, 209, 156, 177, 215, 243, 215, 220, 314, 339, \
              # 404, 482, 484, 482, 404, 339, 314, 220, 230, 344, 367, 462, 486, 462, \
              # 367, 344, 359, 458, 463, 418, 479, 418, 349, 284, 368, 465, 368, 436, \
              # 368, 284, 470, 284, 254, 205, 162, 128, 194, 227, 194, 128, 92, 100, \
              # 92, 81, 137, 168, 171, 168, 207, 297, 207, 168, 137, 81, 108, 167, \
              # 187, 301, 187, 303, 333, 358, 399, 400, 492, 400, 399, 358, 397, 358, \
              # 333, 365, 447, 365, 414, 365, 333, 303, 352, 303, 187, 167, 108, 81, \
              # 45, 85, 45, 40, 74, 40, 19, 32, 19, 15, 13, 14, 17, 33, 17, 28, 30, \
              # 28, 60, 64, 111, 114, 120, 114, 111, 121, 148, 178, 148, 163, 165, \
              # 197, 199, 281, 392, 408, 443, 477, 443, 408, 392, 281, 350, 425, 434, \
              # 425, 350, 281, 199, 318, 394, 422, 461, 422, 394, 426, 394, 318, 340, \
              # 374, 340, 318, 199, 197, 165, 169, 223, 483, 223, 169, 385, 169, 165, \
              # 163, 228, 253, 285, 253, 228, 163, 257, 388, 386, 354, 361, 366, 497, \
              # 366, 361, 354, 321, 334, 384, 435, 384, 334, 321, 304, 240, 233, 152, \
              # 196, 278, 338, 278, 196, 224, 287, 313, 287, 353, 380, 476, 380, 445, \
              # 446, 445, 480, 445, 380, 353, 287, 224, 196, 152, 147, 154, 192, 239, \
              # 336, 373, 336, 421, 336, 239, 255, 239, 192, 154, 184, 154, 147, 139, \
              # 176, 139, 138, 143, 138, 123, 121, 111, 64, 102, 107, 141, 175, 200, \
              # 328, 200, 204, 200, 175, 141, 107, 102, 64, 60, 28, 17, 46, 79, 106, \
              # 161, 166, 208, 307, 208, 166, 161, 106, 112, 210, 112, 124, 174, 277, \
              # 331, 387, 444, 387, 331, 277, 174, 221, 342, 357, 342, 221, 250, 295, \
              # 332, 351, 417, 442, 417, 351, 453, 351, 332, 295, 250, 289, 319, 441, \
              # 319, 289, 324, 391, 396, 391, 489, 491, 489, 391, 324, 411, 428, 452, \
              # 428, 429, 451, 429, 428, 411, 324, 289, 250, 221, 174, 124, 112, 106, \
              # 79, 46, 61, 82, 155, 185, 292, 316, 341, 316, 292, 185, 195, 185, \
              # 155, 82, 61, 63, 140, 63, 61, 46, 17, 14, 47, 14, 13, 9, 7, 12, 20, \
              # 31, 37, 42, 51, 93, 51, 42, 37, 91, 101, 91, 37, 31, 20, 26, 27, 55, \
              # 56, 73, 132, 172, 132, 73, 56, 67, 84, 86, 146, 86, 95, 109, 136, \
              # 231, 282, 231, 294, 311, 499, 311, 389, 311, 294, 363, 294, 231, 136, \
              # 109, 95, 86, 84, 67, 56, 55, 27, 26, 20, 12, 18, 34, 35, 44, 48, 53, \
              # 75, 88, 125, 198, 270, 300, 320, 471, 320, 300, 270, 198, 125, 238, \
              # 293, 238, 381, 431, 381, 238, 125, 88, 103, 88, 75, 78, 90, 98, 186, \
              # 262, 390, 398, 487, 398, 390, 262, 186, 98, 90, 142, 245, 343, 245, \
              # 142, 90, 78, 75, 53, 48, 44, 59, 189, 275, 283, 376, 468, 376, 283, \
              # 275, 189, 59, 44, 35, 34, 39, 52, 39, 71, 150, 251, 150, 71, 115, \
              # 160, 214, 246, 412, 246, 325, 246, 214, 160, 115, 71, 39, 34, 18, 24, \
              # 29, 54, 29, 24, 25, 43, 77, 130, 77, 43, 49, 119, 131, 329, 407, 329, \
              # 131, 119, 219, 305, 330, 454, 330, 348, 330, 305, 219, 242, 286, 288, \
              # 326, 288, 498, 288, 286, 309, 377, 456, 377, 309, 371, 430, 440, 430, \
              # 371, 309, 286, 242, 219, 119, 49, 43, 25, 24, 18, 12, 7, 1, 22, 1, 2, \
              # 10, 38, 10, 2, 5, 6, 62, 65, 134, 144, 218, 252, 261, 345, 409, 488, \
              # 409, 345, 261, 252, 218, 118, 133, 234, 259, 291, 306, 415, 306, 291, \
              # 259, 234, 280, 234, 247, 369, 247, 234, 133, 151, 188, 151, 133, 118, \
              # 110, 157, 110, 97, 153, 97, 94, 113, 145, 183, 145, 113, 94, 57, 68, \
              # 57, 23, 58, 23, 6, 5, 50, 70, 116, 159, 116, 70, 87, 117, 170, 182, \
              # 211, 248, 272, 248, 211, 182, 170, 117, 127, 212, 229, 237, 370, 237, \
              # 229, 212, 127, 173, 202, 249, 202, 267, 302, 402, 403, 439, 403, 402, \
              # 302, 267, 202, 173, 127, 117, 87, 70, 50, 66, 96, 179, 181, 179, 201, \
              # 206, 232, 244, 264, 290, 264, 244, 232, 265, 268, 276, 459, 467, 459, \
              # 276, 322, 424, 322, 276, 268, 265, 273, 296, 308, 337, 383, 460, 383, \
              # 337, 308, 317, 416, 317, 308, 296, 382, 455, 382, 296, 273, 298, 360, \
              # 364, 401, 420, 464, 420, 401, 427, 474, 427, 438, 448, 490, 448, 475, \
              # 496]
#
# know = Knowledge()
#
# traversal_graph = full_knowlege.traversal_graph
#
# for ids, idt in zip(optimal_path, optimal_path[1:]):
    # direction = dict(map(lambda x: (x[1], x[0]), traversal_graph[ids].items()))[idt]
    # go_in_direction(direction, know)
#
# print(know.traversal_path)

# Optimal traversal.
traversal_path = ['s', 'w', 'e', 'n', 'n', 's', 'w', 'w', 's', 'w', 's', 's', 'n', 'n', 'e', 'n', 'e', 'n', 'w', 'w', 's', 'n', 'w', 's', 's', 's', 'w', 'n', 'w', 'w', 'w', 'e', 'e', 'e', 's', 'w', 'w', 's', 'w', 'n', 's', 'e', 'n', 'e', 'e', 'e', 's', 'w', 's', 'w', 'e', 'n', 'w', 'e', 'e', 's', 's', 's', 's', 'w', 's', 's', 's', 'n', 'n', 'w', 's', 'w', 'e', 's', 'w', 'e', 'n', 'n', 'e', 'n', 'e', 's', 's', 's', 's', 'w', 'e', 'n', 'e', 's', 'n', 'e', 's', 's', 's', 'w', 'e', 'n', 'e', 'w', 'n', 'n', 'w', 'w', 'n', 'n', 'n', 'n', 'n', 'w', 's', 'w', 'w', 'w', 's', 's', 'w', 's', 's', 's', 'w', 'w', 'e', 'e', 's', 'n', 'n', 'w', 'e', 'n', 'w', 'e', 'n', 'w', 'w', 'w', 'e', 'e', 'e', 'e', 's', 's', 's', 's', 'e', 'w', 'n', 'e', 'w', 'n', 'n', 'n', 'n', 'w', 'w', 'e', 'e', 'n', 'w', 'e', 'e', 'e', 's', 'w', 's', 'n', 'e', 'n', 'e', 'n', 'w', 'w', 'n', 's', 'w', 'w', 'w', 's', 'w', 's', 'n', 'e', 'n', 'e', 'e', 'n', 'w', 'w', 'n', 'w', 'e', 's', 'e', 'n', 'n', 'w', 'n', 'w', 'e', 'e', 'n', 'w', 'w', 'e', 'n', 's', 'e', 'n', 's', 'e', 'e', 'e', 'n', 'w', 'w', 'e', 'e', 'e', 's', 'n', 'n', 'n', 'w', 'w', 'e', 'n', 'w', 'e', 's', 'e', 's', 'w', 'w', 'w', 'w', 'e', 'n', 'w', 'n', 'w', 'w', 'w', 'e', 'e', 'e', 'n', 's', 's', 'w', 's', 'n', 'w', 'e', 'e', 'e', 'n', 's', 's', 'e', 'e', 'e', 'e', 'n', 's', 'e', 'n', 's', 'e', 'n', 's', 'e', 'e', 'n', 'n', 'n', 's', 'e', 's', 'n', 'n', 'n', 'n', 'e', 'e', 'w', 'w', 'n', 'n', 'e', 'w', 'n', 'w', 'w', 'w', 'n', 'w', 'n', 'n', 'w', 'e', 's', 's', 'e', 'n', 'n', 'n', 's', 's', 's', 's', 'w', 'w', 'w', 'n', 's', 'e', 'n', 's', 'e', 's', 'w', 'e', 'n', 'e', 'e', 'e', 'n', 'w', 'n', 's', 'e', 'n', 's', 's', 'e', 'e', 'n', 'n', 's', 's', 'w', 'n', 'n', 'n', 'e', 'n', 'w', 'w', 'e', 'e', 's', 'e', 'n', 'e', 'e', 'w', 'w', 's', 's', 's', 's', 'e', 'n', 'n', 'n', 's', 's', 'e', 'n', 'n', 's', 'e', 'n', 'n', 's', 'e', 'e', 'w', 's', 'n', 'w', 's', 'w', 's', 'w', 's', 's', 'e', 'n', 'e', 'e', 'n', 's', 'e', 'w', 'w', 'n', 's', 'w', 's', 'e', 'w', 'w', 's', 'e', 'w', 'w', 'n', 's', 'w', 'w', 's', 's', 'w', 'n', 'n', 'w', 'n', 'w', 'e', 'e', 'w', 's', 'e', 's', 's', 'e', 's', 's', 'w', 'w', 'w', 'w', 'n', 'n', 'w', 'n', 's', 'e', 's', 's', 'w', 'n', 's', 'w', 'n', 'n', 'n', 'n', 'n', 's', 's', 's', 's', 'w', 'w', 'w', 'e', 'e', 'n', 'n', 'n', 'n', 'n', 'n', 's', 's', 'w', 'e', 's', 's', 's', 'w', 'n', 'n', 's', 's', 'w', 'n', 'w', 'e', 'n', 'n', 's', 's', 's', 'w', 'w', 'w', 'e', 's', 'w', 'e', 'n', 'e', 'e', 'e', 'e', 's', 'e', 's', 'e', 'e', 'e', 'e', 'n', 'n', 'n', 'w', 'w', 'n', 'w', 'e', 's', 'e', 'n', 's', 'e', 's', 's', 'w', 'n', 's', 'e', 's', 'e', 's', 'w', 'e', 's', 'e', 's', 'e', 'n', 'n', 'n', 'e', 'n', 'n', 's', 's', 'w', 'n', 'n', 's', 's', 's', 's', 'e', 'n', 'e', 'n', 'n', 'n', 'n', 's', 's', 's', 'e', 'n', 'n', 'n', 's', 'e', 'n', 'n', 'e', 'n', 's', 'e', 'e', 'e', 'w', 'n', 's', 'w', 'n', 's', 'w', 'w', 's', 's', 'w', 's', 's', 'w', 's', 'w', 's', 'w', 's', 'e', 'e', 'n', 'e', 'n', 'e', 'n', 'e', 'e', 's', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 'n', 'e', 'e', 'w', 'n', 'e', 'w', 's', 'w', 'w', 's', 'n', 'w', 'n', 'e', 'n', 'n', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 's', 's', 'e', 'n', 'e', 'w', 's', 'w', 'w', 's', 's', 'w', 's', 'e', 'e', 'e', 'e', 'e', 's', 'n', 'w', 'w', 'w', 'w', 'w', 'w', 's', 'e', 's', 'n', 'e', 'e', 'e', 'w', 'w', 's', 'e', 'e', 'e', 'e', 'w', 'n', 's', 'w', 'w', 'w', 'n', 'w', 'w', 'w', 's', 's', 's', 'n', 'n', 'e', 's', 's', 'e', 'w', 'n', 'e', 'e', 'e', 'e', 'e', 'w', 'w', 'w', 's', 'e', 'e', 'e', 'w', 's', 'n', 'w', 'w', 's', 's', 'e', 'n', 's', 'e', 'w', 'w', 's', 'e', 'e', 'w', 'w', 's', 'e', 'e', 'w', 'w', 'n', 'n', 'n', 'n', 'n', 'w', 'w', 'n', 'w', 'n', 'w', 'w', 's', 'e', 'w', 's', 'e', 's', 'n', 'w', 's', 'w', 's', 's', 's', 's', 's', 's', 's', 's', 's', 's', 'n', 'n', 'n', 'n', 'n', 'w', 'w', 's', 'e', 's', 's', 's', 'n', 'n', 'n', 'w', 's', 'n', 'w', 's', 'n', 'e', 'n', 'w', 'n', 's', 'e', 'e', 'n', 'w', 'e', 'n', 'w', 'e', 'n', 'w', 'w', 's', 'n', 'e', 'e', 'n', 'w', 'e', 'n', 'w', 'e', 'e', 'e', 's', 'e', 's', 's', 'n', 'n', 'e', 's', 'e', 'n', 'e', 's', 's', 'n', 'n', 'w', 's', 'w', 's', 's', 's', 's', 'e', 'w', 'n', 'n', 'n', 'e', 's', 'e', 'w', 's', 'e', 'e', 'e', 'e', 'w', 'w', 'w', 'w', 'n', 'n', 'w', 'n', 'n', 'w', 'w', 's', 's', 's', 's', 'n', 'e', 's', 's', 'w', 's', 's', 'n', 'n', 'e', 's', 's', 's', 's', 's', 'n', 'n', 'w', 's', 'n', 'e', 'n', 'n', 'e', 's', 'e', 'e', 's', 's', 'n', 'n', 'w', 's', 's', 'n', 'n', 'w', 's', 's', 'n', 'n', 'n', 'e', 'e', 'n', 'e', 's', 's', 'n', 'n', 'e', 'e', 'w', 's', 's', 'e', 'w', 's', 's']

player = Player(world.starting_room)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
