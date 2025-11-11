import numpy as np

class EightQueensState:
    """This class represents a board in the eight queens puzzle"""
    def __init__(self, state=None, n=8):
        """
        :param state: pass in a numpy array of integers to set the state, otherwise will be generated randomly
        :param n: only used if state is not provided, determines size of board (default: 8)
        """
        if state is None:
            self.n = n
            state = np.random.randint(0, n, n)
        else:
            self.n = len(state)
        self.state = state

    @staticmethod
    def copy_replace(state, i, x):
        """This creates a copy of the state (important as numpy arrays are mutable) with column i set to x"""
        new_state = state.copy()
        new_state[i] = x
        return new_state

    @staticmethod
    def range_missing(start, stop, missing):
        """
        This creates a list of numbers with a single value missing
        e.g. range_missing(0, 8, 2) -> [0, 1, 3, 4, 5, 6, 7]
        """
        return list(range(start, missing)) + list(range(missing + 1, stop))

    def cost(self):
        """Calculates the number of pairs attacking"""
        count = 0
        for i in range(len(self.state) - 1):
            # for each queen, look in columns to the right
            # add one to the count if there is another queen in the same row
            count += np.any(self.state[i + 1:] == self.state[i])

            # add one to the count for each queen on the upper or lower diagonal
            upper_diagonal = self.state[i] + np.arange(1, self.n - i)
            lower_diagonal = self.state[i] - np.arange(1, self.n - i)
            count += np.any(self.state[i + 1:] == upper_diagonal)
            count += np.any(self.state[i + 1:] == lower_diagonal)
        return count

    def neighbourhood(self):
        """This generates every state possible by changing a single queen position"""
        neighbourhood = []
        for column in range(self.n):
            for new_position in self.range_missing(0, self.n, self.state[column]):
                new_state = self.copy_replace(self.state, column, new_position)
                neighbourhood.append(EightQueensState(new_state))

        return neighbourhood

    def random_neighbour(self):
        """Generates a single random neighbour state, useful for some algorithms"""
        column = np.random.choice(range(self.n))
        new_position = np.random.choice(self.range_missing(0, self.n, self.state[column]))
        new_state = self.copy_replace(self.state, column, new_position)
        return EightQueensState(new_state)

    def is_goal(self):
        return self.cost() == 0

    def __str__(self):
        if self.is_goal():
            return f"Goal state! {self.state}"
        else:
            return f"{self.state} cost {self.cost()}"

class HillClimber:
    """Applies the hill climbing algorithm to solve the 8 queens puzzle"""
    def __init__(self, state=EightQueensState()):
        self.state = state
        self.n = state.n

    @staticmethod
    def best_neighbour(state):
        """Gets all neighbours from the state, then returns the one with lowest cost"""
        return min(state.neighbourhood(), key=lambda x: x.cost())

    def hill_climb(self):
        """
        Repeatedly take the best neighbour of each state until we find a solution (or get stuck)
        :returns a goal state OR a local minimum (if all options are worse than the current one but it is not a goal)
        """
        if self.state.is_goal():
            return self.state

        while True:
            neighbour = HillClimber.best_neighbour(self.state)
            if neighbour.is_goal():
                return neighbour
            if neighbour.cost() < self.state.cost():
                self.state = neighbour
            else:
                # notice the method gives up if there are no better options
                return self.state

    def iterative_hill_climb(self):
        """Your code goes here!"""
        # so iterative hill climbing is just continuously finding a random state until you can get through it. crazy!
        # originalState = self.state
        # print(originalState)
        if self.state.is_goal():
            return self.state
        while True:
            neighbour = self.state.random_neighbour()
            # print(neighbour) # debug
            if neighbour.is_goal():
                return neighbour
            if neighbour.cost() < self.state.cost():
                self.state = neighbour
            else:
                print("loop") # debug

            if self.state.is_goal():
                return self.state
    
state = EightQueensState()
climber = HillClimber(state)
# solution = climber.iterative_hill_climb()
solution = climber.hill_climb()
print(solution)