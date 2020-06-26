#def update_screen (state, to, origin):

def update_screen (state, input, origin):
	board = state.split(' ')
	
	TempOLDPosition = int(origin)
	TempPiece = board[TempOLDPosition]

	TempNEWPosition = int(input)
	board[TempNEWPosition] = TempPiece

	board[TempOLDPosition] = 'O'

	print((board[1]+"(1)----------------------"+board[2]+"(2)----------------------"+board[3]+"(3)"));
	print("|                           |                           |");
	print(("|       "+board[4]+"(4)--------------"+board[5]+"(5)--------------"+board[6]+"(6)     	|"));
	print("|       |                   |                    |      |");
	print("|       |                   |                    |      |");
	print(("|       |        "+board[7]+"(7)-----"+board[8]+"(8)-----"+board[9]+"(9)          |      |"));
	print("|       |         |                   |          |      |");
	print("|       |         |                   |          |      |");
	print((board[10]+"(10)---"+board[11]+"(11)----"+board[12]+"(12)               "+board[13]+"(13)----"+board[14]+"(14)---"+board[15]+"(15)"));
	print("|       |         |                   |          |      |");
	print("|       |         |                   |          |      |");
	print(("|       |        "+board[16]+"(16)-----"+board[17]+"(17)-----"+board[18]+"(18)       |      |"));
	print("|       |                   |                    |      |");
	print("|       |                   |                    |      |");
	print(("|       "+board[19]+"(19)--------------"+board[20]+"(20)--------------"+board[21]+"(21)     |"));
	print("|                           |                           |");
	print("|                           |                           |");
	print((board[22]+"(22)----------------------"+board[23]+"(23)----------------------"+board[24]+"(24)"));

	board_join = " "
	board_join = board_join.join(board)

	return board_join
i = 1	
while i<6:


	text_file = open("QUANTUM_MOVE.txt", "r")
	board_split = text_file.read().split(',')

	board_new = update_screen (board_split[0], board_split[8], board_split[9])

	h_origin=int(input('Which piece do you want to move (position)?:'))

	h_input=int(input('Where do you want to move it (position)?:'))

	board_bot = update_screen (board_new, h_input, h_origin)
	print (board_bot)
	print ("Loop Time!")
	i=i+1
