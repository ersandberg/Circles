# Erik Sandberg
# Grid with two players
# Markers show where players were the previous turn
# Player chooses a space to "destroy", if enemy is there, wins game
# Reach Opponent's side of grid to win
# move move, shoot shoot, advance. move move, shoot shoot, advance

import Tkinter as tk
import os

gridsize = 5
possible_moves = ['up','down','left','right', 'stay']
possible_destroys = []
for i in range(gridsize):
    for j in range(gridsize):
        possible_destroys.append([i,j])
turn_counter = 0


class Board(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.canvas = tk.Canvas(self, width=500, height=500, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        self.rows = 100
        self.columns = 100
        self.cellwidth = 100
        self.cellheight = 100

        self.rect = {}
        self.oval = {}
        for column in range(gridsize):
            for row in range(gridsize):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                x_avg = (x1 + x2)/2.
                y_avg = (y1 + y2)/2.
                self.rect[row,column] = self.canvas.create_rectangle(x1,y1,x2,y2, fill="gray", tags="rect")
                self.oval[row,column] = self.canvas.create_oval(x1+2,y1+2,x2-2,y2-2,fill="white", tags="oval")
                self.rect[row,column] = self.canvas.create_text(x_avg,y_avg,text=str(row)+','+str(column) )

        self.redraw()


    def redraw(self): 
        # draw ovals at previous positons [-1] of players
        self.canvas.itemconfig("rect", fill="gray") 
        self.canvas.itemconfig("oval", fill="white")
        row1 = player1.position[-1][0]
        col1 = player1.position[-1][1]
        item_id1 = self.oval[row1,col1]
        row2 = player2.position[-1][0]
        col2 = player2.position[-1][1]
        item_id2 = self.oval[row2,col2]
        self.canvas.itemconfig(item_id1, fill=player1.color)
        self.canvas.itemconfig(item_id2, fill=player2.color)
        return

    def victory(self,winner,loser): 
        # draw ovals at ALL previous positons [-1] of players
        self.canvas.itemconfig("rect", fill="gray") 
        self.canvas.itemconfig("oval", fill="white")
        for i in range(len(loser.position)):
            row1 = loser.position[i][0]
            col1 = loser.position[i][1]
            item_id1 = self.oval[row1,col1]
            self.canvas.itemconfig(item_id1, fill=loser.color)
            
        for i in range(len(winner.position)):
            row2 = winner.position[i][0]
            col2 = winner.position[i][1]
            item_id2 = self.oval[row2,col2]                
            self.canvas.itemconfig(item_id2, fill=winner.color)            

class Player():
    def __init__(self,position,color,win_row):
        self.position = [position,position] # need two copies for first turn
        self.color = color
        self.win_row = win_row
        self.alive = True
        self.winner = False
        self.gridsize_x = gridsize
        self.gridsize_y = gridsize

    def die(self):
        self.alive = False

    def win(self):
        self.winner = True

    def move(self,direction): # string as direction
        if direction == 'left':
            if self.position[-1][1] != 0:
                self.position.append([self.position[-1][0],self.position[-1][1] - 1])
            else:
                print 'You cannot move there.'
                
        if direction == 'right':
            if self.position[-1][1] != gridsize-1:
                self.position.append([self.position[-1][0],self.position[-1][1] + 1])                
            else:
                print 'You cannot move there.'
                
        if direction == 'up':
            if self.position[-1][0] != 0: 
                self.position.append([self.position[-1][0] - 1,self.position[-1][1]])                
            else:
                print 'You cannot move there.'
                
        if direction == 'down':
            if self.position[-1][0] != gridsize-1:
                self.position.append([self.position[-1][0] + 1,self.position[-1][1]])                
            else:
                print 'You cannot move there.'
        if direction == 'stay':
            self.position = self.position


def turn(board,player,opponent):

    ### --- MOVEMENT --- ###

    os.system('clear')
    #print player.color, ' is at ', player.position#[-1]
    #print opponent.color, ' is at ', opponent.position#[-1]

    # PLAYER MOVES
    print player.color + ' is MOVING.'
    print 'Which way would you like to move?'
    print 'Type: stay / left / right / up / down'
    
    move = raw_input()
    while move not in possible_moves:
        print 'Which way would you like to move?'
        print 'Type: left / right / up / down'
        move = raw_input()

    player.move(move)

def shoot(board,player,opponent):
    ### --- DESTRUCTION --- ###
    # OPPONENT SHOOTS
    os.system('clear')
    #print player.color, ' is at ', player.position
    #print opponent.color, ' is at ', opponent.position

    if turn_counter: # No destruction on first turn
        print player.color + ' is SHOOTING.'
        print 'Which space will you destroy?'
        print 'Please type your answer with the format: x,y'
    
        destroyed = raw_input()
        destroyed = [int(destroyed[0]),int(destroyed[2])] # put in correct list format
        while destroyed not in possible_destroys:
            print 'Answer was not in correct format.'
            print 'Which space will you destroy?'
            print 'Example format: 3,2'
            destroyed = raw_input()

        if destroyed == opponent.position[-1]:
            print 'You killed your opponent.'
            opponent.die()
            return
        else:
            print 'You missed your opponent.'



# -- VICTORY NEEDS THE LOSER IN THE CALL
# -- BOARD.VICTORY NEED WINNER,LOSER IN THE CALL
def victory(winner,loser, board):
    print winner.color + ' player wins!'
    board.victory(winner,loser)
    
# Begin the game
player1 = Player([0,2],"green", 4)
player2 = Player([4,2],"red", 0)
board = Board()

if __name__ == "__main__":
    os.system('clear')
    while player1.alive or player2.alive:
        turn_counter +=1
        # move 1
        turn(board, player1, player2)
        if player1.position[-1][0] == player1.win_row:
            victory(player1,player2,board)
            break
        # move 2
        turn(board, player2, player1)
        if player2.position[-1][0] == player2.win_row:
            victory(player2,player1,board)
            break
        # shoot 2 -- Player two shoots first since Player 1 moved first (fair?)
        shoot(board, player2,player1)
        if player1.alive == False:
            victory(player2,player1,board)
            break
        # shoot 1 
        shoot(board, player1, player2)
        if player2.alive == False:
            victory(player1,player2,board)
            break

        board.redraw()
               '''
    #app = App()
    #app.mainloop()

