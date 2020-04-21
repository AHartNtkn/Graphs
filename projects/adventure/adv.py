from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

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

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

traversal_graph = { player.current_room.id : { k:'?' for k in player.current_room.get_exits() } }

def go_in_direction(d):
    old_room = player.current_room
    player.travel(d)
    traversal_graph[old_room.id][d] = player.current_room.id
    if player.current_room.id not in traversal_graph:
        traversal_graph[player.current_room.id] = { k:'?' for k in player.current_room.get_exits() }
    traversal_path.append(d)

def find_path_to_unknown_depth_first():
    exhausted = {player.current_room.id}

    potential_path = [('', player.current_room.id)]

    while potential_path != [] and potential_path[-1][1] != '?':
      next_vertices = [ (d, id) for d, id in traversal_graph[potential_path[-1][1]].items()
                         if (d, id) not in potential_path and id not in exhausted ]
      if next_vertices == []:
        exhausted.add(potential_path[-1][1])
        potential_path.pop()
      else:
        potential_path.append(next_vertices[0])

      if potential_path == []:
        return None

    return [ d for d, id in potential_path ][1:]

def find_path_to_unknown_bredth_first():
    seen = {player.current_room.id}

    potential_paths = [[('', player.current_room.id)]]

    while potential_paths != [] and '?' not in {p[-1][1] for p in potential_paths}:
        potential_paths = [ p + [(d, e)] for p in potential_paths
                                    for d, e in traversal_graph[p[-1][1]].items()
                                    if e not in seen ]
        seen = seen.union({p[-1][1] for p in potential_paths})

    if potential_paths == []:
        return None

    return_path = [ p for p in potential_paths if p[-1][1] == '?' ][-1]

    return [ d for d, id in return_path ][1:]

def take_path_to_unknown():
    path = find_path_to_unknown_bredth_first()
    if path == []:
        return None

    for d in path:
        go_in_direction(d)

while len(traversal_graph) != 500:
    take_path_to_unknown()


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
