#Copied from previous attempt, added a thing where it only plays one game per AI, saves the top 30 for breeding (and 20 randoms). If more than 30 play perfectly, 
#instead of rebreeding (and possibly losing a perfect AI in favor of imperfect ones that got lucky) it ups the number of games. If I get 31 perfect AI's 
#it will enter an infinite loop, but I don't think it will get that far and if it does I will consider it a success. 
#This also makes it run faster (in theory), because the amount of games it plays (processing time) is dynamically minimal, not statically arbitrary. 
#(each epoch advances less because less games means a less accurate fitness function, but overall it should still be better.

#edit: made it so if numGames gets too high it ups difficulty, when difficulty maxes out it is considered complete, and lets you play the champion.

#I will import my minimax code, store every option in a dictionary (hashmap) for speed and use that as the opponent too, with hybrid class shifting between minimax and random


import numpy as np
import random

class Board:
    def __init__(self):
        self.board=np.zeros(9)
        self.STATE=0
    def state(self):
        if self.STATE!=0:
            return self.STATE
        board=self.board
        if board[4]!=0 and ((board[4]==board[0] and board[4]==board[8]) or (board[4]==board[6] and board[4]==board[2]) or (board[4]==board[3] and board[4]==board[5]) or (board[4]==board[1] and board[4]==board[7])):
            return board[4]
        if board[0]!=0 and ((board[0]==board[3] and board[0]==board[6]) or (board[0]==board[1] and board[0]==board[2])):
            return board[0]
        if board[8]!=0 and ((board[8]==board[6] and board[8]==board[7]) or (board[8]==board[2] and board[8]==board[5])):
            return board[8]
        if board[0]!=0 and board[1]!=0 and board[2]!=0 and board[3]!=0 and board[4]!=0 and board[5]!=0 and board[6]!=0 and board[7]!=0 and board[8]!=0:
            return "-"
        return 0
    def makeMove(self,x,piece):
            if(self.board[x]==0):
                self.board[x]=piece
                return 1
            self.STATE=piece*-1
            return 0
    def print(self,visible):
        if(visible):
            board=self.board
            print()
            print("  1 2 3")
            print("1 "+self.piece(0)+" "+self.piece(1)+" "+self.piece(2))
            print("2 "+self.piece(3)+" "+self.piece(4)+" "+self.piece(5))
            print("3 "+self.piece(6)+" "+self.piece(7)+" "+self.piece(8))
    def piece(self,x):
        if(self.board[x]==0):
            return " "
        if(self.board[x]==-1):
            return "O"
        return "X"

class AI:
    def __init__(self):
        self.W1 = np.random.uniform(-1,1,size=(36, 9))
        self.H1 = np.zeros(36)
        self.W2 = np.random.uniform(-1,1,size=(36, 36))
        self.H2 = np.zeros(36)
        self.W3 = np.random.uniform(-1,1,size=(9, 36))
        self.out= np.zeros(9)
        self.numWins=0
    def move(self,board,piece):
        for y in range (36):
            hold=0
            for x in range (9):
                hold+=board.board[x]*self.W1[y][x]
            self.H1[y]=hold
        for y in range (36):
            hold=0
            for x in range (36):
                hold+=self.H1[x]*self.W2[y][x]
            self.H2[y]=hold
        for y in range (9):
            if board.board[y]==0:
                hold=0
                for x in range (36):
                    hold+=self.H2[x]*self.W3[y][x]
                self.out[y]=hold
            else:
                self.out[y]=-999
        return board.makeMove(np.where(self.out == np.amax(self.out))[0][0],piece)
    def rebreed(self,mom,dad):
        for y in range (36):
            for x in range (9):
                self.W1[y][x]=self.val(mom.W1[y][x],dad.W1[y][x])
        for y in range (36):
            for x in range (36):
                self.W2[y][x]=self.val(mom.W2[y][x],dad.W2[y][x])
        for y in range (9):
            for x in range (36):
                self.W3[y][x]=self.val(mom.W3[y][x],dad.W3[y][x])
    def val(self,x,y):
        if random.uniform(0,1)<mutationRate:
            return random.uniform(-1,1)
        if random.uniform(0,1)>0.5:
            return x
        return y

class Player:
    def __init__(self):
        self.numWins=0
    def move(self,board,piece):
        uinput=0
        while int(uinput/10)<1 or int(uinput/10)>3 or uinput%10<1 or uinput%10>3:
                uinput=int(input('Player: '))
        return board.makeMove((int(uinput/10)-1)*3+((uinput%10)-1),piece)

class Rand:
    def move(self,board,piece):
        while 1:
            x=random.randint(0,8)
            if(board.board[x]==0):
                board.makeMove(x,piece)
                return 1

class Minimax:
    def __init__(self):
        board=Board() 
        self.minimaxDict={}
        self.initDict(board,1)
    def initDict(self,board,piece):
        if board.state()!=0:
            return
        delete,self.minimaxDict[self.keyify(board)] = minimax(board,piece)
        for x in range (9):
            if board.board[x]==0:
                board.board[x]=piece
                self.initDict(board,piece*-1)
                board.board[x]=0
    def move(self,board,piece):
        board.makeMove(self.minimaxDict[self.keyify(board)],piece)
    def keyify(self,board):
        out=""
        for x in range (9):
            out+=str(board.board[x])
        return out


#custom minimax algorithm
def minimax(board,piece):
    state=board.state()
    if state!=0:
        if state=='-':
            return 0,0
        return state,0

    bestSpot=0
    if piece==1:
        bestValue=-2
        for x in range(9):
            if board.board[x]==0:
                board.board[x]=1
                currValue,delete=minimax(board,-1)
                board.board[x]=0
                if currValue>bestValue:
                    bestValue=currValue
                    bestSpot=x
    else:
        bestValue=2
        for x in range(9):
            if board.board[x]==0:
                board.board[x]=-1
                currValue,delete=minimax(board,1)
                board.board[x]=0
                if currValue<bestValue:
                    bestValue=currValue
                    bestSpot=x
    return bestValue,bestSpot

class Hybrid:
    def move(self,board,piece):
        if random.uniform(0,10)>=difficulty/10:
            rand.move(board,piece)
        else:
            minimax.move(board,piece)

def playGame(P1,P2,visible):
    board=Board()
    if random.randint(1,2)==1:
        while board.state()==0:
            P1.move(board,1)
            board.print(visible)
            if(board.state()==0):
                P2.move(board,-1)
                board.print(visible)
        if board.state()=="-":
            P1.numWins+=1
        elif board.state()!=-1:
            P1.numWins+=1
    else:
        while board.state()==0:
            P2.move(board,1)
            board.print(visible)
            if(board.state()==0):
                P1.move(board,-1)
                board.print(visible)
        if board.state()=="-":
            P1.numWins+=1
        elif board.state()!=1:
            P1.numWins+=1

rand=Rand()
player=Player()
minimax=Minimax()
hybrid=Hybrid()

population=[]
for x in range (100):
    population.append(AI())
mutationRate=0.001
numGames=1
epochs=0
difficulty=0
difficultyMilestone=5

%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('classic')
xAxis = [3000,0,0]
yAxis = [100,100,0]

while(difficulty<95):
    epochs+=1
    for net in range (100):
        for game in range (numGames):
            playGame(population[net],hybrid,0)
                
    population.sort(key=lambda x: x.numWins, reverse=True)
    if(numGames>5+(difficulty/20)):
        difficulty+=5
        numGames=1

    if epochs%10==0:
        mean=0
        for net in population:
            mean+=net.numWins
        xAxis.append(epochs)
        yAxis.append(mean/numGames)
        print("GENERATION: "+str(epochs).zfill(5)+"   Difficulty: "+str(difficulty).zfill(2)+"   NumGames: "+"{:.0f}".format(numGames).zfill(2)+"   lastSaved: "+"{:.1f}".format(population[29].numWins).zfill(4)+"   MEAN: "+"{:.2f}".format(mean/numGames))
    
    if(difficulty==difficultyMilestone):
        plt.plot(xAxis,yAxis)
        plt.xlabel("epoch")
        plt.ylabel("Mean")
        plt.title("Results")
        plt.show()
        difficultyMilestone+=5
    
    if population[30].numWins>=numGames*0.9:
        numGames+=1
        if(epochs%10!=0):
            epochs-=1
    else:
        your_sliced_list = population[30:]
        random.shuffle(your_sliced_list)
        population[30:] = your_sliced_list
        for x in range (50,100):
            population[x].rebreed(population[random.randint(0,49)],population[random.randint(0,49)])
    
    for net in population:
        net.numWins=0

print("done training, finding best opponent")

for net in range (100):
        for game in range (1000):
            playGame(population[net],minimax,0)
population.sort(key=lambda x: x.numWins, reverse=True)

while 1:
    playGame(population[0],player,1)
