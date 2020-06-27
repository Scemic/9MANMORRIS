from Utility import *
import copy

def adjacentLocations(position):
	'''
	Return pieces adjacent to the piece at position
	@param position: index of the piece
	'''
	adjacent = [
		[1, 3, 4],
		[0, 2, 4],
		[1, 5, 4],
		[0, 4, 6],
		[0, 1, 2, 3, 5, 6, 7, 8],
		[2, 4, 8],
		[3, 4, 7],
		[4, 6, 8],
		[4, 5, 7],
	]
	return adjacent[position]

def checkMillFormation(position, board, player):
	'''
	Return True if there's a mill at position for player on given board
	@param position: the index of the position we're checking
	@param board: the list of the current board
	@param player: string representation of the board piece color
	'''

	mill = [
		(isMill(player, board, 1, 2) or isMill(player, board, 3, 6) or isMill(player, board, 4, 8)),
		(isMill(player, board, 0, 2) or isMill(player, board, 4, 7)),
		(isMill(player, board, 5, 8) or isMill(player, board, 0, 1) or isMill(player, board, 4, 6)),
		(isMill(player, board, 0, 6) or isMill(player, board, 4, 5)),
		(isMill(player, board, 0, 8) or isMill(player, board, 2, 6) or isMill(player, board, 1, 7) or isMill(player, board, 3, 5)),
		(isMill(player, board, 2, 8) or isMill(player, board, 3, 4)),
		(isMill(player, board, 0, 3) or isMill(player, board, 7, 8) or isMill(player, board, 2, 4)),
		(isMill(player, board, 6, 8) or isMill(player, board, 1, 4)),
		(isMill(player, board, 6, 7) or isMill(player, board, 2, 5) or isMill(player, board, 0, 4)),
	]

	return mill[position]

def isMill(player, board, pos1, pos2):
	'''
	Return True if pos1 and pos2 on board both belong to player
	@param player: string representation of the board piece color
	@param board: current list
	@param pos1: first position index
	@param pos2: second position index
	'''

	if (board[pos1] == player and board[pos2] == player):
		return True
	return False

def isCloseMill(position, board):
	'''
	Return True if any player has a mill on position
	@param position: the index of the position we're checking
	@param board: the list of the current board
	'''

	player = board[position]
	# if position is not empty
	if (player != "X"):
		return checkMillFormation(position, board, player)
	
	return False

def stage1Moves(board):
	'''
	'''
	board_list = []

	for i in range(len(board)):
		# fill empty positions with white
		if (board[i] == "X"):
			board_clone = copy.deepcopy(board)
			board_clone[i] = "₣"

			if (isCloseMill(i, board_clone)):
				board_list = removePiece(board_clone, board_list)
			else:
				board_list.append(board_clone)
	return board_list

def stage2Moves(board):
	'''

	@param board: current list
	'''
	board_list = []
	for i in range(len(board)):
		if (board[i] == "₣"):
			adjacent_list = adjacentLocations(i)

			for pos in adjacent_list:
				if (board[pos] == "X"):
					board_clone = copy.deepcopy(board)
					board_clone[i] = "X"
					board_clone[pos] = "₣"

					if isCloseMill(pos, board_clone):
						board_list = removePiece(board_clone, board_list)
					else:
						board_list.append(board_clone)
	return board_list

def stage3Moves(board):
	'''
	'''
	board_list = []

	for i in range(len(board)):
		if (board[i] == "₣"):

			for j in range(len(board)):
				if (board[j] == "X"):
					board_clone = copy.deepcopy(board)

					board_clone[i] = "X"
					board_clone[j] = "₣"

					if (isCloseMill(j, board_clone)):
						board_list = removePiece(board_clone, board_list)
					else:
						board_list.append(board_clone)
	return board_list

def stage23Moves(board):
	if (numOfValue(board, "₣") == 3):
		return stage3Moves(board)
	else:
		return stage2Moves(board)

def removePiece(board_clone, board_list):
	'''
	'''
	for i in range(len(board_clone)):
		if (board_clone[i] == "€"):

			if not isCloseMill(i, board_clone):
				new_board = copy.deepcopy(board_clone)
				new_board[i] = "X"
				board_list.append(new_board)
	return board_list

def getPossibleMillCount(board, player):
	'''
	'''
	count = 0

	for i in range(len(board)):
		if (board[i] == "X"):
			if checkMillFormation(i, board, player):
				count += 1
	return count

def getEvaluationStage23(board):
	'''
	'''
	
	numWhitePieces = numOfValue(board, "₣")
	numBlackPieces = numOfValue(board, "€")
	mills = getPossibleMillCount(board, "₣")

	evaluation = 0

	board_list = stage23Moves(board)

	numBlackMoves = len(board_list)

	if numBlackPieces <= 2 or numBlackPieces == 0:
		return float('inf')
	elif numWhitePieces <= 2:
		return float('-inf')
	else:
		return 0

def potentialMillInFormation(position, board, player):
	'''
	'''
	adjacent_list = adjacentLocations(position)

	for i in adjacent_list:
		if (board[i] == player) and (not checkMillFormation(position, board, player)):
			return True
	return False

def getPiecesInPotentialMillFormation(board, player):
	'''
	'''
	count = 0

	for i in range(len(board)):
		if (board[i] == player):
			adjacent_list = adjacentLocations(i)
			for pos in adjacent_list:
				if (player == "1"):
					if (board[pos] == "€"):
						board[i] = "€"
						if isCloseMill(i, board):
							count += 1
						board[i] = player
				else:
					if (board[pos] == "₣" and potentialMillInFormation(pos, board, "₣")):
						count += 1
	return count
