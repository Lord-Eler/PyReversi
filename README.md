# PyReversi ![](docs/icon.png)
## Introduction
The goal of this project was to develop an AI playing Reversi, with a correct level.
I started from scratch by coding the Reversi app, which can be played by two human players, one human player against the AI, or two AIs.

<img src='docs/game.png' alt='Game Screen' width=50%>

## Installation
Clone the repository and install the required modules :

    git@github.com:ronan-lebas/PyReversi.git
    cd PyReversi
    pip install -r requirements.txt

## How to use it
Type :

    python main.py
Then select the options you want for the game.  
You can play with or without available moves visibility :

<img src='docs/game.png' alt='Game Screen' width=20%>
<img src='docs/game_no_help.png' alt='Game Screen' width=20%>

Simply click on the case you want to place a disk, but make sure to wait your turn before clicking if you play against the AI. Just press `echap` if you want to stop the game.

## How it works
After some research, I decided to use the Monte-Carlo Tree Search (MCTS) algorithm, since it is used mainly for two players games with perfect information and a high branching factor, which is the case of Reversi.
More explanations on MCTS can be found [here](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search).

Aside of the number of iterations of MCTS per move (which is just a compromise between skill and computation time), there is one parameter to tweak to optimize MCTS : the exploration factor. This constant tells the algorithm to favor moves that are known to be good (exploitation), or to favor the analysis of moves that are rather unknown (exploration).  
To find a good exploration factor, I set up tournaments with multiple versions of my AI, each having a different exploration factor. The range for the factors was initially [0.6,1.5] since I found [here](https://dke.maastrichtuniversity.nl/m.winands/documents/mctshybrids.pdf) that a good factor is 0.7 for Reversi, and the theoretical value is sqrt(2) = 1.41.

Here are some of the graphs I got :

<img src='docs/second_graph.png' alt='First Graph' width=40%>

<img src='docs/fourth_graph.png' alt='Second Graph' width=40%>

I can't extract a relevant value from this method, because the behavior of the win rate is too random, althought values slightly greater than 0.6 and values slightly smaller than 1 seem to be more efficient.  
I chose to set the default exploration factor to 0.7, since it gives very correct results.