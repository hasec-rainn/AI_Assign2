# AI_Assign2
Othello Board game (with minMax AI). To play, enter into the command prompt
"GameDriver.py PLAYER1 PLAYER2", where PLAYER# can be either "human" or 
"minimax".
Must be executed in the same directory as GameDriver.py (and all its
dependancies).

It may take a while (15-30 seconds) for the minimax player to decide on a move
This is because every time the minimax player thinks of what to do,
it re-generates the entire state tree from scratch, which is costly.

A better implementation would have the state-tree generated once and saved,
allowing it to be referenced back to later. 