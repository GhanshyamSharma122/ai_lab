import math

# --- Game Board and Logic ---
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # Represents the 3x3 board
        self.current_winner = None  # Keeps track of the winner

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # 0 | 1 | 2
        # ---+---+---
        # 3 | 4 | 5
        # ---+---+---
        # 6 | 7 | 8
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, player):
        if self.board[square] == ' ':
            self.board[square] = player
            if self.check_winner(player):
                self.current_winner = player
            return True
        return False

    def check_winner(self, player):
        # Check rows
        for row in range(3):
            if all(s == player for s in self.board[row*3:(row+1)*3]):
                return True
        # Check columns
        for col in range(3):
            if all(s == player for s in [self.board[col+i*3] for i in range(3)]):
                return True
        # Check diagonals
        if all(s == player for s in [self.board[i] for i in [0, 4, 8]]):
            return True
        if all(s == player for s in [self.board[i] for i in [2, 4, 6]]):
            return True
        return False

# --- Minimax Algorithm ---
def minimax(state, player, tree_nodes, depth=0, parent_id=None, alpha=-math.inf, beta=math.inf):
    """
    Minimax with alpha-beta pruning.

    Args:
        state: TicTacToe board state
        player: current player ('X' or 'O')
        tree_nodes: list to record explored nodes for visualization
        depth: current depth in the tree
        parent_id: id of parent node in tree_nodes
        alpha: best already explored option along path to maximizer
        beta: best already explored option along path to minimizer

    Returns:
        dict with 'position' and 'score'
    """
    max_player = 'X'  # Our AI player
    other_player = 'O'  # Opponent of the AI (used for terminal scoring)

    # Terminal states
    if state.current_winner == max_player:
        return {'position': None, 'score': 1 * (state.num_empty_squares() + 1)}
    elif state.current_winner == other_player:
        return {'position': None, 'score': -1 * (state.num_empty_squares() + 1)}
    elif not state.empty_squares():
        return {'position': None, 'score': 0}

    # Initialize best
    if player == max_player:
        best = {'position': None, 'score': -math.inf}
    else:
        best = {'position': None, 'score': math.inf}

    current_node_id = len(tree_nodes)
    tree_nodes.append({'id': current_node_id, 'board': list(state.board), 'player': player, 'depth': depth, 'parent': parent_id, 'score': None})

    # Determine the next player
    next_player = other_player if player == max_player else max_player

    for possible_move in state.available_moves():
        # Simulate move
        new_state = TicTacToe()
        new_state.board = list(state.board)
        new_state.make_move(possible_move, player)

        # Recurse with alpha-beta
        sim_score = minimax(new_state, next_player, tree_nodes, depth + 1, current_node_id, alpha, beta)

        # Update best and alpha/beta
        if player == max_player:
            if sim_score['score'] > best['score']:
                best['score'] = sim_score['score']
                best['position'] = possible_move
            alpha = max(alpha, best['score'])
        else:
            if sim_score['score'] < best['score']:
                best['score'] = sim_score['score']
                best['position'] = possible_move
            beta = min(beta, best['score'])

        # Alpha-beta pruning
        if beta <= alpha:
            break

    # Update the score of the current node in the tree
    tree_nodes[current_node_id]['score'] = best['score']

    return best

# --- Game Play ---
def play_game(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'  # Starting player
    tree_nodes = [] # To store the game tree for visualization

    while game.empty_squares():
        if letter == 'O' and o_player == 'AI':
            square = minimax(game, letter, tree_nodes)['position']
        elif letter == 'X' and x_player == 'AI':
            square = minimax(game, letter, tree_nodes)['position']
        else:
            valid_move = False
            while not valid_move:
                try:
                    square = int(input(f"{letter}'s turn. Input move (0-8): "))
                    if square not in game.available_moves():
                        raise ValueError
                    valid_move = True
                except ValueError:
                    print("Invalid square. Try again.")

        if game.make_move(square, letter):
            if print_game:
                print(f"{letter} makes a move to square {square}")
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(f"{game.current_winner} wins!")
                return game.current_winner, tree_nodes
            
            letter = 'O' if letter == 'X' else 'X'  # Switch player

    if print_game:
        print("It's a tie!")
    return 'Tie', tree_nodes

# --- Tree Visualization (Simple Text-based) ---
def visualize_tree(tree_nodes):
    print("\n--- Game Tree Visualization ---")
    for node in tree_nodes:
        indent = "  " * node['depth']
        board_str = "".join(node['board'])
        parent_info = f" (Parent: {node['parent']})" if node['parent'] is not None else ""
        score_info = f" (Score: {node['score']})" if node['score'] is not None else ""
        print(f"{indent}Node {node['id']}{parent_info}: Player {node['player']} - Board: {board_str}{score_info}")

if __name__ == '__main__':
    game = TicTacToe()
    
    # Choose players: 'Human' or 'AI'
    x_player_type = 'Human'
    o_player_type = 'AI'

    winner, tree = play_game(game, x_player_type, o_player_type)
    
    # Visualize a portion of the generated game tree
    visualize_tree(tree[:50]) # Limiting to first 50 nodes for readability
