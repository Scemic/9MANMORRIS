import sys
import numpy as np
class Board:

    def __init__(self):
        # init empty board
        self.board_array = np.zeros(24,dtype=int)
        self.num_checkers_one = 0
        self.num_checkers_two = 0
        self.phase = 0
        self.mills = []
        
    def __str__(self):
        print("Board :",self.board_array)
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
        self.check_mill()
        return True
    
    # pos is the index that corresponds to a moved/removed marker that potentially removes a mill
    def check_in_mill(self,pos):
        return any(pos in mill for mill in self.mills)
    
    # Remove a mill based on one of its indices
    def remove_from_mill(self,pos):
        for mill in self.mills:
            if pos in mill:
                self.mills.remove(mill)
    
    def remove_mill_if_altered(self,pos):
        if self.check_in_mill(pos):   # New stuff, might break
            self.remove_from_mill(pos)#
    
    def move_marker(self,FROM,TO,player_moving):
        if self.board_array[FROM] != player_moving:
            print("Not your marker mate")
            return False
        
        if TO in self.get_neighbor_idx(FROM):
            result = self.fly_marker(FROM,TO,player_moving)
            print(str(player_moving)+ " moved from ", FROM + 1, " to ",TO + 1)
            # Both those are already in fly_marker!
            #self.check_mill()                
            #self.remove_mill_if_altered(FROM) # might break
            return result # We return whatever fly_marker has determined
        else:
            print("You cannot move the marker here!")
            return False
    
    # For "AI"
    def dumb_move_marker(self):
        for idx,marker in enumerate(self.board_array):
            if marker == 2:
                direct_neighbors = self.get_neighbor_idx(idx)
                for neighbor in direct_neighbors:
                    if self.board_array[neighbor] == 0:
                        self.move_marker(idx,neighbor,2)
                        return True
        return False
    
    
    def dumb_fly_marker(self):
        for idx,marker in enumerate(self.board_array):
            if marker == 2:
                for idx2,marker2 in enumerate(self.board_array):
                    if marker2 == 0:
                        return self.fly_marker(idx,idx2,2)
        return False
    
    def fly_marker(self,FROM, TO,player_moving):
        if self.board_array[FROM] != player_moving:
            print("Not your marker mate")
            return False
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
        
        self.remove_mill_if_altered(FROM) # might break
        return True
    
    
    def remove_marker(self,pos,player_removing):
        if self.board_array[pos] == 0:
            print("No marker to remove :(")
            return False
        if self.board_array[pos] == player_removing:
            print("This is one of yours mate")
            return False
        # Sorry this is disgusting, change later
        if player_removing == 1:
            player = 2
        else:
            player = 1
        if  any(pos in mill for mill in self.mills) and not self.check_only_mills(player):
            print("Are you really trying to remove a mill's marker? Try again")
            return False
        # Remove the marker
        self.board_array[pos] = 0
        self.remove_mill_if_altered(pos) # might break
        return True
    
    # This method checks if a player only has marker present in mills, in which case they are removeable
    def check_only_mills(self,player_num):
        for idx,marker in enumerate(self.board_array): 
            if marker == player_num:
                if not any(idx in mill for mill in self.mills):
                    return False
        return True
    """
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
    """   
    def check_mill(self):
            neighbors = [
            [0,1,2],[3,4,5],[6,7,8],[9,10,11],[12,13,14],[15,16,17],[18,19,20],[21,22,23],
            [0,9,21],[3,10,18],[6,11,15],[1,4,7],[16,19,22],[8,12,17],[5,13,20],[2,14,23]
            ]
            
            for neighbor in neighbors:
                if np.array_equal(self.board_array[neighbor],np.array([1,1,1])) and neighbor not in self.mills:
                    print(self)
                    
                    self.mills.append(neighbor) # We store the completed mill
                    #sys.exit('Player number 1 wins!')
                    print("You may remove one of the enemy's marker!")
                   
                    res = False
                    while not res:
                        selected_pos = input("Selected position > ")
                        res = self.remove_marker(int(selected_pos) - 1,1) # Player 1 here
                    
                if np.array_equal(self.board_array[neighbor],np.array([2,2,2])) and neighbor not in self.mills:
                    print(self)
                    self.mills.append(neighbor) # We store the completed mill
                    #sys.exit('Player number 2 wins!')
                    #AI stuff here
                    # Temporary "solution" before ML
                    print("The filthy AI may remove one of your marker!")
                    
                    for idx,marker in enumerate(self.board_array):
                        if marker == 1:
                            if self.remove_marker(idx,2): # AI here
                                print("The AI removed the marker at ",idx + 1,".")
                                break
                        
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

    def check_game_over(self):
        players= {1:0,2:0,0:0}
        for marker in self.board_array:
            players[marker] += 1
        
        if players[1] < 3:
            print("Game over - Player 2 wins")
            return True
        
        elif players[2] < 3:
            print("Game over - Player 1 wins")
            return True
        
        return False
    
    def get_markers_on_board(self):
        players= {1:0,2:0,0:0}
        for marker in self.board_array:
            players[marker] += 1        
        return players
    
if __name__ == '__main__':
    b = Board()
    b.place_marker(pos=3,player_num=1)
    b.place_marker(pos=4,player_num=1)
    b.place_marker(pos=5,player_num=1)
    print(b)
    print('Hello')

    #b.place_marker(pos=1,player_num=1)
    #b.place_marker(pos=2,player_num=1)
