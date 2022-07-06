#COMP 3106 chess AI
#Alexander Breeze 	101 143 291
#Ryan Ayotte		101 073 548
#Alex Muir 			101 147 003
#https://github.com/niklasf/python-chess

import chess
from colorama import init
from numpy import char
from termcolor import colored
import unicodedata
init(convert=True)
import re
import sys
import time
import random

def main():
	board=chess.Board()
	render(board)
	winner=""
	random.seed(None)

	while(True):
		board.push_san(eval(sys.argv[1]+"(board,1)"))
		render(board)
		if(board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material()):
			winner="WHITE"
			break
		
		board.push_san(eval(sys.argv[2]+"(board,0)"))
		render(board)
		if(board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material()):
			winner="BLACK"
			break
	if board.is_stalemate() or board.is_insufficient_material():
		print("TIE")
	else:
		print("WINNER IS "+winner)


pieceDict={'R':colored("R ",'white'),'N':colored("N ",'white'),'B':colored("B ",'white'),'Q':colored("Q ",'white'),'K':colored("K ",'white'),'P':colored("P ",'white'),'r':colored("R ",'red'),'n':colored("N ",'red'),'b':colored("B ",'red'),'q':colored("Q ",'red'),'k':colored("K ",'red'),'p':colored("P ",'red'),'1':". ",'2':". . ",'3':". . . ",'4':". . . . ",'5':". . . . . ",'6':". . . . . . ",'7':". . . . . . . ",'8':". . . . . . . . "}
def render(board):
	fen='/'+board.fen()
	countdown=8
	out="\n\n  A B C D E F G H"
	for x in range (len(fen)):
		if fen[x]==" ":
			break
		if fen[x]=="/":
			out+="\n"+str(countdown)+" "
			countdown-=1
		else:
			out+=pieceDict[fen[x]]
	print(out)
	print("Basic: ", basicHeuristic(board))
	print("Advanced: ", advancedHeuristic(board))

#booList makes it return a list, if false it returns a string (different formatting, use for displaying)
def getMoveList(board,booList):
	if booList:
		return list(str(board.legal_moves)[38:len(str(board.legal_moves))-2].replace(" ", "").split(","))
	return str(board.legal_moves)[38:len(str(board.legal_moves))-2]

def userMove(board,color):
	colorString='red'
	if color:
		colorString='white';
	print(colored("MAKE A MOVE",colorString,'on_blue'))
	print("OPTIONS: "+getMoveList(board,False))
	inp="hith"
	while not inp in str(board.legal_moves):
		inp=input()
	return inp

def randomMove(board,color):
	time.sleep(1)
	numInt=random.randrange(0,board.legal_moves.count())
	return getMoveList(board,True)[numInt]

pieceValueDict={'R':5,'N':3,'B':3,'Q':9,'K':99,'P':1,'r':-5,'n':-3,'b':-3,'q':-9,'k':-99,'p':-1,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0,'/':0}
#evaluates the board, and returns a basic heuristic. Positive favors white.
def basicHeuristic(board):
	fen=board.fen()
	boardSum=0
	for x in range(len(fen)):
		if fen[x]==" ":
			break
		boardSum+=pieceValueDict[fen[x]]
	return boardSum

# Function takes the basic heuristic value and adds values based on board conditions
# Function takes the basic heuristic value and adds values based on board conditions
def advancedHeuristic(board):
    boardSum = basicHeuristic(board)
    threats=[]  # List of pieces that are in attacking range of the king
    wK = board.king(chess.WHITE)  #Find locations of each king
    bK = board.king(chess.BLACK)

    pMap = board.piece_map()  # Gets loctions of each piece on the board
    for i in pMap:
        h = str(pMap[i])
        up = h.isupper()  # Checks to see if the current piece is an uppercase (White) or lowercase (Black/Red)
        down = h.islower()
        if(up and i < bK+20 and i > bK-20) or (down and i < wK+20 and i > wK-20):# If it is close to the enemy king, add it to the list of threats
            threats.append(h)

    for x in threats:
        boardSum+=pieceValueDict[x]*0.05
    return boardSum


def minimaxMove(board, color):
	depth = 3
	minimax = minimaxMoveRecursive(board, color, depth)
	return minimax[1]

def minimaxMoveRecursive(board, color, depth):	#color=true=white=maximizer
	if depth == 0:
		# return (basicHeuristic(board), None)
		return (advancedHeuristic(board), None)
	
	if board.is_checkmate():
		if color: 	# maxNode implies that it is the turn of the player who called this alphaBetaMove, which means they are in checkmate, so -inf
			return (float('-inf'), None)
		else:
			return (float('inf'), None)
	
	if board.is_stalemate() or board.is_insufficient_material():
		return (0, None)

	# if this is a max node (the AI's turn), then return the best move (leads to the board with the biggest heuristic)
	if color:
		maxHeuristic = float('-inf')
		maxMoves = []
		for move in getMoveList(board,True):
			board.push_san(move)
			childValue = minimaxMoveRecursive(board, not color, depth-1)[0]
			if childValue == maxHeuristic:
				maxMoves.append(move)
			if childValue > maxHeuristic:
				maxHeuristic = childValue
				maxMoves = [move]
			board.pop()
		return (maxHeuristic, maxMoves[random.randrange(0,len(maxMoves))])
			
	# if this is not a max node (the players's turn), then return the worst move (leads to the board with the smallest heuristic)
	else:
		minHeuristic = float('inf')
		minMoves = []
		for move in getMoveList(board,True):
			board.push_san(move)
			childValue = minimaxMoveRecursive(board, not color, depth-1)[0]
			if childValue == minHeuristic:
				minMoves.append(move)
			if childValue < minHeuristic:
				minHeuristic = childValue
				minMoves = [move]
			board.pop()
		return (minHeuristic, minMoves[random.randrange(0,len(minMoves))])


def minimaxAlphaBetaMove(board,color):
	depth = 4

	minimax = minimaxAlphaBetaMoveRecursive(board, color, depth, float('-inf'), float('inf'))
	#print("minimax:", minimax)
	return minimax[1]

def minimaxAlphaBetaMoveRecursive(board, color, depth, _alpha, _beta):	#color=true=white=maximizer
	# if depth is 0, return heuristic for board
	if depth == 0:
		# return (basicHeuristic(board), None)
		return (advancedHeuristic(board), None)
	
	elif board.is_checkmate():
		if color: 	# maxNode implies that it is the turn of the player who called this alphaBetaMove, which means they are in checkmate, so -inf
			return (float('-inf'), None)
		else:
			return (float('inf'), None)

	elif board.is_stalemate() or board.is_insufficient_material():
		return (0, None)

	alpha = _alpha
	beta = _beta

	# if this is a max node (the AI's turn), then return the best move (leads to the board with the biggest heuristic)
	if color:
		maxHeuristic = float('-inf')
		maxMoves = []

		for move in getMoveList(board,True):
			board.push_san(move)

			childValue = minimaxAlphaBetaMoveRecursive(board, not color, depth-1, alpha, beta)[0]
			
			if childValue == maxHeuristic:
				maxMoves.append(move)
			if childValue > maxHeuristic:
				maxHeuristic = childValue
				alpha = childValue
				maxMoves = [move]

				if maxHeuristic >= beta:
					board.pop()
					break
				
			board.pop()
			
		return (maxHeuristic, maxMoves[random.randrange(0,len(maxMoves))])
			
	# if this is not a max node (the players's turn), then return the worst move (leads to the board with the smallest heuristic)
	else:
		minHeuristic = float('inf')
		minMoves = []

		for move in getMoveList(board,True):
			board.push_san(move)

			childValue = minimaxAlphaBetaMoveRecursive(board, not color, depth-1, alpha, beta)[0]

			if childValue == minHeuristic:
				minMoves.append(move)
			if childValue < minHeuristic:
				minHeuristic = childValue
				beta = childValue
				minMoves = [move]

				if minHeuristic <= alpha:
					board.pop()
					break
				
			board.pop()
			
		return (minHeuristic, minMoves[random.randrange(0,len(minMoves))])
		

main()
