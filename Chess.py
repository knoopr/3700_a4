import datetime
from sys import maxint
class Chess_Player():
    def __init__ (self, given_Player, max_Player, given_Indexes = None, goal_Depth = 0, alpha_Beta= None):
        self.player = given_Player
        if self.player == "W":
            self.opponent = "B"
        else:
            self.opponent = "W"
        
        self.max = max_Player
        self.must_Take = []
        self.other_Moves = []
        self.depth = goal_Depth
        self.alpha = alpha_Beta[0]
        self.beta = alpha_Beta[1]

        if given_Indexes == None:   #If no index has been generated for the current board, load it
            count = 0
            the_Board = []
            while count != 8:
                the_Board.append(raw_input())
                count += 1
        
            self.index_Pieces(the_Board)
        else:
            self.player_Pieces = given_Indexes[1]
            self.opponent_Pieces = given_Indexes[0]



    def Play_game(self):
        if abs(self.Check_win()) == 1000:
            return (None, self.Check_win())
        elif self.depth == 0:
            return (None, self.Score_board())
        else:
            self.Possible_moves()
            if len(self.must_Take) == 0:
                for start, end in self.other_Moves:
                    p_Piece = self.player_Pieces[start]
                    del self.player_Pieces[start]
                    self.player_Pieces[end] = p_Piece
                    
                    resultant_Score = Chess_Player(self.opponent, self.max, (self.player_Pieces, self.opponent_Pieces), self.depth-1, (self.alpha, self.beta)).Play_game()
                    
                    del self.player_Pieces[end]
                    self.player_Pieces[start] = p_Piece
                    
                    if self.max == self.player:
                        if resultant_Score[1] != None and resultant_Score[1] > self.alpha[1]:
                            self.alpha = ((start,end), resultant_Score[1])
                            if self.beta[1] < self.alpha[1]:
                                break
                    else:
                        resultant_Score = (resultant_Score[0], -resultant_Score[1])
                        if resultant_Score[1] != None and resultant_Score[1] < self.beta[1]:
                            self.beta = ((start,end), resultant_Score[1])
                            if self.beta[1] < self.alpha[1]:
                                break
            
                if self.max == self.player:
                    return self.alpha
                else:
                    return self.beta
            else:
                for start, end in self.must_Take:
                    p_Piece = self.player_Pieces[start]
                    o_Piece = self.opponent_Pieces[end]
                    del self.player_Pieces[start]
                    self.player_Pieces[end] = p_Piece
                    del self.opponent_Pieces[end]
                    
                    resultant_Score = Chess_Player(self.opponent, self.max, (self.player_Pieces, self.opponent_Pieces), self.depth-1, (self.alpha, self.beta)).Play_game()
                    del self.player_Pieces[end]
                    self.player_Pieces[start] = p_Piece
                    self.opponent_Pieces[end] = o_Piece

                    if self.max == self.player:
                        if resultant_Score[1] != None and resultant_Score[1] > self.alpha[1]:
                            self.alpha = ((start,end), resultant_Score[1])
                            if self.beta[1] < self.alpha[1]:
                                break
                    else:
                        resultant_Score = (resultant_Score[0], -resultant_Score[1])
                        if resultant_Score[1] != None and resultant_Score[1] < self.beta[1]:
                            self.beta = ((start,end), resultant_Score[1])
                            if self.beta[1] < self.alpha[1]:
                                break
                                    
                if self.max == self.player:
                    return self.alpha
                else:
                    return self.beta





    #Indexes the locations for O(1) searching
    def index_Pieces(self, the_Board):
        
        upper_Pieces = {}
        lower_Pieces = {}
        
        x = 0
        y = 0
        #For every location in the board index the piece if it's not a
        for y in range(8):
            for x in range(8):
                if the_Board[y][x] != " ":
                    if the_Board[y][x].isupper():
                        upper_Pieces[(y,x)] = the_Board[y][x]
                    else:
                        lower_Pieces[(y,x)] = the_Board[y][x]


        if self.player == "W":
            self.player_Pieces = lower_Pieces
            self.opponent_Pieces = upper_Pieces
        else:
            self.player_Pieces = upper_Pieces
            self.opponent_Pieces = lower_Pieces


    def Possible_moves(self):
        self.possible_Takes = []
        for (y,x), piece in self.player_Pieces.items():
            if piece.lower() == "p":
                self.Check_pawn(y,x)
            elif piece.lower() == "r":
                self.Check_rook(y,x)
            elif piece.lower() == "n":
                self.Check_knight(y,x)
            elif piece.lower() == "b":
                self.Check_bishop(y,x)
            elif piece.lower() == "q":
                self.Check_bishop(y,x)
                self.Check_rook(y,x)
            elif piece.lower() == "k":
                self.Check_king(y,x)



    def Check_pawn(self, y, x):
        if self.player == "B":
            if y+1 != 8:
                if (y+1, x+1) in self.opponent_Pieces:
                    self.must_Take.append(((y,x),(y+1,x+1)))
                if (y+1, x-1) in self.opponent_Pieces:
                    self.must_Take.append(((y,x),(y+1,x-1)))
                if (y+1, x) not in self.opponent_Pieces and (y+1,x) not in self.player_Pieces:
                    self.other_Moves.append(((y,x),(y+1,x)))
                if y == 1 and (y+2, x) not in self.opponent_Pieces and (y+1,x) not in self.player_Pieces and (y+2,x) not in self.player_Pieces :
                    self.other_Moves.append(((y,x),(y+2,x)))
        else:
            if y-1 != 0:
                if (y-1, x+1) in self.opponent_Pieces:
                    self.must_Take.append(((y,x),(y-1,x+1)))
                if (y-1, x-1) in self.opponent_Pieces:
                    self.must_Take.append(((y,x),(y-1,x-1)))
                if (y-1, x) not in self.opponent_Pieces and (y-1,x) not in self.player_Pieces:
                    self.other_Moves.append(((y,x),(y-1,x)))
                if y == 6 and (y-2, x) not in self.opponent_Pieces and (y-1,x) not in self.player_Pieces and (y-2,x) not in self.player_Pieces :
                    self.other_Moves.append(((y,x),(y-2,x)))



    def Check_knight(self, y, x):
        py = y+1            #Down 1
        if py <= 7:
            px = x+2
            if px <= 7:
                if (py,px) in self.opponent_Pieces:
                    self.must_Take.append(((y,x),(py,px)))
                elif (py,px) not in self.player_Pieces:
                    self.other_Moves.append(((y,x),(py,px)))
            px = x-2
            if px >= 0:
                if (py,px) in self.opponent_Pieces:
                    self.must_Take.append(((y,x),(py,px)))
                elif (py,px) not in self.player_Pieces:
                    self.other_Moves.append(((y,x),(py,px)))
        py = y-1            #Up 1
        if py >= 0:
            px = x+2
            if px <= 7:
                if (py,px) in self.opponent_Pieces:
                    self.must_Take.append(((y,x),(py,px)))
                elif (py,px) not in self.player_Pieces:
                    self.other_Moves.append(((y,x),(py,px)))
            px = x-2
            if px >= 0:
                if (py,px) in self.opponent_Pieces:
                    self.must_Take.append(((y,x),(py,px)))
                elif (py,px) not in self.player_Pieces:
                    self.other_Moves.append(((y,x),(py,px)))
        py = y+2            #Down 2
        if py <= 7:
            px = x+1
            if px <= 7:
                if (py,px) in self.opponent_Pieces:
                    self.must_Take.append(((y,x),(py,px)))
                elif (py,px) not in self.player_Pieces:
                    self.other_Moves.append(((y,x),(py,px)))
            px = x-1
            if px >= 0:
                if (py,px) in self.opponent_Pieces:
                    self.must_Take.append(((y,x),(py,px)))
                elif (py,px) not in self.player_Pieces:
                    self.other_Moves.append(((y,x),(py,px)))
        py = y-2            #Up 2
        if py >= 0:
            px = x+1
            if px <= 7:
                if (py,px) in self.opponent_Pieces:
                    self.must_Take.append(((y,x),(py,px)))
                elif (py,px) not in self.player_Pieces:
                    self.other_Moves.append(((y,x),(py,px)))
            px = x-1
            if px >= 0:
                if (py,px) in self.opponent_Pieces:
                    self.must_Take.append(((y,x),(py,px)))
                elif (py,px) not in self.player_Pieces:
                    self.other_Moves.append(((y,x),(py,px)))



    def Check_rook(self, y, x):
        for py in range (y+1,8):
            if (py, x) in self.player_Pieces:
                break
            elif (py, x) in self.opponent_Pieces:
                self.must_Take.append(((y,x),(py,x)))
                break
            else:
                self.other_Moves.append(((y,x),(py,x)))
        for px in range (x+1,8):
            if (y, px) in self.player_Pieces:
                break
            elif (y, px) in self.opponent_Pieces:
                self.must_Take.append(((y,x),(y,px)))
                break
            else:
                self.other_Moves.append(((y,x),(y,px)))


    def Check_bishop(self, y, x):
        px = x
        py = y
        for count in range (8):     #Down right
            py += 1
            px += 1

            if py > 7 or px > 7:
                break
            elif (py,px) in self.player_Pieces:
                break
            elif (py,px) in self.opponent_Pieces:
                self.must_Take.append(((y,x),(py,px)))
                break
            else:
                self.other_Moves.append(((y,x),(py,px)))
        px = x
        py = y
        for count in range (8):     #Down left
            py += 1
            px -= 1
            
            if py > 7 or px < 0:
                break
            elif (py,px) in self.player_Pieces:
                break
            elif (py,px) in self.opponent_Pieces:
                self.must_Take.append(((y,x),(py,px)))
                break
            else:
                self.other_Moves.append(((y,x),(py,px)))
        px = x
        py = y
        for count in range (8):     #Up right
            py -= 1
            px += 1
            
            if py < 0 or px > 7:
                break
            elif (py,px) in self.player_Pieces:
                break
            elif (py,px) in self.opponent_Pieces:
                self.must_Take.append(((y,x),(py,px)))
                break
            else:
                self.other_Moves.append(((y,x),(py,px)))
        px = x
        py = y
        for count in range (8):     #Up left
            py -= 1
            px -= 1
            
            if py < 0 or px < 0:
                break
            elif (py,px) in self.player_Pieces:
                break
            elif (py,px) in self.opponent_Pieces:
                self.must_Take.append(((y,x),(py,px)))
                break
            else:
                self.other_Moves.append(((y,x),(py,px)))


    def Check_king(self, y, x):
        if y+1 <= 7:
            if (y+1,x) in self.opponent_Pieces:
                self.must_Take.append(((y,x),(y+1,x)))
            elif (y+1,x) not in self.player_Pieces:
                self.other_Moves.append(((y,x),(y+1,x)))
            
            if (y+1,x+1) in self.opponent_Pieces:
                self.must_Take.append(((y,x),(y+1,x+1)))
            elif (y+1,x+1) not in self.player_Pieces and x+1 <= 7:
                self.other_Moves.append(((y,x),(y+1,x+1)))
            
            if (y+1,x-1) in self.opponent_Pieces:
                self.must_Take.append(((y,x),(y+1,x-1)))
            elif (y+1,x-1) not in self.player_Pieces and x-1 >= 0:
                self.other_Moves.append(((y,x),(y+1,x-1)))
        elif y-1 >= 0:
            if (y-1,x) in self.opponent_Pieces:
                self.must_Take.append(((y,x),(y-1,x)))
            elif (y-1,x) not in self.player_Pieces:
                self.other_Moves.append(((y,x),(y-1,x)))
            
            if (y-1,x+1) in self.opponent_Pieces:
                self.must_Take.append(((y,x),(y-1,x+1)))
            elif (y-1,x+1) not in self.player_Pieces and x+1 <= 7:
                self.other_Moves.append(((y,x),(y-1,x+1)))
            
            if (y-1,x-1) in self.opponent_Pieces:
                self.must_Take.append(((y,x),(y-1,x-1)))
            elif (y-1,x-1) not in self.player_Pieces and x-1 >= 0:
                self.other_Moves.append(((y,x),(y-1,x-1)))



    def Score_board(self):
        score = 0
        for piece in self.player_Pieces.values():
            if piece.lower() == "p":
                score -= 1
            elif piece.lower() == "n":
                score -= 3
            elif piece.lower() == "b":
                score -= 3
            elif piece.lower() == "r":
                score -= 5
            elif piece.lower() == "q":
                score -= 9
            elif piece.lower() == "k":
                score -= 4
        for piece in self.opponent_Pieces.values():
            if piece.lower() == "p":
                score += 1
            elif piece.lower() == "n":
                score += 3
            elif piece.lower() == "b":
                score += 3
            elif piece.lower() == "r":
                score += 5
            elif piece.lower() == "q":
                score += 9
            elif piece.lower() == "k":
                score += 4
        return score


    def Check_win(self):
        score = 0
        if len(self.player_Pieces) == 0:
            return 1000
        elif len(self.opponent_Pieces) == 0:
            return -1000
        else:
            return 0


    def Print_board(self):
        for y in range(8):
            for x in range (8):
                if (y,x) in self.player_Pieces:
                    print self.player_Pieces[(y,x)],
                elif (y,x) in self.opponent_Pieces:
                    print self.opponent_Pieces[(y,x)],
                else:
                    print " ",
            print ""
        print "\n\n"



if __name__ == "__main__":
    first_Player = raw_input()
    result =  Chess_Player(first_Player,first_Player, goal_Depth=3, alpha_Beta=[((None), -maxint), ((None), maxint)]).Play_game()
    

    print str(result[0][0][0]) + "," + str(result[0][0][1]) + "-" + str(result[0][1][0]) + "," + str(result[0][1][1])
