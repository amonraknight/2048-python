2048 Python: computer play by itself
===========

This branch is based on the game from [yangshun/2048-python](https://github.com/yangshun/2048-python). Added a function to ask the computer to play by itself.  
The idea is to calculate the score of all the 4 actions in each situation and step to the direction rewards the most. The score of one action is the weighted sum of the scores of the following n steps. Monotonicity and merged cells are considered in scoring.
