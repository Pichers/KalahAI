from kalah import *
from jogos import *
from utils import *



def arvore(state, player):
    POTENTIAL_STEAL = 40
    MARBLE_DIFFERENCE = 0
    DIFFERENCE_TO_OPPONENT = 10
    LEFT_SIDE = 0
    RIGHT_SIDE = 0

    result = 0
    isSouth = (player == state.SOUTH)
    board = state.state

    #win +1000, loss -1000
    if state.is_game_over():
        aux = state.result()
        return aux * 1000 if isSouth else aux  * -1000
    
    if isSouth:
        if board[6] > 24:
            return 1000
        elif board[13] > 24:
            return -1000
    else:
        if board[13] > 24:
            return 1000
        elif board[6] > 24:
            return -1000
        
    #Maximize captured ???
    
    #difference in pieces in each side
    if isSouth:
        for i in range(6):
            result += board[i] * MARBLE_DIFFERENCE
            result -= board[7+i] * MARBLE_DIFFERENCE
    else:
        for i in range(6):
            result -= board[i] * MARBLE_DIFFERENCE
            result += board[7+i] * MARBLE_DIFFERENCE
        
    #How far ahead of the opponent
    result += (board[6 + (7 * (not isSouth))] - board[6 + (7 * isSouth)]) * DIFFERENCE_TO_OPPONENT


    #Checks if it can move to the kalah
    result += steal(state, isSouth) * POTENTIAL_STEAL

    result -= steal(state, (not isSouth)) * POTENTIAL_STEAL

    #Marbles in the left most pits
    for i in range(6):
        p = i + (7 * (not isSouth))
        result += board[p] * ((5 - p) / (i + 1)) * LEFT_SIDE

    #Right most pit is empty
    for i in range(6):
        p = (5 - i) + (7 * (not isSouth))
        if board[p] == 0:
            result += (p / (i + 1)) * RIGHT_SIDE

    return result



def steal(state, isSouth):
    maxSteal = 0
    
    for i in range(6):
        board = state.state
        pos = i + (7 * (not isSouth)) 
        newPos = (pos + board[pos]) // 13

        if(isSouth):
            if pos >= 6:
                return -1
            
            if newPos < 6 and board[newPos] == 0:
                if board[12 - newPos] > maxSteal:
                    maxSteal = board[12 - newPos]
                #stolen += board[12 - newPos]
        else:
            if pos <= 6:
                return -1
            
            if newPos > 6 and board[newPos] == 0:
                if board[12 - newPos] > maxSteal:
                    maxSteal = board[12 - newPos]
                #stolen += board[12 - newPos]

        return maxSteal + 1

def profSol(state,player):
    ret = 0
    if player == state.SOUTH:
        for i in range(6):
            ret += state.state[i]
            ret -= state.state[7+i] 
    else:
        for i in range(6):
            ret -= state.state[i]
            ret += state.state[7+i] 
    if state.is_game_over():
        aux = state.result()
        return aux * 100 if player == state.SOUTH else aux  * -100
    return ret