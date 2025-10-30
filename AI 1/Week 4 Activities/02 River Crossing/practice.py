# I recommend you to start coding in another cell below and to keep this cell as a reference.
# That way you can incrementally build --> debug --> build --> debug --> ... your classes  
# instead of trying to do it all at once.

class Node:
    def __init__(self, m_wrong_side, c_wrong_side, boat_wrong_side):
        self.state = ...
        
    def is_goal_state(self):
        ...

    def get_child_node(self, action):
        ...

    ...

        
class Game:
    def __init__(self):
        self.initial_node = Node(m_wrong_side=3, c_wrong_side=3, boat_wrong_side=1)
        ...
    
    def breadth_first_search(self):
        ...