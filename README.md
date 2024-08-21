# Implement and Compare the Performances of Evolutionary Algorithms for Solving Combinatorial Optimization Problem 

The project implements four evolutionary algorithms to solve the n-queens problem. N-queens represent a combinatorial optimization problem where the goal is to place n number of queens on an n * n chessboard. An optimal solution to this problem is one where no queen is in a position to attack another. In opposition to other optimization problems, the n-queens problem proposes a single, optimal solution, meaning there is no need to look any further once a solution is found. As there is only a single objective, an optimal solution is found when it fulfils the constraints of that objective. <br />

The purpose of the project had two main aspects: implementation and analysis. Regarding implementation, the goal was to learn how to implement four different Evolutionary Algorithms (EAs) proposed during the course. The other aspect was the analysis of the obtained results. The analysis includes a study of the effects and correlations of different evolutionary operators and parameters used in each of our selected EAs. The proposed codebase works as a foundation for further discussion and elaboration, and during the report we aim to address the shortcomings and uncertainties and investigate opportunities and specific measures for improvement. <br />

## Installation 
The code can bee cloned from the GitLab repository or accessed using the submitted ZIP-file. The program requires some prerequisites upon execution, these dependencies include: numpy, pillow, matplotlib, and seaborn. <br />

Before execution, please conduct the following:  <br />
1. Install the dependices using the following commands:  

`pip install numpy` <br />
`pip install Pillow` <br />
`pip install matplotlib` <br />
`pip install seaborn` <br />

2. Make sure to navigate to the folder "evolutionary-ai". This is necessary in order to find the image used in the result screen. 

3. If desired, change the values of the evolutionary operators listed in the beginning of "main.py". 

4. When executing "main.py", a screen to set the board size (n) and inital position will apprear. Please set the desired size and position before pressing "Run".

5. Sit back and relax while the program does its thing :-) 

Once the program finishes, a graph showing the fitness scores in each generation and the average fitness throughout the run will appear. This window must be closed to see the result screen with the chessboard and a valid posistion of the n queens (if a valid solution was found). 
 
