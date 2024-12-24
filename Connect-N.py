import pygame
import numpy as np
import random
import math
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
FONT_SIZE = 20
while True:
    try:
        n = int(input("Enter the number of columns: "))
        if n <= 0:
            print("Please enter a positive integer for the number of columns.")
            continue
        break
    except ValueError:
        print("Please enter correctly. The number of columns must be an integer.")
while True:
    try:
        k = int(input("Enter the number of rows: "))
        if k <= 0:
            print("Please enter a positive integer for the number of rows.")
            continue
        break
    except ValueError:
        print("Please enter correctly. The number of rows must be an integer.")
while True:
    CONNECT_N = int(input("Enter the winning condition (3 or more): "))
    if CONNECT_N >= 3:
        break
    print("Invalid input. Please choose a number greater than or equal to 3.")
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
def create_board():
    return np.zeros((k, n))
def drop_piece(board, row, col, piece):
    board[row][col] = piece
def is_valid_location(board, col):
    return board[k - 1][col] == 0
def get_next_open_row(board, col):
    for r in range(k):
        if board[r][col] == 0:
            return r
def winning_move(board, piece):
    winning_positions = []
    for c in range(n - CONNECT_N + 1):
        for r in range(k):
            if all(board[r][c + i] == piece for i in range(CONNECT_N)):
                winning_positions = [(r, c + i) for i in range(CONNECT_N)]
                return True, winning_positions
    for c in range(n):
        for r in range(k - CONNECT_N + 1):
            if all(board[r + i][c] == piece for i in range(CONNECT_N)):
                winning_positions = [(r + i, c) for i in range(CONNECT_N)]
                return True, winning_positions
    for c in range(n - CONNECT_N + 1):
        for r in range(k - CONNECT_N + 1):
            if all(board[r + i][c + i] == piece for i in range(CONNECT_N)):
                winning_positions = [(r + i, c + i) for i in range(CONNECT_N)]
                return True, winning_positions
    for c in range(n - CONNECT_N + 1):
        for r in range(CONNECT_N - 1, k):
            if all(board[r - i][c + i] == piece for i in range(CONNECT_N)):
                winning_positions = [(r - i, c + i) for i in range(CONNECT_N)]
                return True, winning_positions
    return False, []
def draw_board(board, screen, hovering_col, font, player_names, winning_positions=None):
    screen.fill(BLACK)
    for c in range(n):
        for r in range(k):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    if winning_positions is None:
        winning_positions = []
    for c in range(n):
        for r in range(k):
            if board[r][c] == 1:
                color = RED
                player_name = player_names[0]
            elif board[r][c] == 2:
                color = YELLOW
                player_name = player_names[1]
            else:
                continue
            if (r, c) in winning_positions:
                color = GREEN
            pygame.draw.circle(screen, color, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            text = font.render(player_name, True, BLACK)
            screen.blit(text, (int(c * SQUARESIZE + SQUARESIZE / 2 - text.get_width() / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2) - text.get_height() / 2))
    if hovering_col is not None:
        color = RED if turn == 0 else YELLOW
        pygame.draw.circle(screen, color, (int(hovering_col * SQUARESIZE + SQUARESIZE / 2), int(SQUARESIZE / 2)), RADIUS)
        text = font.render(player_names[turn], True, BLACK)
        screen.blit(text, (int(hovering_col * SQUARESIZE + SQUARESIZE / 2 - text.get_width() / 2), SQUARESIZE / 2 - 10))
    pygame.display.update()
def minimax(board, depth, alpha, beta, maximizing_player):
    valid_locations = [c for c in range(n) if is_valid_location(board, c)]
    if depth == 0 or len(valid_locations) == 0:
        return evaluate_board(board), None
    best_col = random.choice(valid_locations)
    if maximizing_player:
        value = -math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, 2) 
            new_score, _ = minimax(board_copy, depth - 1, alpha, beta, False)
            if new_score > value:
                value = new_score
                best_col = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value, best_col
    else:
        value = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            board_copy = board.copy()
            drop_piece(board_copy, row, col, 1)
            new_score, _ = minimax(board_copy, depth - 1, alpha, beta, True)
            if new_score < value:
                value = new_score
                best_col = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value, best_col
def evaluate_board(board):
    score = 0
    for r in range(k):
        for c in range(n - CONNECT_N + 1):
            window = board[r][c:c + CONNECT_N]
            score += evaluate_window(window, 1)  
            score -= evaluate_window(window, 2)  
    for c in range(n):
        for r in range(k - CONNECT_N + 1):
            window = board[r:r + CONNECT_N, c]
            score += evaluate_window(window, 1) 
            score -= evaluate_window(window, 2)
    for r in range(k - CONNECT_N + 1):
        for c in range(n - CONNECT_N + 1):
            window = [board[r + i][c + i] for i in range(CONNECT_N)]
            score += evaluate_window(window, 1) 
            score -= evaluate_window(window, 2) 
    for r in range(CONNECT_N - 1, k):
        for c in range(n - CONNECT_N + 1):
            window = [board[r - i][c + i] for i in range(CONNECT_N)]
            score += evaluate_window(window, 1) 
            score -= evaluate_window(window, 2) 
    center_col = n // 2
    for r in range(k):
        if board[r][center_col] == 1:
            score += 3  
        elif board[r][center_col] == 2:
            score -= 3
    return score
def evaluate_window(window, piece):
    score = 0
    opponent = 2 if piece == 1 else 1
    window = np.array(window)
    piece_count = np.count_nonzero(window == piece)
    empty_count = np.count_nonzero(window == 0)
    opponent_count = np.count_nonzero(window == opponent)
    if piece_count == CONNECT_N:
        score += 100
    elif piece_count == CONNECT_N - 1 and empty_count == 1:
        score += 10
    elif piece_count == CONNECT_N - 2 and empty_count == 2:
        score += 5
    if opponent_count == CONNECT_N - 1 and empty_count == 1:
        score -= 50
    if opponent_count == CONNECT_N - 2 and empty_count == 2:
        score -= 10
    return score
def is_board_full(board):
    for r in range(k):
        for c in range(n):
            if board[r][c] == 0:
                return False
    return True
while True:
    try:
        mode = int(input("Choose Game Mode:\n1. Player vs Player\n2. Player vs Computer\nEnter your choice (1/2): "))
        if mode in [1, 2]:
            break
        else:
            print("Please select correctly.")
    except ValueError:
        print("Please select correctly.")
if mode == 1:
    player1_name = input("Enter Player 1's name: ")
    player2_name = input("Enter Player 2's name: ")
    player_names = [player1_name, player2_name]
    difficulty = None
elif mode == 2:
    player_name = input("Enter Player's name: ")
    player_names = [player_name, "Computer"]
    while True:
        try:
            print("Choose Difficulty:")
            print("1. Easy")
            print("2. Medium")
            print("3. Hard")
            difficulty = int(input("Enter your choice (1/2/3): "))
            if difficulty not in [1, 2, 3]:
                print("Please select correctly.")
                continue
            break
        except ValueError:
            print("Please select correctly.")
pygame.init()
WIDTH = n * SQUARESIZE
HEIGHT = (k + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Connect-N')
font = pygame.font.SysFont("monospace", FONT_SIZE)
game_over = False
turn = 0
board = create_board()
hovering_col = None
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.MOUSEMOTION:
            x_pos = event.pos[0]
            hovering_col = int(math.floor(x_pos / SQUARESIZE))
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if is_valid_location(board, hovering_col):
                row = get_next_open_row(board, hovering_col)
                drop_piece(board, row, hovering_col, 1 if turn == 0 else 2)
                win, winning_positions = winning_move(board, 1 if turn == 0 else 2)
                if win:
                    draw_board(board, screen, hovering_col, font, player_names, winning_positions)
                    pygame.display.update()
                    pygame.time.wait(2000)
                    game_over = True
                elif np.all(board != 0):  
                    draw_board(board, screen, hovering_col, font, player_names)
                    pygame.display.update()
                    pygame.time.wait(2000)
                    game_over = True
                turn = (turn + 1) % 2
    if mode == 2 and turn == 1 and not game_over:
        valid_locations = [c for c in range(n) if is_valid_location(board, c)]
        if difficulty == 1:
            col = random.choice(valid_locations)
        elif difficulty == 2: 
            _, col = minimax(board, 3, -math.inf, math.inf, True)
        elif difficulty == 3:  
            _, col = minimax(board, 7, -math.inf, math.inf, True)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, 2)
        win, winning_positions = winning_move(board, 2)
        if win:
            draw_board(board, screen, hovering_col, font, player_names, winning_positions)
            pygame.display.update()
            pygame.time.wait(2000)
            game_over = True
        elif np.all(board != 0):
            draw_board(board, screen, hovering_col, font, player_names)
            pygame.display.update()
            pygame.time.wait(2000)  
            game_over = True
        turn = 0
    if not game_over:
        draw_board(board, screen, hovering_col, font, player_names)
pygame.time.wait(2000)
pygame.quit()
