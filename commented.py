import pygame
import random
import pygame.freetype  # Enhanced pygame module for loading and rendering computer fonts

# Initialize settings
grid_size = 8  # Default grid size for the game
difficulty = "0"  # Default difficulty level

# Difficulty selection and instructions
while difficulty != "1" and difficulty != "2" and difficulty != "3":
    difficulty = input("Please select a difficulty: type 1 for easy, 2 for medium, 3 for hard. Type 'i' for instructions: ")
    if difficulty not in ["1", "2", "3", "i"]:  # Check if the input is valid
        print("Please input a valid number!")
    if difficulty == "i":  # Display instructions if the user types "i"
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

# Adjust game settings based on difficulty
mine_count = 7  # Default mine count
if difficulty == "2":  # Medium difficulty
    grid_size = 16
    mine_count = 35
elif difficulty == "3":  # Hard difficulty
    grid_size = 25
    mine_count = 110

# Generate the game grid and place mines
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]  # Initialize grid with zeros
center_start = grid_size // 2 - 1  # Center exclusion zone start
center_end = grid_size // 2 + 1  # Center exclusion zone end

# Place mines randomly on the grid
while mine_count > 0:
    xrand = random.randint(0, grid_size - 1)  # Random x-coordinate
    yrand = random.randint(0, grid_size - 1)  # Random y-coordinate
    # Ensure the mine is not in the exclusion zone and not already a mine
    if grid[xrand][yrand] != "x" and not (center_start <= xrand <= center_end and center_start <= yrand <= center_end):
        grid[xrand][yrand] = "x"  # Place mine
        # Update numbers around the placed mine
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx, ny = xrand + dx, yrand + dy  # Neighboring cell coordinates
                if 0 <= nx < grid_size and 0 <= ny < grid_size and grid[nx][ny] != "x":  # Valid cell
                    grid[nx][ny] += 1  # Increment number
        mine_count -= 1  # Decrease mine count

# Initialize pygame
pygame.init()
cell_size = 25  # Size of each cell
screen = pygame.display.set_mode((grid_size * cell_size, grid_size * cell_size + 30))  # Screen size
pygame.display.set_caption("Minesweeper")
screen.fill((23, 158, 21))  # Background color
clock = pygame.time.Clock()
font = pygame.freetype.SysFont(None, 24)  # Font for rendering text

# Game states
revealed = [[False for _ in range(grid_size)] for _ in range(grid_size)]  # Track revealed cells
flags = [[False for _ in range(grid_size)] for _ in range(grid_size)]  # Track flagged cells
game_over = False  # Game over state
win = False  # Win state

# Function to draw the grid
def draw_grid():
    for i in range(grid_size):
        for j in range(grid_size):
            rect = pygame.Rect(i * cell_size, j * cell_size + 30, cell_size, cell_size)  # Cell rectangle

            if revealed[i][j]:  # If the cell is revealed
                if grid[i][j] == "x":  # Mine
                    pygame.draw.rect(screen, (255, 0, 0), rect)  # Red for mines
                else:  # Safe cell
                    pygame.draw.rect(screen, (200, 200, 200), rect)  # Light grey for revealed cells
                    if grid[i][j] > 0:  # Display the number if greater than 0
                        font.render_to(screen, (i * cell_size + 10, j * cell_size + 35), str(grid[i][j]), pygame.Color('black'))
            else:  # If the cell is not revealed
                if (i + j) % 2 == 0:  # Alternate colors for unrevealed cells
                    pygame.draw.rect(screen, (170, 215, 81), rect)  
                else:
                    pygame.draw.rect(screen, (162, 239, 73), rect)  

                if flags[i][j]:  # Display flag if flagged
                    font.render_to(screen, (i * cell_size + 10, j * cell_size + 35), "F", pygame.Color('red'))

            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Draw grid lines

# Function to draw the timer
def draw_timer():
    ticks = pygame.time.get_ticks()  # Get elapsed time in milliseconds
    seconds = int(ticks / 1000 % 60)  # Convert to seconds
    minutes = int(ticks / 60000 % 60)  # Convert to minutes
    time_string = f"{minutes:02d}:{seconds:02d}"  # Format time as MM:SS
    pygame.draw.rect(screen, (122, 61, 15), (0, 0, grid_size * cell_size, 30))  # Timer background
    font.render_to(screen, (10, 5), f"Time: {time_string}", pygame.Color('dodgerblue'))  # Render timer text

# Function to reveal a cell
def reveal_cell(x, y):
    if revealed[x][y] or flags[x][y]:  # If the cell is already revealed or flagged, do nothing
        return
    revealed[x][y] = True  # Mark the cell as revealed
    if grid[x][y] == 0:  # If the cell has no adjacent mines
        for dx in [-1, 0, 1]:  # Check all neighboring cells
            for dy in [-1, 0, 1]:
                nx, ny = x + dx, y + dy  # Neighboring cell coordinates
                if 0 <= nx < grid_size and 0 <= ny < grid_size:  # Ensure within bounds
                    reveal_cell(nx, ny)  # Recursively reveal neighboring cells

# Function to check if the player has won
def check_win():
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] != "x" and not revealed[i][j]:  # If there are unrevealed non-mine cells
                return False
    return True  # All safe cells are revealed

# Main game loop
running = True
while running:
    screen.fill((23, 158, 21))  # Clear the screen
    draw_grid()  # Draw the grid
    draw_timer()  # Draw the timer

    if game_over:  # Display "Lost" if the game is over
        font.render_to(screen, (10, grid_size * cell_size + 5), "Lost", pygame.Color('red'))
        for i in range(grid_size):
            for j in range(grid_size):
                if not revealed[i][j]:
                    reveal_cell(i, j) # Reveal all unrevealed grids
    elif win:  # Display "Won" if the player has won
        font.render_to(screen, (10, grid_size * cell_size + 5), "Won", pygame.Color('red'))

    for event in pygame.event.get():  # Process events
        if event.type == pygame.QUIT:  # Quit the game
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and not win:  # Handle mouse clicks
            pos = pygame.mouse.get_pos()  # Get mouse position
            x, y = pos[0] // cell_size, (pos[1] - 30) // cell_size  # Convert to grid coordinates
            if 0 <= x < grid_size and 0 <= y < grid_size:  # Ensure within bounds
                if event.button == 1:  # Left click
                    if grid[x][y] == "x":  # Clicked on a mine
                        game_over = True
                        revealed[x][y] = True  # Reveal the mine
                    else:  # Clicked on a safe cell
                        reveal_cell(x, y)  # Reveal the cell
                        if check_win():  # Check if the player has won
                            win = True
                elif event.button == 3:  # Right click
                    flags[x][y] = not flags[x][y]  # Toggle flag
    pygame.display.flip()  # Update the display
    clock.tick(60)  # Limit frame rate to 60 FPS

pygame.quit()  # Quit pygame