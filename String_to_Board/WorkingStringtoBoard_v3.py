text_file = open("QUANTUM_MOVE.txt", "r")
board = text_file.read().split(' ')

TempOLDPosition = int(board[39])
TempPiece = board[TempOLDPosition]

TempNEWPosition = int(board[38])
board[TempNEWPosition] = TempPiece

board[TempOLDPosition] = 'O'

#board = 'E O O O O O O O O O O O O O O O O O O M O O O O'

#board = board.split (' ')

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