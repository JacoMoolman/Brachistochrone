import pygame
import sys
import random
from colorama import init, Fore
from pathlib import Path
import math
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 1500
HEIGHT = 600
FPS = 200
GRAVITY = 0.8
BOUNCE_FACTOR = 0.5
NUM_BLOCKS = 200  # Controls number of steps in the staircase
STAIRCASE_START_X = 50  # Where stairs begin from left
STAIRCASE_END_GAP = 150  # Space for final block and gap
USABLE_WIDTH = WIDTH - STAIRCASE_START_X - STAIRCASE_END_GAP  # Available width for stairs
step_width = USABLE_WIDTH / NUM_BLOCKS  # Dynamically calculate step width
max_height = 500  # Maximum height for the tallest block
BALL_START_X = 100
BALL_START_Y = 50
TIMER_STARTED = False
start_time = 0
end_time = 0
runtime_start = pygame.time.get_ticks()  # Start time for general runtime
POPULATION_SIZE = 200
NUM_GENERATIONS = 1000
MAX_SIMULATION_TIME = 1500 #Milliseconds
NUM_SURVIVORS = 50
MUTATION_RATE = 0.05  # 10% chance of mutation per block
INITIAL_GOAL_HEIGHT = 300  # Starting goal height
current_goal_height = INITIAL_GOAL_HEIGHT

# Colors
WHITE = (255, 255, 255)
RED = Fore.RED
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = Fore.GREEN
RESET = Fore.RESET  # Reset color back to default

# Enable Windows ANSI support (make sure this is at the start of your script)
import os
os.system('')  # Enable Windows ANSI support

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Physics Simulation")
clock = pygame.time.Clock()

# Color constants for pygame drawing
BALL_COLOR = (255, 0, 0)  # Red color for the ball
BLOCK_COLOR = (0, 0, 255)  # Blue color for blocks

# ANSI color codes for terminal output
TERM_RED = '\x1b[31m'
TERM_GREEN = '\x1b[32m'
TERM_RESET = '\x1b[0m'

# Create screenshots directory if it doesn't exist
Path("screenshots").mkdir(exist_ok=True)
screenshot_counter = 0  # Global counter for screenshots

# Add after other constants
LOG_FILE = f"simulation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# Create a custom print function that writes to both console and file
def log_print(*args, **kwargs):
    # Print to console
    print(*args, **kwargs)
    
    # Write to file
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        # Convert ANSI color codes to plain text for file
        text = ' '.join(map(str, args))
        text = text.replace(TERM_RED, '[RED]')\
                  .replace(TERM_GREEN, '[GREEN]')\
                  .replace(TERM_RESET, '[/]')
        f.write(text + '\n')

class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Create points for the polygon
        self.points = [(x, HEIGHT), (x, y), (x + width, y), (x + width, HEIGHT)]
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, surface):
        pygame.draw.polygon(surface, BLOCK_COLOR, self.points)

class Ball:
    def __init__(self):
        self.radius = 20
        self.x = BALL_START_X
        self.y = BALL_START_Y
        self.vel_y = 0
        self.vel_x = 0
        
    def update(self, blocks):
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Ground collision
        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vel_y *= -BOUNCE_FACTOR
        
        # Block collisions
        for block in blocks:
            # Find closest point on block to circle center
            closest_x = max(block.rect.left, min(self.x, block.rect.right))
            closest_y = max(block.rect.top, min(self.y, block.rect.bottom))
            
            # Calculate distance between closest point and circle center
            distance_x = self.x - closest_x
            distance_y = self.y - closest_y
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
            
            # Check for collision
            if distance < self.radius:
                # Calculate collision normal
                if distance > 0:
                    normal_x = distance_x / distance
                    normal_y = distance_y / distance
                else:
                    normal_x = 0
                    normal_y = -1
                
                # Move circle out of collision
                overlap = self.radius - distance
                self.x += normal_x * overlap
                self.y += normal_y * overlap
                
                # Calculate velocity reflection
                dot_product = (self.vel_x * normal_x + self.vel_y * normal_y)
                self.vel_x = -2 * dot_product * normal_x * BOUNCE_FACTOR + self.vel_x
                self.vel_y = -2 * dot_product * normal_y * BOUNCE_FACTOR + self.vel_y
    
    def draw(self, surface):
        pygame.draw.circle(surface, BALL_COLOR, (int(self.x), int(self.y)), self.radius)

# Create ball instance
ball = Ball()

class Member:
    def __init__(self, block_heights=None):
        self.block_heights = block_heights or self.generate_random_heights()
        self.smooth_heights()  # Apply smoothing after generating heights
        self.fitness = (float('inf'), 0)
        
    def generate_random_heights(self):
        heights = []
        current_height = max_height
        for i in range(NUM_BLOCKS):
            if i == 0:
                current_height = max_height * (NUM_BLOCKS - i) / NUM_BLOCKS  # Fixed height for first block
            else:
                random_change = random.uniform(-20, 20)
                current_height = max(50, min(current_height + random_change, max_height))
            heights.append(current_height)
        return heights
    
    def smooth_heights(self, window_size=10):
        smoothed = self.block_heights.copy()
        first_height = smoothed[0]  # Save the first height
        half_window = window_size // 2
        transition_length = 40  # Longer transition zone for the end
        
        # Smooth all heights including transitions at both ends
        for i in range(len(self.block_heights)):
            if i == 0:
                continue  # Skip the first block
            elif i < window_size:  # Create gradual transition from start
                # Weighted average: more weight to first_height for blocks closer to start
                weight = (window_size - i) / window_size
                start = max(0, i - half_window)
                end = min(len(self.block_heights), i + half_window + 1)
                window = self.block_heights[start:end]
                avg_height = sum(window) / len(window)
                smoothed[i] = (weight * first_height) + ((1 - weight) * avg_height)
            elif i > len(self.block_heights) - transition_length:  # Create gradual transition to ground
                # Use cosine interpolation for smoother transition
                progress = (i - (len(self.block_heights) - transition_length)) / transition_length
                weight = (1 + math.cos(progress * math.pi)) / 2  # Cosine interpolation
                start = max(0, i - half_window)
                end = min(len(self.block_heights), i + half_window + 1)
                window = self.block_heights[start:end]
                avg_height = sum(window) / len(window)
                smoothed[i] = avg_height * weight
            else:  # Normal smoothing for the middle section
                start = max(0, i - half_window)
                end = min(len(self.block_heights), i + half_window + 1)
                window = self.block_heights[start:end]
                smoothed[i] = sum(window) / len(window)
        
        self.block_heights = smoothed
    
    def mutate(self):
        for i in range(len(self.block_heights)):
            if random.random() < MUTATION_RATE:
                random_change = random.uniform(-50, 50)
                current_height = self.block_heights[i] + random_change
                self.block_heights[i] = max(50, min(current_height, max_height))
        self.smooth_heights()  # Smooth after mutation

# Add this function before the run_simulation function
def draw_smooth_surface(surface, blocks):
    # Create a list of points for the smooth surface
    points = [(STAIRCASE_START_X, HEIGHT)]  # Start at bottom left
    
    # Add points for each block's top edge (excluding the final goal block)
    for block in blocks[:-1]:  # Note the [:-1] to exclude the last block
        points.append((block.x, block.y))
    
    # Add the last point straight down to the ground from the last regular block
    last_block = blocks[-2]  # Get the last regular block (not the goal)
    points.append((last_block.x + last_block.width, last_block.y))
    points.append((last_block.x + last_block.width, HEIGHT))
    
    # Draw the filled polygon for the main surface
    pygame.draw.polygon(surface, BLOCK_COLOR, points)
    
    # Draw the goal block separately
    goal_block = blocks[-1]
    goal_points = [
        (goal_block.x, goal_block.y),
        (goal_block.x + goal_block.width, goal_block.y),
        (goal_block.x + goal_block.width, HEIGHT),
        (goal_block.x, HEIGHT)
    ]
    pygame.draw.polygon(surface, BLOCK_COLOR, goal_points)

def run_simulation(member):
    global screenshot_counter  # Use global counter
    
    # Reset simulation
    ball = Ball()
    start_time = pygame.time.get_ticks()
    simulation_start = pygame.time.get_ticks()
    max_x_reached = BALL_START_X
    
    # Create blocks using member's heights
    blocks = []
    for i in range(NUM_BLOCKS):
        blocks.append(Block(
            STAIRCASE_START_X + (i * step_width),
            HEIGHT - member.block_heights[i],
            step_width + 1,
            member.block_heights[i]
        ))
    
    # Add final block
    final_x = STAIRCASE_START_X + (NUM_BLOCKS * step_width) + 100
    blocks.append(Block(
        final_x,
        HEIGHT - current_goal_height,
        step_width,
        current_goal_height
    ))
    
    # Draw initial state and take screenshot
    screen.fill(BLACK)
    draw_smooth_surface(screen, blocks)
    ball.draw(screen)
    pygame.display.flip()
    
    # Save screenshot
    pygame.image.save(screen, f"screenshots/simulation_{screenshot_counter}.png")
    screenshot_counter += 1
    
    while True:
        current_time = pygame.time.get_ticks()
        
        # Update ball
        ball.update(blocks)
        max_x_reached = max(max_x_reached, ball.x)
        
        # Check if ball touches the goal block (which is the last block)
        goal_block = blocks[-1]
        distance_x = max(goal_block.rect.left, min(ball.x, goal_block.rect.right)) - ball.x
        distance_y = max(goal_block.rect.top, min(ball.y, goal_block.rect.bottom)) - ball.y
        distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        
        if distance <= ball.radius:  # Ball is touching the goal block
            completion_time = (current_time - start_time) / 1000
            return (completion_time, 1.0)
            
        # Check for timeout
        if current_time - simulation_start > MAX_SIMULATION_TIME:
            progress = (max_x_reached - BALL_START_X) / (final_x - BALL_START_X)
            return (float('inf'), progress)
        
        # Draw
        screen.fill(BLACK)
        draw_smooth_surface(screen, blocks)
        ball.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def create_next_generation(population):
    # Sort by fitness - prioritizing completion time over progress
    population.sort(key=lambda x: (
        0 if x.fitness[0] != float('inf') else 1,  # Completed runs first
        x.fitness[0],                              # Then by time
        -x.fitness[1]                              # Then by progress
    ))
    
    # Keep top performers
    survivors = population[:NUM_SURVIVORS]
    
    # Create new population
    new_population = []
    while len(new_population) < POPULATION_SIZE:
        parent = random.choice(survivors)
        child = Member(block_heights=parent.block_heights.copy())
        child.fitness = parent.fitness
        child.mutate()
        new_population.append(child)
    
    return new_population

# Main genetic algorithm loop
population = [Member() for _ in range(POPULATION_SIZE)]

for generation in range(NUM_GENERATIONS):
    # Update goal height
    current_goal_height = max(50, INITIAL_GOAL_HEIGHT - generation)  # Don't let it go below 50
    log_print(f"\nGeneration {generation + 1} - Goal Height: {current_goal_height}")
    
    # Evaluate each member
    for i, member in enumerate(population):
        completion_time, progress = run_simulation(member)
        member.fitness = (completion_time, progress)
        
        # # Debug print right after assignment
        # print(f"DEBUG - Just set member {i+1} fitness to: {member.fitness}")
        
        if completion_time != float('inf'):
            # Completed - show in GREEN
            log_print(f"{TERM_GREEN}Testing member {i + 1}/{POPULATION_SIZE}: Completed in: {completion_time:.2f}s{TERM_RESET}")
        else:
            # Did not complete - show in RED
            log_print(f"{TERM_RED}Testing member {i + 1}/{POPULATION_SIZE}: Did not complete. Progress: {progress*100:.1f}%{TERM_RESET}")
    
    # Create next generation
    population = create_next_generation(population)
    
    # At the end of each generation
    # Find best member and PRINT THE ACTUAL VALUES FOR DEBUGGING
    best_member = min(population, key=lambda x: x.fitness[0])
    
    log_print("\nDEBUG - All completion times:")
    for member in population:
        log_print(f"Member fitness: {member.fitness}")
    log_print(f"Best member fitness: {best_member.fitness}")
    
    # Print best result
    if best_member.fitness[0] != float('inf'):
        log_print(f"{TERM_GREEN}Best time this generation: {best_member.fitness[0]:.2f}s{TERM_RESET}")
    else:
        log_print(f"{TERM_RED}Best this generation: {best_member.fitness[1]*100:.1f}% progress{TERM_RESET}")

# Final results
best_member = min(population, key=lambda x: (x.fitness[0], -x.fitness[1]))
log_print(f"\nBest overall time: {best_member.fitness[0]:.2f}s")

# Create blocks using best member's heights
blocks = []
for i in range(NUM_BLOCKS):
    blocks.append(Block(
        STAIRCASE_START_X + (i * step_width),
        HEIGHT - best_member.block_heights[i],
        step_width + 1,
        best_member.block_heights[i]
    ))

# Add final block
blocks.append(Block(
    STAIRCASE_START_X + (NUM_BLOCKS * step_width) + 100,
    HEIGHT - current_goal_height,
    step_width,
    current_goal_height
))

# Reset ball
ball = Ball()

# Game loop to show final result
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Update
    ball.update(blocks)
    
    # Draw
    screen.fill(BLACK)
    draw_smooth_surface(screen, blocks)
    ball.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)
