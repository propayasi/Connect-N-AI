import pygame
import numpy as np

# Constants
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)  # Define the radius

# Get grid size from the user
n = int(input("Enter the number of columns (n): "))
k = int(input("Enter the number of rows (k): "))
CONNECT_N = 4  # You can also allow the user to input this if desired

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Create the board
def create_board():
    return np.zeros((k, n))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[k-1][col] == 0

def get_next_open_row(board, col):
    for r in range(k):
        if board[r][col] == 0:
            return r

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(n - CONNECT_N + 1):
        for r in range(k):
            if all(board[r][c + i] == piece for i in range(CONNECT_N)):
                return True

    # Check vertical locations for win
    for c in range(n):
        for r in range(k - CONNECT_N + 1):
            if all(board[r + i][c] == piece for i in range(CONNECT_N)):
                return True

    # Check positively sloped diagonals
    for c in range(n - CONNECT_N + 1):
        for r in range(k - CONNECT_N + 1):
            if all(board[r + i][c + i] == piece for i in range(CONNECT_N)):
                return True

    # Check negatively sloped diagonals
    for c in range(n - CONNECT_N + 1):
        for r in range(CONNECT_N - 1, k):
            if all(board[r - i][c + i] == piece for i in range(CONNECT_N)):
                return True

def draw_board(board, screen):
    for c in range(n):
        for r in range(k):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(n):
        for r in range(k):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                font = pygame.font.SysFont("monospace", 30)
                label = font.render(player1_name, 1, BLACK)  # Use player 1 name
                screen.blit(label, (c * SQUARESIZE + 5, HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2) - 20))
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                font = pygame.font.SysFont("monospace", 30)
                label = font.render(player2_name, 1, BLACK)  # Use player 2 name
                screen.blit(label, (c * SQUARESIZE + 5, HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2) - 20))
    pygame.display.update()

# Initialize Pygame
pygame.init()
WIDTH = n * SQUARESIZE
HEIGHT = (k + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Connect-N')

# Get player names
player1_name = input("Enter Player 1 name (or press Enter for default 'PLAYER 1'): ") or "PLAYER 1"
player2_name = input("Enter Player 2 name (or press Enter for default 'PLAYER 2'): ") or "PLAYER 2"

game_over = False
turn = 0
board = create_board()
draw_board(board, screen)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
            # Player 1 Input
            if turn == 0:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        print(f"CONGRATULATIONS :) {player1_name} WINS!")
                        game_over = True

            # Player 2 Input
            else:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        print(f"CONGRATULATIONS :) {player2_name} WINS!")
                        game_over = True

            draw_board(board, screen)

            turn += 1
            turn = turn % 2

pygame.quit()


