# GeneticAlgoritm
Solution to find most optimal buildings positions.
Generates optimal building around Bank.
Idea came from game "They are billions"

# Best Solution 
Best city plan looks like triangle symmetry, we got 3 major paths. Algoritm is very heavy loaded, minor human adjustment is indicated.

### Legend:
1. Score - the more the better, we add points for every green house
2. Blank - path
.. Red Dot - path without connection

.. Triangle - Energy Tower

3. Stars - Bank (must have road around itself)
4. Squares - Houses, every house is builded of 4 parts, 
.. green: ok

.. yellow: squares are not fully connected (ignored)

.. black: house has no path to outer side

![Alt](/City_Plan/Gold.png?raw=true "Golden Solution")

# Please ignore minor issues 
PEP8. 
This was my first project. Many things could be done better, including readability and syntax. Operations complexity, better approach to problem, better mutation methods.


I did not want to use any GA library, I just wanted to train myself in python.