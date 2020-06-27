from .BoardLogic import *

def numberOfPiecesHeuristic(board, isStage1):
	'''
	Heuristic that looks at the number of pieces on the board
	'''
	
	numPlayerOneTokens = numOfValue(board, "₣")
	numPlayerTwoTokens = numOfValue(board, "€")

	moveablePiecesPlayer2 = 0

	if not isStage1:
		movablePiecesBlack = len(stage23Moves(board))

	if not isStage1:
		if numPlayerTwoTokens <= 2 or movablePiecesBlack == 0:
			evaluation = float('inf')
		elif numPlayerOneTokens <= 2:
			evaluation = float('-inf')
		else:
			evaluation = 200 * (numPlayerOneTokens - numPlayerTwoTokens)
	else:
		evaluation = 100 * (numPlayerOneTokens - numPlayerTwoTokens)

	return evaluation

def potentialMillsHeuristic(board, isStage1):
	'''
	Heuristic that looks at the number of potential mills on the board
	'''

	evaluation = 0

	numPlayerOneTokens = numOfValue(board, "₣")
	numPlayerTwoTokens = numOfValue(board, "€")

	numPossibleMillsPlayer1 = getPossibleMillCount(board, "₣")
	numPossibleMillsPlayer2 = getPossibleMillCount(board, "€")

	moveablePiecesPlayer2 = 0

	if not isStage1:
		movablePiecesBlack = len(stage23Moves(board))

	potentialMillsPlayer1 = getPiecesInPotentialMillFormation(board, "₣")
	potentialMillsPlayer2 = getPiecesInPotentialMillFormation(board, "€")

	if not isStage1:
		if numPlayerTwoTokens <= 2 or movablePiecesBlack == 0:
			evaluation = float('inf')
		elif numPlayerOneTokens <= 2:
			evaluation = float('-inf')
		else:
			if (numPlayerOneTokens < 4):
				evaluation += 100 * numPossibleMillsPlayer1
				evaluation += 200 * potentialMillsPlayer2
			else:
				evaluation += 200 * numPossibleMillsPlayer1
				evaluation += 100 * potentialMillsPlayer2
	else:
		if numPlayerOneTokens < 4:
			evaluation += 100 * numPossibleMillsPlayer1
			evaluation += 200 * potentialMillsPlayer2
		else:
			evaluation += 200 * numPossibleMillsPlayer1
			evaluation += 100 * potentialMillsPlayer2

	return evaluation

def numberOfMoveablePiecesHeuristic(board, isStage1):
	'''
	Heuristic that looks at the number of pieces and if they can move
	'''
	
	evaluation = 0

	numPlayerOneTokens = numOfValue(board, "₣")
	numPlayerTwoTokens = numOfValue(board, "€")

	moveablePiecesPlayer1 = 0
	moveablePiecesPlayer2 = 0

	if not isStage1:
		movablePiecesBlack = len(stage23Moves(board))

	if not isStage1:
		if numPlayerTwoTokens <= 2 or movablePiecesBlack == 0:
			evaluation = float('inf')
		elif numPlayerOneTokens <= 2:
			evaluation = float('-inf')
		else:
			evaluation = 100 * (numPlayerOneTokens - numPlayerTwoTokens)
			evaluation -= 50 * movablePiecesBlack
	else:
		evaluation = 100 * (numPlayerOneTokens - numPlayerTwoTokens)
		evaluation -= 50 * moveablePiecesPlayer2

	return evaluation


def AdvancedHeuristic(board, isStage1):
	'''
	Heuristic that looks at the number of pieces and the potential mills
	 that could be formed
	'''

	evaluation = 0

	numPlayerOneTokens = numOfValue(board, "₣")
	numPlayerTwoTokens = numOfValue(board, "€")

	numPossibleMillsPlayer1 = getPossibleMillCount(board, "₣")
	numPossibleMillsPlayer2 = getPossibleMillCount(board, "€")

	moveablePiecesPlayer1 = 0
	moveablePiecesPlayer2 = 0

	if not isStage1:
		movablePiecesBlack = len(stage23Moves(board))

	potentialMillsPlayer1 = getPiecesInPotentialMillFormation(board, "₣")
	potentialMillsPlayer2 = getPiecesInPotentialMillFormation(board, "€")

	if not isStage1:
		if numPlayerTwoTokens <= 2 or movablePiecesBlack == 0:
			evaluation = float('inf')
		elif numPlayerOneTokens <= 2:
			evaluation = float('-inf')
		else:
			if (numPlayerOneTokens < 4):
				evaluation += 100 * numPossibleMillsPlayer1
				evaluation += 200 * potentialMillsPlayer2
			else:
				evaluation += 200 * numPossibleMillsPlayer1
				evaluation += 100 * potentialMillsPlayer2
			evaluation -= 25 * movablePiecesBlack
			evaluation += 50 * (numPlayerOneTokens - numPlayerTwoTokens)
	else:
		if numPlayerOneTokens < 4:
			evaluation += 100 * numPossibleMillsPlayer1
			evaluation += 200 * potentialMillsPlayer2
		else:
			evaluation += 200 * numPossibleMillsPlayer1
			evaluation += 100 * potentialMillsPlayer2
		evaluation -= 25 * moveablePiecesPlayer2
		evaluation += 50 * (numPlayerOneTokens - numPlayerTwoTokens)

	return evaluation
