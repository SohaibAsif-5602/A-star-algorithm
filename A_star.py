import heapq

class PuzzleNode:
    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def heuristic(state, goal_state):
    total_distance = 0
    for i in range(3):
        for j in range(3):
            value = state[i][j]
            if value != 0:
                goal_i, goal_j = next((x, y) for x, row in enumerate(goal_state) for y, val in enumerate(row) if val == value)
                total_distance += abs(i - goal_i) + abs(j - goal_j)
    return total_distance

def get_neighbors(node):
    neighbors = []
    zero_i, zero_j = next((i, j) for i, row in enumerate(node.state) for j, val in enumerate(row) if val == 0)
    
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for move_i, move_j in moves:
        new_i, new_j = zero_i + move_i, zero_j + move_j
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = [row.copy() for row in node.state]
            new_state[zero_i][zero_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[zero_i][zero_j]
            neighbors.append(PuzzleNode(new_state, parent=node, action=(zero_i, zero_j)))
    
    return neighbors

def a_star(start_state, goal_state):
    start_node = PuzzleNode(start_state, heuristic=start_state)
    goal_node = PuzzleNode(goal_state)

    open_set = [start_node]
    closed_set = set()

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.state == goal_state:
            path = []
            while current_node:
                path.append(current_node.action)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(tuple(map(tuple, current_node.state)))

        for neighbor in get_neighbors(current_node):
            if tuple(map(tuple, neighbor.state)) not in closed_set:
                neighbor.cost = current_node.cost + 1
                neighbor.heuristic = heuristic(neighbor.state, goal_state)
                heapq.heappush(open_set, neighbor)

    return None

start_state = [
    [1, 2, 3],
    [4, 0, 5],
    [6, 7, 8]
]

goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

solution = a_star(start_state, goal_state)
print("Solution:", solution)
