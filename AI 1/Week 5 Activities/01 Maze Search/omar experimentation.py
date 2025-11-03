from priorityqueue import PriorityQueue
import copy
import random
import mazegen

# random.seed(0)

# height = 10
# width = 20

# maze = mazegen.mazegen(height, width)
# mazegen.print_maze(maze)

# here is an implementation of our heuristic function
# note this function will be redefined in the code later
def h_cost(space, goal):
    return abs(goal[0] - space[0]) + abs(goal[1] - space[1])

class Node:
    def __init__(self, state, parent=None):
        self.state = state # A* is different where the parent's cost is also calculated
        self.parent = parent

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.state < other.state

    def __hash__(self):
        return hash(self.state)

    def __str__(self):
        return f"Node space {self.state}"

# this imports from priority queue

# when a state is pushed, its heuristic cost is calculated (manhattan distance which is goal state - cur state)
# what does it mean, whats updated??
# not sure about the third point
class Frontier:
    # Note the heuristic function is passed in as a parameter
    # Python borrows some nice features from functional programming
    def __init__(self, heuristic, start_node=None):
        self.heuristic = heuristic
        # gives itself a heuristic law
        self.queue = PriorityQueue()
        self.states = set()
        # produces a queue and has a set of states intialised
        if start_node is not None:
            self.push(start_node)
            
    def push(self, node):
        cost = self.heuristic(node)
        # get_priority returns math.inf if the task is not in the queue
        if cost < self.queue.get_priority(node):
            self.queue.push(node, priority=cost)
            self.states.add(node.state)
        
    def pop(self):
        node = self.queue.pop()
        self.states.remove(node.state)
        return node
        
    def contains(self, state):
        return state in self.states
    
    def length(self):
        return self.queue.length()

def valid_space(maze, space):
    return 0 <= space[0] < len(maze) \
           and 0 <= space[1] < len(maze[0]) \
           and maze[space[0]][space[1]] == '.'

def greedy_search(maze, start=(0, 0), goal=None):
    if goal is None:
        goal = (len(maze) - 1, len(maze[0]) - 1)

    # here's our Manhattan distance heurstic, as a lambda expression
    heuristic = lambda node: abs(goal[0] - node.state[0]) + abs(goal[1] - node.state[1])
    frontier = Frontier(heuristic, Node(start))
    explored = set()

    current_node = frontier.pop()
    number_explored = 0
    
    while not current_node.state == goal:
        current_state = current_node.state

        number_explored += 1
        explored.add(current_state)
        
        # the four neigbouring locations
        right = (current_state[0], current_state[1] + 1)
        left = (current_state[0], current_state[1] - 1)
        down = (current_state[0] + 1, current_state[1])
        up = (current_state[0] - 1, current_state[1])
        
        for space in [right, left, down, up]:
            if valid_space(maze, space) \
               and space not in explored:
                node = Node(space, parent=current_node)
                frontier.push(node)

        if frontier.length() == 0:
            return None, number_explored

        current_node = frontier.pop()
    
    return current_node, number_explored

# here is the "main" code, we generate a new maze then try the search
# try changing the random seed to try different mazes (not all are solvable)
height = 10
width = 20

random.seed(0)
maze = mazegen.mazegen(height, width)
final_node, number_explored = greedy_search(maze)

if final_node is None:
    print("No path exists!\n")
    mazegen.print_maze(maze)
else:
    node = final_node
    steps = 0
    while node.parent is not None:
        state = node.state
        maze[state[0]][state[1]] = 'X'
        steps += 1
        node = node.parent

    state = node.state
    maze[state[0]][state[1]] = 'X'
    mazegen.print_maze(maze)
    
    print(f"Total steps on path: {steps}")
    print(f"Total states explored: {number_explored}")



# PART 2
# this is a differently defined node.
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        if parent is None:
            self.path_cost = 0
        else:
            self.path_cost = parent.path_cost + 1

    def __eq__(self, other):
        return self.state == other.state

    def __lt__(self, other):
        return self.state < other.state

    def __hash__(self):
        return hash(self.state)

    def __str__(self):
        return f"Node space {self.state}"

def a_star_search(maze, start=(0, 0), goal=None):
    if goal is None:
        goal = (len(maze) - 1, len(maze[0]) - 1)

    # This is the key line that turns the greedy search into A*
    heuristic = lambda node: node.path_cost + \
                             abs(goal[0] - node.state[0]) + abs(goal[1] - node.state[1])
    frontier = Frontier(heuristic, Node(start))
    explored = set()

    current_node = frontier.pop()
    number_explored = 0
    
    while not current_node.state == goal:
        current_state = current_node.state

        number_explored += 1
        explored.add(current_state)
        
        # the four neigbouring locations
        right = (current_state[0], current_state[1] + 1)
        left = (current_state[0], current_state[1] - 1)
        down = (current_state[0] + 1, current_state[1])
        up = (current_state[0] - 1, current_state[1])
        
        for space in [right, left, down, up]:
            if valid_space(maze, space) \
               and space not in explored:
                node = Node(space, parent=current_node)
                frontier.push(node)

        if frontier.length() == 0:
            return None, number_explored

        current_node = frontier.pop()
    
    return current_node, number_explored

# The main code is mostly the same as above, just have to call the correct function!
height = 10
width = 20

random.seed(0)
maze = mazegen.mazegen(height, width)
final_node, number_explored = a_star_search(maze)

if final_node is None:
    print("No path exists!\n")
    mazegen.print_maze(maze)
else:
    node = final_node
    steps = 0
    while node.parent is not None:
        state = node.state
        maze[state[0]][state[1]] = 'X'
        steps += 1
        node = node.parent

    state = node.state
    maze[state[0]][state[1]] = 'X'
    mazegen.print_maze(maze)
    
    print(f"Total steps on path: {steps}")
    print(f"Total states explored: {number_explored}")

# This helper function makes the code cleaner in the next cell



def display_results(maze, final_node, number_explored):
    if final_node is None:
        print("No path exists!\n")
        mazegen.print_maze(maze)
    else:
        maze = copy.deepcopy(maze)
        node = final_node
        steps = 0
        while node.parent is not None:
            state = node.state
            maze[state[0]][state[1]] = 'X'
            steps += 1
            node = node.parent

        state = node.state
        maze[state[0]][state[1]] = 'X'
        mazegen.print_maze(maze)

        print(f"Total steps on path: {steps}")
        print(f"Total states explored: {number_explored}")
        print()

height = 10
width = 50

random.seed(1)
maze = mazegen.mazegen(height, width, obstacle_weight=0.3)

final_node, number_explored = greedy_search(maze)
display_results(maze, final_node, number_explored)

final_node, number_explored = a_star_search(maze)
display_results(maze, final_node, number_explored)