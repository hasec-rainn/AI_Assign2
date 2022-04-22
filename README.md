# AI_Assign2
Othello Board game (with minMax AI)

It may take a while (15-30 seconds) for the minimax player to decide on a move
This is because every time the minimax player thinks of what to do,
it re-generates the entire state tree from scratch, which is costly.

A better implementation would have the state-tree generated once and saved,
allowing it to be referenced back to later. 