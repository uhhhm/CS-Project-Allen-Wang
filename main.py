import pygame
import random
import pygame.freetype # Enhanced pygame module for loading and rendering computer fonts

# Initialize settings
grid_size = 8
difficulty = "0"  # Set default difficulty

# Difficulty selection and instructions
while difficulty != "1" and difficulty != "2" and difficulty != "3":
    difficulty = input("Please select a difficulty: type 1 for easy, 2 for medium, 3 for hard. Type 'i' for instructions: ")
    if difficulty not in ["1", "2", "3", "i"]:
        print("Please input a valid number!")
    if difficulty == "i":
        print("""
How to play Minesweeper:
    
Minesweeper is a game where mines are hidden in a grid of squares. Safe squares have numbers 
telling you how many mines touch the square. You can use the number clues to solve the game 
by opening all of the safe squares. If you click on a mine you lose the game!

You open squares with the left mouse button and put flags on mines with the right mouse button. 
Pressing the right mouse button again changes your flag into a question mark. When you open a square 
that does not touch any mines, it will be empty and the adjacent squares will automatically open 
in all directions until reaching squares that contain numbers.

Good luck and have fun!
        """)

# Difficulty settings, changing mine count and grid size
mine_count = 7
if difficulty == "2":
    grid_size = 16
    mine_count = 30
elif difficulty == "3":
    grid_size = 25
    mine_count = 70

# Generate grid and mines
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)] 
center_start = grid_size // 2 - 1 # Generate center for omission zone
center_end = grid_size // 2 + 1
while mine_count > 0:
    xrand = random.randint(0, grid_size - 1)
    yrand = random.randint(0, grid_size - 1)
    if grid[xrand][yrand] != "x" and not (center_start <= xrand <= center_end and center_start <= yrand <= center_end): # If statement, code below is skipped if mine is in center omission zone or already on a mine
        grid[xrand][yrand] = "x"
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = xrand + dx, yrand + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[nx][ny] != "x":
                    grid[nx][ny] += 1
        mine_count -= 1

# Initialize pygame
pygame.init()
cell_size = 25  
screen = pygame.display.set_mode((grid_size * cell_size, grid_size * cell_size + 30))
pygame.display.set_caption("Minesweeper")
screen.fill((23, 158, 21))  
clock = pygame.time.Clock()
font = pygame.freetype.SysFont(None, 24)

# Game states
revealed = [[False for _ in range(grid_size)] for _ in range(grid_size)]
flags = [[False for _ in range(grid_size)] for _ in range(grid_size)]
game_over = False
win = False

def draw_grid(): # Updates screen and draws the grid in the game loop
    for i in range(grid_size):
        for j in range(grid_size):
            rect = pygame.Rect(i * cell_size, j * cell_size + 30, cell_size, cell_size)
            
            if revealed[i][j]:
                if grid[i][j] == "x":
                    pygame.draw.rect(screen, (255, 0, 0), rect)  # Red for mines
                else:
                    pygame.draw.rect(screen, (200, 200, 200), rect)  # Light grey for revealed cells
                    if grid[i][j] > 0:
                        font.render_to(screen, (i * cell_size + 10, j * cell_size + 35), str(grid[i][j]), pygame.Color('black'))
            else:
                if (i + j) % 2 == 0:
                    pygame.draw.rect(screen, (170, 215, 81), rect)  
                else:
                    pygame.draw.rect(screen, (162, 239, 73), rect)  

                if flags[i][j]:
                    font.render_to(screen, (i * cell_size + 10, j * cell_size + 35), "F", pygame.Color('red'))

            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Grid lines

def draw_timer(): #Timer that is rendered as a clock, called upon in the game loop
    ticks = pygame.time.get_ticks()
    seconds = int(ticks / 1000 % 60)
    minutes = int(ticks / 60000 % 60)
    time_string = f"{minutes:02d}:{seconds:02d}"
    pygame.draw.rect(screen, (122, 61, 15), (0, 0, grid_size * cell_size, 30))  
    font.render_to(screen, (10, 5), f"Time: {time_string}", pygame.Color('dodgerblue'))

def reveal_cell(x, y):
    if revealed[x][y] or flags[x][y]:
        return
    revealed[x][y] = True
    if grid[x][y] == 0:
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < grid_size and 0 <= ny < grid_size:
                    reveal_cell(nx, ny)

def check_win():
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] != "x" and not revealed[i][j]:
                return False
    return True

running = True
while running:
    screen.fill((23, 158, 21))
    draw_grid()
    draw_timer()

    if game_over:
        font.render_to(screen, (10, grid_size * cell_size + 5), "Lost", pygame.Color('red'))
    elif win:
        font.render_to(screen, (10, grid_size * cell_size + 5), "Won", pygame.Color('red'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not win:  
            pos = pygame.mouse.get_pos()
            x, y = pos[0] // cell_size, (pos[1] - 30) // cell_size
            if 0 <= x < grid_size and 0 <= y < grid_size:
                if event.button == 1:  # Left click
                    if grid[x][y] == "x":
                        game_over = True
                        revealed[x][y] = True
                    else:
                        reveal_cell(x, y)
                        if check_win():
                            win = True
                elif event.button == 3:  # Right click
                    flags[x][y] = not flags[x][y]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()