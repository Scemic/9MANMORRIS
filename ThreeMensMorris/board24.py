import sys
import numpy as np
class Board:

    def __init__(self):
        # init empty board
        self.board_array = np.zeros(24,dtype=int)
        self.num_checkers_one = 0
        self.num_checkers_two = 0
        self.phase = 0

    def __str__(self):
        board = ' '
        for i in self.board_array:
            board = board + str(i)
        print((len(board)))
        out = board[1]+"(1)----------------------"+board[2]+"(2)----------------------"+board[3]+"(3)\n" \
        	 + "|                           |                           |\n" \
        	 +   "|       "+board[4]+"(4)--------------"+board[5]+"(5)--------------"+board[6]+"(6)     	| \n" \
        	 + "|       |                   |                    |      | \n" \
        	 + "|       |                   |                    |      | \n" \
        	 + "|       |        "+board[7]+"(7)-----"+board[8]+"(8)-----"+board[9]+"(9)          |      | \n" \
        	 + "|       |         |                   |          |      | \n" \
        	 + "|       |         |                   |          |      | \n" \
        	 + board[10]+"(10)---"+board[11]+"(11)----"+board[12]+"(12)               "+board[13]+"(13)----"+board[14]+"(14)---"+board[15]+"(15) \n" \
        	 + "|       |         |                   |          |      | \n" \
        	 + "|       |         |                   |          |      | \n" \
        	 + "|       |        "+board[16]+"(16)-----"+board[17]+"(17)-----"+board[18]+"(18)       |      | \n" \
        	 + "|       |                   |                    |      | \n" \
        	 + "|       |                   |                    |      | \n" \
        	 + "|       "+board[19]+"(19)--------------"+board[20]+"(20)--------------"+board[21]+"(21)     | \n" \
        	 + "|                           |                           |\n" \
        	 + "|                           |                           |\n" \
        	 + board[22]+"(22)----------------------"+board[23]+"(23)----------------------"+board[24]+"(24)\n"
        return out
    def place_marker(self,pos, player_num):
        # Check if position is vacant
        if self.board_array[pos] == player_num:
            return True
        if self.board_array[pos] == 0:
            self.board_array[pos] = player_num
            if player_num == 1:
                self.num_checkers_one += 1
            if player_num == 2:
                self.num_checkers_two += 1
        else:
            print('Position already set on board!')
            return False

        self.check_num_markers()
        #self.check_mill()
        return True

    def move_marker(self,FROM, TO):
        if self.board_array[FROM] == 0:
            print('No marker at from position')
            return False
        if self.board_array[TO] != 0:
            print('TO position already used')
            return False
        # change markers
        tmp = self.board_array[FROM]
        self.board_array[FROM] = 0
        self.board_array[TO] = tmp
        self.check_mill()
        return True

    def check_mill(self):
        neighbors = [
        [0,1,2],[3,4,5],[6,7,8],[9,10,11],[12,13,14],[15,16,17],[18,19,20],[21,22,23],
        [0,9,21],[3,10,18],[6,11,15],[1,4,7],[16,19,22],[8,12,17],[5,13,20],[2,14,22]
        ]
        for neighbor in neighbors:
            if np.array_equal(self.board_array[neighbor],np.array([1,1,1])):
                print(self)
                sys.exit('Player number 1 wins!')
            if np.array_equal(self.board_array[neighbor],np.array([2,2,2])):
                print(self)
                sys.exit('Player number 2 wins!')

    def get_neighbor_idx(self,pos):
        if pos == 0: return [1,9]
        if pos == 1: return [0,2,4]
        if pos == 2: return [1,14]
        if pos == 3: return [4,10]
        if pos == 4: return [1,3,5,7]
        if pos == 5: return [4,13]
        if pos == 6: return [7,11]
        if pos == 7: return [4,6,8]
        if pos == 8: return [7,12]
        if pos == 9: return [0,10,21]
        if pos == 10: return [3,9,11,18]
        if pos == 11: return [6,10,15]
        if pos == 12: return [8,13,17]
        if pos == 13: return [5,12,14,20]
        if pos == 14: return [2,13,23]
        if pos == 15: return [11,16]
        if pos == 16: return [15,17,19]
        if pos == 17: return [12,16]
        if pos == 18: return [10,19]
        if pos == 19: return [16,18,20,22]
        if pos == 20: return [13,19]
        if pos == 21: return [9,22]
        if pos == 22: return [19,21,23]
        if pos == 23: return [14,22]



    def get_rowcol_idx(self,pos):
        if pos == 0: return [1,2,9,21]
        if pos == 1: return [0,2,4,7]
        if pos == 2: return [0,1,14,23]
        if pos == 3: return [4,5,10,18]
        if pos == 4: return [1,3,5,7]
        if pos == 5: return [3,4,13,20]
        if pos == 6: return [7,8,11,15]
        if pos == 7: return [1,4,6,8]
        if pos == 8: return [6,7,12,17]
        if pos == 9: return [0,10,11,21]
        if pos == 10: return [3,9,11,18]
        if pos == 11: return [6,9,10,15]
        if pos == 12: return [8,13,14,17]
        if pos == 13: return [5,12,14,20]
        if pos == 14: return [2,12,13,23]
        if pos == 15: return [6,11,16,17]
        if pos == 16: return [15,17,19,22]
        if pos == 17: return [8,12,15,16]
        if pos == 18: return [3,10,19,20]
        if pos == 19: return [16,18,20,22]
        if pos == 20: return [5,13,18,19]
        if pos == 21: return [0,9,22,23]
        if pos == 22: return [16,19,21,23]
        if pos == 23: return [2,14,21,22]


    def check_num_markers(self):
        if self.num_checkers_one > 9:
            sys.exit('Player 1 placed too many markers')
        if self.num_checkers_two > 9:
            sys.exit('Player 2 placed too many markers')

    def convert_to_gui_array(self):
        gui_array = np.copy(self.board_array)
        for i in range(self.board_array.shape[0]):
            if self.board_array[i] == 2:
                gui_array[i] = -1
        return gui_array


if __name__ == '__main__':
    b = Board()
    b.place_marker(pos=3,player_num=1)
    b.place_marker(pos=4,player_num=1)
    b.place_marker(pos=5,player_num=1)
    print(b)
    print('Hello')

    #b.place_marker(pos=1,player_num=1)
    #b.place_marker(pos=2,player_num=1)
