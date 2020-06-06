# GeneticAlgoritm
#### Problem
Find optimal city plan
#
## Evolution mechanics implemented
* Clone

    Random areas of board are cloned from target to current agent

* Swap 

    Random areas positions are swaped inside agent
    
* Shuffle

    In random positions random elements are places
    
Evolutions are rejected if they decrease score, only swap persists.


* Drop out
    
    Every agent has chance to not survive. At each epoch, 10% of population is removed and replaced with new random agents. 
### First results
Best results so far.

![Best home from run](./run4/best_0.png)

![Scores](./run4/stats_06-06--16-03-30.png)

#### Legend:
Tower - power
Bank - always in center
Homes - green are good, black has no path reach, red has no power


### Requriements
```
conda create -n genetic python=3.8
conda activate genetic
pip install -r requrements.txt
```
#### Next steps
Add outer line for 'real' electricity input, it will make problem harder.
