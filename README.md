# A-Pathfinding-Visualizer
A presentation of the A* Pathfinding Algorithm using Python and the Pygame library.
The algorithm finds the shortest path between a start an and end point on the grid, using the heuristic value between the two points.
Works under the rule that diagonal paths do not exist in this grid. 
Adding diagonal functionality is possible and fairly simple (extend the "neighbor" definition to diagonal nodes as well), but since the code presents the algorithm
well enough already, I thought it would be unnecessary.

---------------------------------------------------------------------------------------------------------------------------------------------------------------
This project lacks a UI. 
To quickly begin, run the code in an interpreter and LEFT-CLICK on any 2 squarse on the grid.
Then create some barriers by DRAGGING THE MOUSE BUTTON over the white squares.
To initialize, press SPACE-BAR.
Then RESET by pressing / .

Controls are hence listed:
1. The FIRST LEFT-CLICK will produce the START position.
2. SECOND LEFT-CLICK will produce the END position.
3. ANY LEFT-CLICKS or DRAG hence-forth will produce BARRIERS.
4. To ERASE, RIGHT-CLICK or DRAG RIGHT-CLICK. 
5. To INITIALIZE ALGORITHM, press SPACEBAR.
6. To RESET BOARD, press the FORWARD-SLASH key (/).
