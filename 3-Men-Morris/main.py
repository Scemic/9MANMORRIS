from .AlphaBeta import *
from .BoardLogic import *
from .heuristics import *
import time

alpha = float('-inf')
beta = float('inf')
depth = 3
ai_depth = 4

def boardOutput(board):
		
		print((board[0]+"(0)----------------------"+board[1]+"(1)----------------------"+board[2]+"(2)"));
		print("|                          |                         |");
		print("|                          |                         |");
		print((board[3]+"(3)----------------------"+board[4]+"(4)----------------------"+board[5]+"(5)"));
		print("|                          |                         |");
		print("|                          |                         |");
		print((board[6]+"(6)----------------------"+board[7]+"(7)----------------------"+board[8]+"(8)"));
			

def AI_VS_AI(heuristic1, heuristic2):

	board = []
	for i in range(9):
		board.append("X")

	evaluation = evaluator()
	
	print("Stage 1")
	for i in range(9):

		boardOutput(board)
		evalBoard = alphaBetaPruning(board, ai_depth, True, alpha, beta, True, heuristic1)

		if evalBoard.evaluator == float('inf'):
			print("AI Bot 1 has won!")
			exit(0)
		else:
			board = evalBoard.board
		
		boardOutput(board)
		evalBoard = alphaBetaPruning(board, ai_depth, False, alpha, beta, True, heuristic2)
		
		if evalBoard.evaluator == float('-inf'):
			print("AI Bot 2 has won!")
			exit(0)
		else:
			board = evalBoard.board

	'''print("Stage 2")
	while True:

		boardOutput(board)
		evalBoard = alphaBetaPruning(board, ai_depth, True, alpha, beta, False, heuristic1)

		if evalBoard.evaluator == float('inf'):
			print("AI Bot 1 has won!")
			exit(0)
		else:
			board = evalBoard.board

		boardOutput(board)
		evaluation = alphaBetaPruning(board, ai_depth, False, alpha, beta, False, heuristic2)

		if evaluation.evaluator == float('-inf'):
			print("AI Bot 2 has won")
			exit(0)
		else:
			board = evaluation.board
'''

def HUMAN_VS_AI(heuristic_stage1, heuristic_stage23):
	
	board = []
	for i in range(9):
		board.append("X")

	evaluation = evaluator()
		
	for i in range(9):

		boardOutput(board)
		finished = False
		while not finished:
			try:

				pos = int(eval(input("\nPlace '₣' piece: ")))	
				if board[pos] == "X":
					board[pos] = '₣'
					if isCloseMill(pos, board):
						itemPlaced = False
						while not itemPlaced:
							try:

								#pos = int(input("\nRemove '2' piece: "))
								if (getNumberOfPieces(board, "₣") == 3):
										finished = True
										
							except Exception:
								print("Input was either out of bounds or wasn't an integer")

					finished = True

				else:
					print("There is already a piece there")

			except Exception:
				print("Couldn't get the input value")
		
		boardOutput(board)
		evalBoard = alphaBetaPruning(board, depth, False, alpha, beta, True, heuristic_stage1)

		if evalBoard.evaluator == float('-inf'):
			print("You Lost")
			exit(0)
		else:
			board = evalBoard.board

	endStagesFinished = True
	while not endStagesFinished:

		boardOutput(board)
		
		#Get the users next move
		userHasMoved = False
		while not userHasMoved:
			try:
				pos = int(eval(input("\nMove '1' piece: ")))

				while board[pos] != '₣':
					pos = int(eval(input("\nMove '₣' piece: "))) 

				userHasPlaced = False
				while not userHasPlaced:

					newPos = int(eval(input("'1' New Location: ")))

					if board[newPos] == "X":
						board[pos] = 'X'
						board[newPos] = '₣'

						if isCloseMill(newPos, board):
							
							userHasRemoved = False
							while not userHasRemoved:
								try:

									pos = int(eval(input("\nRemove '2' piece: ")))
									
									if board[pos] == "€" and not isCloseMill(pos, board) or (isCloseMill(pos, board) and getNumberOfPieces(board, "₣") == 3):
										board[pos] = "X"
										userHasRemoved = True
									else:
										print("Invalid position")
								except Exception:
									print("Error while accepting input")

						userHasPlaced = True
						userHasMoved = True

					else:
						print("You cannot move there")

			except Exception:
				print("You cannot move there")

		if getEvaluationStage23(board) == float('inf'):
			print("You Win!")
			exit(0)

		boardOutput(board)

		evaluation = alphaBetaPruning(board, depth, False, alpha, beta, False, heuristic_stage23)

		if evaluation.evaluator == float('-inf'):
			print("You Lost")
			exit(0)
		else:
			board = evaluation.board


if __name__ == "__main__":
	
	print("Welcome to Nine Mens Morris")
	print("==========================")
	print("1. Is Human vs AI")
	print("2. Is AI vs AI")
	gametype = eval(input("Please enter 1 or 2: "))

	while gametype != "1" and gametype != "2":
		gametype = eval(input("Please enter 1 or 2: "))

	if gametype == "1":
		HUMAN_VS_AI(numberOfPiecesHeuristic, AdvancedHeuristic)
	elif gametype == "2":
		AI_VS_AI(numberOfMoveablePiecesHeuristic, AdvancedHeuristic)

	















	
