'''
    MODIFIED BY: Thomas Weathers - May 2020
    Created by: Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''
import sys

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        return NotImplementedError()



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


    def Minimax(self, board, symbol):
        value = max_val(self,board)
        #value[1].display()
        return value[1]

    def get_move(self,board):
        return self.Minimax(board,self.symbol)


    
def get_possible_moves(self, board):
        options = []
        for c in range(0,4):
            for r in range(0,4):
                if(board.is_legal_move(c,r,self.symbol)):
                    new = board.cloneOboard()
                    new.play_move(c,r,self.symbol)
                    options.append(new)
                    #rank option before adding to options array
        return options


def Util(self,symbol,board):
    #rank the options for my symbol (minimax algorithm)
    opp = board.count_score(self.oppSym)
    mine = board.count_score(self.symbol)
    if(mine > opp):
        return 1
    elif(mine < opp):
        return -1  #still needs to be played
    else:
        return 0    

def max_val(self,board):
    value = sys.maxsize * -1
    pair = (value,board)

    if not board.has_legal_moves_remaining(self.symbol):
        return (Util(self,self.symbol,board),board)

    for option in get_possible_moves(self,board):
        temp = max(value,max_val(self,option)[0])
        if temp == value:
            pair = (temp,board)
        else:
            pair = (temp,option)

    return pair

def mini_val(self,board):
        value = sys.maxsize
        pair = (value, board)

        if not board.has_legal_moves_remaining():
            return (Util(self,self.symbol,board),board)

        for option in get_possible_moves(board):
            temp = min(value,max_val(option)[0])
            if temp == value:
                pair = (temp,board)
            else:
                pair = (temp,option)

        return pair
    
def get_possible_moves(self, board):
        options = []
        for c in range(0,4):
            for r in range(0,4):
                if(board.is_legal_move(c,r,self.symbol)):
                    new = board.cloneOBoard()
                    new.play_move(c,r,self.symbol)
                    options.append(new)
                    #rank option before adding to options array
        return options