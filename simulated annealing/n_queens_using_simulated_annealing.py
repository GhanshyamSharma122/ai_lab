import random
import math

def calculate_conflicts(board):
    """Calculates the number of conflicts (attacking pairs of queens) on the board."""
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Check for same row (not possible with current representation)
            # Check for same column
            if board[i] == board[j]:
                conflicts += 1
            # Check for diagonals
            if abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_random_neighbor(board):
    """Generates a random neighbor state by moving one queen to a different row within its column."""
    n = len(board)
    neighbor = list(board)  # Create a copy to avoid modifying the original
    col_to_move = random.randint(0, n - 1)
    new_row = random.randint(0, n - 1)
    while new_row == neighbor[col_to_move]:  # Ensure the queen actually moves
        new_row = random.randint(0, n - 1)
    neighbor[col_to_move] = new_row
    return neighbor

def simulated_annealing_n_queens(n, initial_temperature=1000, cooling_rate=0.99, min_temperature=1):
    """Solves the N-Queens problem using Simulated Annealing."""
    # Initial state: queens placed randomly in each column
    current_board = [random.randint(0, n - 1) for _ in range(n)]
    current_conflicts = calculate_conflicts(current_board)
    
    best_board = list(current_board)
    best_conflicts = current_conflicts

    temperature = initial_temperature

    while temperature > min_temperature and best_conflicts > 0:
        neighbor_board = get_random_neighbor(current_board)
        neighbor_conflicts = calculate_conflicts(neighbor_board)

        delta_e = neighbor_conflicts - current_conflicts

        if delta_e < 0:  # If neighbor is better, accept it
            current_board = neighbor_board
            current_conflicts = neighbor_conflicts
            if current_conflicts < best_conflicts:
                best_conflicts = current_conflicts
                best_board = list(current_board)
        else:  # If neighbor is worse, accept with a probability
            probability = math.exp(-delta_e / temperature)
            if random.random() < probability:
                current_board = neighbor_board
                current_conflicts = neighbor_conflicts
        
        temperature *= cooling_rate

    return best_board, best_conflicts

# Example usage:
if __name__ == "__main__":
    n_queens = 4  # Number of queens (and board size)
    solution_board, conflicts = simulated_annealing_n_queens(n_queens)

    print(f"N-Queens problem for N={n_queens}")
    if conflicts == 0:
        print("Solution found:")
        for row in solution_board:
            print(" ".join(["Q" if i == row else "." for i in range(n_queens)]))
    else:
        print(f"Could not find a perfect solution. Best found has {conflicts} conflicts.")
        for row in solution_board:
            print(" ".join(["Q" if i == row else "." for i in range(n_queens)]))
