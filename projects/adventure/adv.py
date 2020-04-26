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

full_knowlege = Knowledge()

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
