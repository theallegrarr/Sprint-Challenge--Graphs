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

def projected_path(starting_room, already_visited=set()):
    # create new empty set for visited rooms
    visited = set()
    # loop over all visited rooms and add them to already visted
    for room in already_visited:
        visited.add(room)

    # create an empty list to hold paths and a tuple of opposite directions
    path = []
    opposite = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

    # create method that adds a room and all possible exits to the path 
    def add_to_path(room, back=None):
        visited.add(room)
        exits = room.get_exits()

        # this loop will repeatedly call its parent method when it moves to a new room
        # that has not been visited
        for direction in exits:
            if room.get_room_in_direction(direction) not in visited:
                path.append(direction)
                add_to_path(room.get_room_in_direction(direction), opposite[direction])

        if back:
            path.append(back)
    
    add_to_path(starting_room)
    
    return path

# create path traversal method
def create_path(starting_room, visited=set()):
    path = []
    opposite = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

    # create method that adds possible paths
    def add_to_path(room, back=None):
        visited.add(room)
        exits = room.get_exits()
        path_lengths = {}

        # create item in path lengths for each projected path in every exit
        for direction in exits:
            path_lengths[direction] = len(projected_path(room.get_room_in_direction(direction), visited))
        
        
        traverse_order = []
        # for every key and value in path lengths, sort and turn into lists
        for key, x in sorted(path_lengths.items(), key=lambda x: x[1]):
            # append every traverse order
            traverse_order.append(key)

        for direction in traverse_order:
            # if the next room has not been visited
            if room.get_room_in_direction(direction) not in visited:
                # in every room add to path
                path.append(direction)
                # continue in the next room
                add_to_path(room.get_room_in_direction(direction), opposite[direction])

        # print(len(visited))
        # check if all rooms have been visited
        if len(visited) == len(world.rooms):
            return
        # if not visited and back is defined then append back
        elif back:
            path.append(back)

    add_to_path(starting_room)
    print(path)
    return path

traversal_path = create_path(world.starting_room)

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
