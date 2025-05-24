**The instructions Game of Life Project with P5 and OOP**

This project is an implementation of Conway’s Game of Life using Python, object-oriented programming, and P5 for graphical rendering.

**Step 1: Game of Life in P5 and OOP**

Objective: Implement the Game of Life using a graphical animation with the P5 library.

Requirements:

* The grid size and structure are customizable. You can choose how cells behave near the edges (classic border, toroidal wrapping, resizable window, etc.).
* Each cell is an instance of a class. The class constructor should store all the key information about the cell.

  * The cell class should provide methods to:

    * Access and modify attributes
    * Render the cell graphically
* The grid is also a class, responsible for handling interactions between cells:

  * Count live neighbors
  * Update the state of each cell per generation
  * Draw all the cells
  * Internally, the grid can be stored as a 2D list or a dictionary of cells
* The draw() function should be minimal, only responsible for computing and rendering the grid
* In this first step, the initial configuration of live cells is hardcoded — no graphical interface yet

Step 2: Competing Cell Populations

The Game of Life is now adapted to include two sets of cells, each with a different color (for example, red and blue).

Key questions:

* How do the survival rules adapt?

  * Do blue cells count red neighbors in their survival rules?
  * Or do they ignore them entirely?
* How do red cells evolve compared to blue ones?

Goal:
Explore and visualize how these two populations compete or coexist over time. You can freely choose the initial setup (randomized, teams placed face-to-face, etc.).

Step 3: Strategy Comparison

Introduce a menu or selection interface that allows the user to pick a strategy for each color (blue strategy, red strategy) before launching the simulation.

Bonus Ideas

You are encouraged to expand the project with any creative ideas you may have, such as:

* A menu to launch various Game of Life configurations
* The ability to manually place live cells using the mouse
* Visual or auditory enhancements
* Saving and loading configurations


 **Warning: The project doesn't work on Linux. If you encounter any bugs with the window scaling, please upgrade numpy and p5. The project was coded in Python 3.7.10.** 
