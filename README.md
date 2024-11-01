
# Ball Physics Simulation for the Brachistochrone Curve Approximation

This project is a **Ball Physics Simulation** developed in **Python** using **Pygame**. It applies a **Genetic Algorithm (GA)** to approximate the **Brachistochrone Curve** — the path of fastest descent under gravity, which theoretically resembles a cycloid curve.

## Brachistochrone Problem

The **Brachistochrone Problem** is a fundamental question in physics and calculus of variations. It seeks to find the optimal curve, known as a cycloid, along which a particle under gravity will travel between two points in the shortest time possible. This project simulates an approximation of this path by evolving a terrain of blocks, adjusting heights to minimize the travel time of a rolling ball under gravity.

## Key Features

### Physics Simulation

This project uses a custom physics engine to simulate:

1. **Gravity and Freefall**: A downward force accelerates the ball, simulating real gravitational pull.
2. **Collisions with Blocks**: The ball interacts with terrain blocks. When the ball collides with a block, it reflects and bounces, mimicking real-life behavior.
3. **Horizontal and Vertical Velocities**: The ball’s velocities are affected by gravitational acceleration and collisions, making its descent trajectory realistically complex.

### Genetic Algorithm for Terrain Optimization

The core of this simulation is the genetic algorithm, which evolves terrain configurations to approximate the Brachistochrone Curve.

1. **Initialization**: A population of "terrain configurations" is created, each with a unique arrangement of block heights.
2. **Evaluation**: Each configuration is evaluated by how fast a simulated ball reaches the endpoint on that terrain. Configurations that bring the ball closer to the end in the shortest time are rated higher.
3. **Selection**: The top-performing configurations are selected to form the next generation.
4. **Mutation**: Random changes are applied to the terrain blocks to introduce variability, helping the algorithm avoid local optima.
5. **Next Generation**: The algorithm repeats this process over multiple generations to iteratively improve the terrain towards the shortest path.

### Smooth Terrain Rendering

The terrain is rendered as a smooth surface, which is essential for creating a continuous and realistic path for the ball. Each block in the configuration is drawn as part of a smooth polygonal surface. This representation helps the ball traverse the terrain naturally and allows for precise collision detection.

### Screenshots and Logging

- **Screenshots**: Each generation's terrain configuration is saved as an image in the `screenshots` directory. This allows for a visual review of the terrain evolution over generations.
- **Log File**: Every generation's performance is logged in a timestamped text file. The log includes color-coded progress updates, showing completed runs in green and unfinished runs in red.

## Code Structure and Classes

### `Block` Class

Represents a single terrain block in the simulation.

- **Attributes**: `x`, `y` coordinates, `width`, and `height`.
- **Method**: `draw(surface)`, which draws the block as a polygon on the screen.

### `Ball` Class

The `Ball` class simulates a ball object, including attributes and methods for handling physics.

- **Attributes**: `x`, `y` coordinates, radius, and vertical/horizontal velocities.
- **Methods**:
  - `update(blocks)`: Updates the ball's position based on gravitational acceleration and checks for collisions with blocks.
  - `draw(surface)`: Draws the ball on the screen.

### `Member` Class

Represents an individual in the genetic algorithm, holding a terrain configuration.

- **Attributes**: `block_heights` for the terrain, `fitness` to evaluate performance.
- **Methods**:
  - `generate_random_heights()`: Creates a random initial configuration.
  - `smooth_heights()`: Smooths terrain heights to produce a continuous descent.
  - `mutate()`: Applies mutations to create variation in block heights, simulating genetic mutation.

### Genetic Algorithm Workflow

The genetic algorithm runs across multiple generations, each seeking an optimal terrain:

1. **Simulation of Each Member**: Each member's configuration is evaluated by how efficiently a ball travels from the start to the goal.
2. **Fitness Calculation**: Completion time or progress distance is calculated and stored as fitness.
3. **Selection and Mutation**: Top performers are selected to form the next generation, with mutation applied to introduce variability.
4. **Generation Progression**: The loop continues for a specified number of generations, continually improving the population.

## Requirements

- `pygame`
- `colorama`

Install requirements with:

```bash
pip install pygame colorama
```

## Usage

1. Run the main script to start the simulation and observe the evolution of the terrain.
2. Check the `screenshots` directory for images of each generation’s configuration.
3. Review the log file for generation summaries, color-coded for completion status.

## Configuration Parameters

- **`NUM_BLOCKS`**: Number of blocks in the terrain.
- **`POPULATION_SIZE`**: Population size in the genetic algorithm.
- **`NUM_GENERATIONS`**: Total generations for evolution.
- **`MAX_SIMULATION_TIME`**: Max time allowed per simulation.
- **`MUTATION_RATE`**: Mutation rate for genetic variability.

## License

This project is licensed under the **Apache License 2.0**. See the LICENSE file for details.

---

This project is a hands-on simulation to understand the Brachistochrone problem and the application of genetic algorithms in terrain optimization for minimizing travel time.

For more information see: https://jacomoolman.co.za/brachistochrone/
