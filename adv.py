from room import Room
from player import Player
from world import World
from util import Stack

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

def dft(starting_room):
    print("|||||||||||||||||||||||||||")
    s = Stack()
    visited = {}
    start_directions = starting_room.get_exits()
    opposites = {"n":"s", "e":"w", "s":"n", "w":"e"}
    print(start_directions)

    for d in start_directions:
        s.push(d)
        print(f"\n\n{d}\n\n")
        
        path = []
        forks = []

        while s.size() > 0:
            curr_move = s.pop()
            traversal_path.append(curr_move)
            
            curr_room = player.current_room.id
            ### Check if the room we're in has multiple routes
            if len(player.current_room.get_exits()) > 2:
                if curr_room not in forks:
                    forks.append(curr_room)
                print("FORKS", forks)

            ### move
            player.travel(curr_move)
            move_room = player.current_room
            ### Keep track of where we need to return to
            path.insert(0, opposites[curr_move])


            print(f"{curr_room} == {curr_move} ==> {move_room.id}")

            if move_room.id == starting_room.id:
                print("continue")
                s.pop()
                # path=[]
                # continue

            #### Add connections to graph
            if curr_room not in visited:
                visited[curr_room] = {curr_move: move_room.id}
            else:
                visited[curr_room].update({curr_move: move_room.id})
            if move_room.id not in visited:
                visited[move_room.id] = {opposites[curr_move]: curr_room}


            ### Find which way player can move
            exits = move_room.get_exits()
            for e in exits:
                if e not in visited[move_room.id]:
                    next_room = {e: "?"}
                    visited[move_room.id].update(next_room)
                    s.push(e)
            print("Exits", exits)

            ### Move back if we're at a dead end
            if len(exits) == 1:
                print("REVERSE PATH ", path)
                to_pop = 0
                for p in path:
                    print("P in path:", p)
                    to_pop += 1
                    room = player.current_room.get_room_in_direction(p)

                    if len(forks) > 0 and room == forks[0]:
                        fork_exits = player.current_room.get_exits()
                        count = len(fork_exits)
                        for e in fork_exits:
                            room = player.current_room.get_room_in_direction(e)

                            if room in visited:
                                count -= 1

                        if count == 0:
                            forks.pop(0)
                            print("Break")
                        break
                print(to_pop)
                for i in range(to_pop-1):
                    print(i)
                    move = path.pop(0)
                    traversal_path.append(move)
                    player.travel(move)
                    print("each path", path)
                print("NEWPATH", path)
                print("Current room", player.current_room.id)
                

                    
            
        print("\nVISITED", visited, "\n")

        # print("REVERSE movements ", reverse)
        # for r in reverse:
        #     traversal_path.append(r)
        #     player.travel(r)          


dft(player.current_room)
print("PATH: ", traversal_path)
# TRAVERSAL TEST - DO NOT MODIFY
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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
