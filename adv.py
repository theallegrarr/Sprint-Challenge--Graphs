from room import Room
from player import Player
from world import World
from collections import defaultdict
from util import Stack, Queue

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
opposite_direction = { 'n': 's', 's': 'n','e': 'w','w': 'e'}

graph = {}

# finding the last room with BFS
def breadth_first_search(graph, starting_room):
    queue = Queue()
    visited_set = set()
    queue.enqueue([starting_room])

    while queue.size():
        path = queue.dequeue()
        next_room = path[-1]

        # if next room has not been visited
        if next_room not in visited_set:
            visited_set.add(next_room)

            # check all exits in the next room
            for room in graph[next_room]:
                # check if an exit has been visited
                if graph[next_room][room] == 'visited':
                    return path
            
            for any_exit in graph[next_room]:
                # set the exit to be tracked to a variable
                neighboring_room = graph[next_room][any_exit]
                
                # copy the path
                new_path = list(path)
                new_path.append(neighboring_room)

                # save the path
                queue.enqueue(new_path)


while len(graph) < len(room_graph):
    current_room_id = player.current_room.id
    
    # if current room is not yet in the graph
    if current_room_id not in graph:
        # insert the room as an empty dict
        graph[current_room_id] = {}

        # loop over the exits
        for room_exits in player.current_room.get_exits():
            # check if they have been visited
            graph[current_room_id][room_exits] = "visited"

    
    # loop over any direction a room can go
    for direction in graph[current_room_id]:
        # check if player can not move beyond room
        if direction not in graph[current_room_id]:
            break

        # check if all exits have been visited
        if graph[current_room_id][direction] == 'visited':
            
            # if there is an exit in the dictionary
            if direction is not None:
                traversal_path.append(direction)
                player.travel(direction)
                
                # create a variable to hold current room id
                room_id = player.current_room.id

                # if the room_id has not been visited
                if room_id not in graph:
                    graph[room_id] = {}

                    # for each available exit in the room, set exits to visited
                    for any_exit in player.current_room.get_exits():
                        graph[room_id][any_exit] = 'visited'

            # set previous room directions and exits
            graph[current_room_id][direction] = room_id
            graph[room_id][opposite_direction[direction]] = current_room_id
            current_room_id = room_id

    # using BFS, with parameters for graph and current room
    bfs_path = breadth_first_search(graph, player.current_room.id)
    
    # create directions using all rooms in the path and appending all directions
    if bfs_path is not None:
        for room in bfs_path:
            for any_exit in graph[current_room_id]:
                if graph[current_room_id][any_exit] == room:
                    traversal_path.append(any_exit)
                    # move in that direction
                    player.travel(any_exit)

    current_room_id = player.current_room.id


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
