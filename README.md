
# Ball Physics Simulation with Genetic Algorithm for Terrain Optimization

This project is a **Ball Physics Simulation** developed using **Pygame** and **Python**. The simulation utilizes a **Genetic Algorithm** (GA) to evolve and optimize a terrain (staircase-like block structure) such that a ball reaches a specified goal point.

## Features

1. **Physics Simulation**: Realistic ball physics with gravity and bounce mechanics.
2. **Terrain Optimization**: Genetic Algorithm used to adjust terrain for optimized ball travel.
3. **Smooth Surface Drawing**: Terrain surface is rendered with smooth polygon edges.
4. **Logging and Visual Output**: Each simulation generation and member progress is logged to a text file and displayed in the console with color-coded outputs.

## Requirements

To run the simulation, you need the following Python libraries:

- `pygame`
- `colorama`

You can install the required libraries via pip:

```bash
pip install pygame colorama
```

## Usage

1. **Run the Simulation**: Launch the main script to start the genetic algorithm simulation. Each generation will attempt to find a better terrain configuration.
2. **View Results**: Each generation's performance is logged with color coding, showing completed runs in green and failed attempts in red.
3. **Screenshots**: Screenshots of each generation’s terrain configuration are saved to the `screenshots` directory.
4. **Final Visualization**: After all generations, the best member's terrain is displayed for visualization.

## Configuration Parameters

Some of the main adjustable parameters are:

- `NUM_BLOCKS`: Number of blocks in the staircase.
- `POPULATION_SIZE`: Size of the population in the genetic algorithm.
- `NUM_GENERATIONS`: Total number of generations for evolution.
- `MAX_SIMULATION_TIME`: Maximum time allowed per simulation.
- `MUTATION_RATE`: Mutation rate applied to block heights for evolution.

## File Structure

- `simulation_log_<timestamp>.txt`: Log file containing generation results.
- `screenshots/`: Directory where screenshots of each generation are saved.

## Code Overview

### Block Class

Represents a block in the terrain. Each block is created with `x`, `y` coordinates, width, and height.

### Ball Class

Handles the physics of the ball, including gravity, bounce, and collision detection.

### Member Class

Represents an individual in the genetic algorithm, including generation, smoothing, and mutation of block heights.

### Genetic Algorithm

Implements the evolution process: selection of top performers, reproduction, and mutation to create a new population in each generation.

### Main Loop

Runs the simulation across multiple generations, logging progress and capturing the final optimized terrain.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

This simulation is both an educational tool for understanding genetic algorithms and an interactive demonstration of physics and terrain optimization.
