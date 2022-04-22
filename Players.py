'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''

import OthelloBoard
import operator

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol);

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)


class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol);
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
        self.gameTree = None


    def get_move(self, othelloBoard):
        
        rtNode = OthelloNode(othelloBoard,[], self.symbol, None)
        self.CompleteExpansion(rtNode, self.symbol)

        self.MiniMax(rtNode)
    
        choices = rtNode.nodes
        
        # for choice in choices:
        #     choice.PrintSelf()

        #input("test")
        return max(choices).action



    #################################################################
    # Function: CompleteExpansion
    # Desc: Takes in a board state in "OthelloNode" format and returns
    #       a tree of all possible board states that could arise from
    #       the input/origin board state.
    #
    #       Note that leaves are terminal game states.
    #       Additionally, CompleteExpansion computes each state's
    #       value (where higher=better for Max).
    #
    #       "Atop the Lone Throne for the Last, all is seen."
    #################################################################
    def CompleteExpansion(self, bdNode, turn):
        bdNode.nodes = self.Expansion(bdNode.oBoard, turn)

        if (bdNode.nodes == []): #no legal moves to be made: game over
            bdNode.value = bdNode.oBoard.count_score(self.symbol)
            return bdNode
        else:                   #still need to work down to base case
            if (self.symbol == turn):
                turn = self.oppSym
            else:
                turn = self.symbol

            for n in bdNode.nodes:
                self.CompleteExpansion(n, turn)


        return bdNode

    #################################################################
    # Function: Expansion
    # Desc: Takes in an Othello board state and returns a list with
    #       all the possible next board states, given the current
    #       board state.
    #       Note that this list is of board state *nodes*.
    #################################################################
    def Expansion(self, board, turn):
        #keep track of current state
        currState = board.cloneOBoard()
        #potential state that can be reached from current state
        expandedSt = board.cloneOBoard()
        #List of board nodes
        bnList = []



        if(turn == self.symbol): #AI's turn
            pSymbol = self.symbol
            altSybmol = self.oppSym
        else: #opponent's turn
            pSymbol = self.oppSym
            altSybmol = self.symbol

        for r in range(currState.rows):
            for c in range(currState.cols):
                if( currState.is_legal_move(c, r, pSymbol) ):
                    expandedSt.play_move(c, r, pSymbol) #create new state
                    bnList.append(OthelloNode(expandedSt.cloneOBoard(), [], altSybmol, (c,r) ))

                    expandedSt = board.cloneOBoard() #revert to prev state

        return bnList

    #################################################################
    # Function: MiniMax
    # Desc: Assigns values to each node in a completely expanded tree
    #       of the game.
    #       Does so recursively
    #################################################################
    def MiniMax(self, bdNode):
        if(bdNode.nodes != []): #Go to leaves first to find base values
            for node in bdNode.nodes:
                self.MiniMax(node)
        else:   #we're at a leaf node, which means node.value=utility
            bdNode.value = bdNode.oBoard.count_score(self.symbol)
            return
        
        #At this point, we can assume deeper nodes have their values
        #(ie, each node in bdNodes.nodes has a value)
        if (bdNode.turn == self.symbol):
            #its the AI's turn: it wants to play (goto the next state)
            #that maximizes its performance
            bdNode.value = max(bdNode.nodes).value
        else:
            #its the human's turn: it wants to play (goto the next state)
            #that minimizes the AI's performance
            bdNode.value = min(bdNode.nodes).value
        


                
        

class OthelloNode:
    def __init__(self, board, nodes, turn, action):
        self.turn = turn
        self.value = None
        self.oBoard = board
        self.nodes = nodes
        self.action = action #the action that led to this state

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def AddNode(self,node):
        self.nodes.append(node)

    def PrintSelf(self):
        print("==========OthelloNode==========")
        self.oBoard.display()
        print("###Action:", self.action)
        print("###Turn:", self.turn)
        print("###Value:", self.value)
        print("###number of children nodes:", len(self.nodes))