#connect 4 game against AI, using minimax algorithm
#used research for understanding minimax, all code designed by me
#pretty slow, should've done it in C/C++ because idk how to optimise code in python (no "inline" and such)
#Alexander Breeze 


#custom minimax algorithm
def minimax(board,boardStack,maxi,depth):
    state=boardState(board)
    if depth==0 or state==9999 or state==-9999:
        return boardState(board)
    
    if maxi:
        bestValue=-999999
        for x in range(7):
            if(board[5][x]==" "):
                placePiece(board,boardStack,x,"O")
                currValue=minimax(board,boardStack,False,depth-1)
                removePiece(board,boardStack,x)
                if currValue>bestValue:
                    bestValue=currValue
    else:
        bestValue=999999
        for x in range(7):
            if(board[5][x]==" "):
                placePiece(board,boardStack,x,"X")
                currValue=minimax(board,boardStack,True,depth-1)
                removePiece(board,boardStack,x)
                if currValue<bestValue:
                    bestValue=currValue
    return bestValue

#gets input, keeps trying for valid input
def getInput(board,boardStack):
    uinput=-5
    while uinput<0 or uinput>6 or boardStack[int(uinput)]==6:
        uinput=int(input('Move: '))-1
        if uinput<0:#to end game
            exit(0)
    return uinput

#places piece on board
def placePiece(board,boardStack,slot,piece):
    board[boardStack[slot]][slot]=piece
    boardStack[slot]+=1

#removes piece from the board
def removePiece(board,boardStack,slot):
    boardStack[slot]-=1
    board[boardStack[slot]][slot]=" "

#finds out if anyone has won/tied(-)
def boardState(board): #69 calls to evalWin
    score=0
    #check verticals
    for y in range(3):
        for x in range(7):
            score+=evalWin([board[y][x],board[y+1][x],board[y+2][x],board[y+3][x]])
    
    #check horizontals
    for y in range(6):
        for x in range(4):
            score+=evalWin([board[y][x],board[y][x+1],board[y][x+2],board[y][x+3]])

    #check diagonals
    for y in range(3):
        for x in range(4):
            score+=evalWin([board[y][x],board[y+1][x+1],board[y+2][x+2],board[y+3][x+3]])
    for y in range(3):
        for x in range(4):
            score+=evalWin([board[5-y][x],board[4-y][x+1],board[3-y][x+2],board[2-y][x+3]])

    #check for victories, then return score
    if score>9999:return 9999
    if score<-9999:return -9999
    return score

#returns if a certain 4 slots contain only air and one type of tile
# "X XX"=-3,  "OXOO"=0, "O  O"=2
evalWinArr=[-99999,-10,-1,0,0,0,1,10,99999]  #global to reduce lag hopefully
def evalWin(chars):
    score=0
    goodChar=""
    for x in range(4):
        if chars[x]=="X":
            if goodChar=="O":
                return 0
            goodChar="X"
            score-=1
        elif chars[x]=="O":
            if goodChar=="X":
                return 0
            goodChar="O"
            score+=1
    return evalWinArr[score+4]

#prints the board
def printBoard(board):
    print()
    print("1 2 3 4 5 6 7")
    for y in range(5,-1,-1):
        out=""
        for x in range(7):
            out+=board[y][x]+"|"
        print(out[:13])

#Main function that runs the game
#Note: player is always X because no point making it work for O also
def main():
    board=[[" "," "," "," "," "," "," "],[" "," "," "," "," "," "," "],[" "," "," "," "," "," "," "],
    [" "," "," "," "," "," "," "],[" "," "," "," "," "," "," "],[" "," "," "," "," "," "," "]]
    boardStack=[0,0,0,0,0,0,0]
    state=0;
    
    while state<9999 and state>-9999:
        printBoard(board)
        print(state)
        placePiece(board,boardStack,getInput(board,boardStack),"X")
        state=boardState(board)
        
        if state<9999 and state>-9999:
            bestValue=-999999
            currValue=0
            bestSlot=-1
            for x in range(7):
                if boardStack[x]!=6:
                    placePiece(board,boardStack,x,"O")
                    currValue=minimax(board,boardStack,False,5)
                    removePiece(board,boardStack,x)
                    if currValue>bestValue:
                        bestValue=currValue
                        bestSlot=x
            placePiece(board,boardStack,bestSlot,"O")
            state=boardState(board)
    
    printBoard(board)
    if state==-9999:
        print("YOU WIN!")
    elif state==9999:
        print("YOU LOSE!")
    else:
        print("TIE!")

main()