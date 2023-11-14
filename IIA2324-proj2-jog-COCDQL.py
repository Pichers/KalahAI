#Função de avaliação de estados de Kalah no contexto da
#Avaliação Contínua 3 da UC IIA de 2023/2024
#
#António Almeida - fc58235
#Pedro Cardoso - fc58212
#14 de Novembro de 2023

from kalah import *
from jogos import *
from utils import *

def func_COCDQL(estado, jogador):
    POTENTIAL_STEAL = 0.8
    DIFFERENCE_TO_OPPONENT = 1
    LEFT_SIDE = 0.25
    RIGHT_SIDE = 0.25
    CAPTURED = 0.625
    CLOSE_WIN = 0.25
    CLOSE_LOSS = 0.25
    PLAY_AGAIN = 0.3

    WIN = 100
    LOSS = -100

    result = 0
    isSouth = (jogador == estado.SOUTH)
    board = estado.state

    #win +1000, loss -1000
    if estado.is_game_over():
        aux = estado.result()
        return aux * WIN if isSouth else aux  * LOSS
    
    if isSouth:
        if board[6] > 24:
            return WIN
        elif board[13] > 24:
            return LOSS
    else:
        if board[13] > 24:
            return WIN
        elif board[6] > 24:
            return LOSS
        
    if board[6] + board[13] == 48:
        return 0
        
    #Maximize captured
    result += board[6 + (7 * (not isSouth))] * CAPTURED
        
    #How far ahead of the opponent
    result += (board[6 + (7 * (not isSouth))] - board[6 + (7 * isSouth)]) * DIFFERENCE_TO_OPPONENT

    #How close I am to winning
    result += (board[6 + (7 * (not isSouth))] - 25) * CLOSE_WIN

    #How close I am to losing
    result -= (board[6 + (7 * (isSouth))] - 25) * CLOSE_LOSS


    #Maximum steal in this move
    if estado.to_move == jogador:
        result -= steal_COCDQL(estado, jogador) * POTENTIAL_STEAL
    else:
        result += steal_COCDQL(estado, estado.to_move) * POTENTIAL_STEAL

    #Can play again
    if estado.to_move == jogador:
        result += 5 * PLAY_AGAIN

    #Marbles on left side
    for i in range(4,6):
        result -= board[i + (7 * (not isSouth))] * LEFT_SIDE

    #Marbles on right side
    for i in range(0,2):
        result += board[i + (7 * (not isSouth))] * RIGHT_SIDE

    return result



def steal_COCDQL(state, toMove):
    maxSteal = 0
    isSouth = (toMove == state.SOUTH)
    board = state.state
    
    for i in range(6):
        pos = i + (7 * (not isSouth)) 
        newPos = (pos + board[pos]) // 13

        if(isSouth):
            
            if newPos < 6 and board[newPos] == 0:
                if board[12 - newPos] > maxSteal:
                    maxSteal = board[12 - newPos]
        else:
            
            if newPos > 6 and board[newPos] == 0:
                if board[12 - newPos] > maxSteal:
                    maxSteal = board[12 - newPos]

        return maxSteal + 1

