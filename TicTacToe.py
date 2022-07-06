#tictactoe game against AI, using minimax algorithm
#used research for understanding minimax, all code designed by me
#Alexander Breeze 


#custom minimax algorithm
def minimax(board,maxi):
    state=boardState(board)
    if state!=" ":
        if state=="X":
            return -1
        if state=="O":
            return 1
        return 0
    
    if maxi:
        bestValue=-2
        for y in range(3):
            for x in range(3):
                if(board[y][x]==" "):
                    board[y][x]="O"
                    currValue=minimax(board,False)
                    board[y][x]=" "
                    if currValue>bestValue:
                        bestValue=currValue
    else:
        bestValue=2
        for y in range(3):
            for x in range(3):
                if(board[y][x]==" "):
                    board[y][x]="X"
                    currValue=minimax(board,True)
                    board[y][x]=" "
                    if currValue<bestValue:
                        bestValue=currValue
    return bestValue

#gets input, keeps trying for valid input
def getInput(board):
	uinput=0
	while int(uinput/10)<1 or int(uinput/10)>3 or uinput%10<1 or uinput%10>3 or board[int(uinput/10)-1][(uinput%10)-1]!=" ":
		uinput=int(input('Player X: (ex. "13")  '))
	board[int(uinput/10)-1][(uinput%10)-1]="X"

#finds out if anyone has won/tied(-)
def boardState(board):
    if board[1][1]!=" " and ((board[1][1]==board[0][0] and board[1][1]==board[2][2]) or (board[1][1]==board[2][0] and board[1][1]==board[0][2]) or 
    (board[1][1]==board[1][0] and board[1][1]==board[1][2]) or (board[1][1]==board[0][1] and board[1][1]==board[2][1])):
        return board[1][1]
    if board[0][0]!=" " and ((board[0][0]==board[1][0] and board[0][0]==board[2][0]) or (board[0][0]==board[0][1] and board[0][0]==board[0][2])):
        return board[0][0]
    if board[2][2]!=" " and ((board[2][2]==board[2][0] and board[2][2]==board[2][1]) or (board[2][2]==board[0][2] and board[2][2]==board[1][2])):
        return board[2][2]
    if board[0][0]!=" " and board[0][1]!=" " and board[0][2]!=" " and board[1][0]!=" " and board[1][1]!=" " and board[1][2]!=" " and board[2][0]!=" " and board[2][1]!=" " and board[2][2]!=" ":
        return "-"
    return " "

#prints the board
def printBoard(board):
    print()
    print("  1 2 3")
    print("1 "+board[0][0]+" "+board[0][1]+" "+board[0][2])
    print("2 "+board[1][0]+" "+board[1][1]+" "+board[1][2])
    print("3 "+board[2][0]+" "+board[2][1]+" "+board[2][2])

#Main function that runs the game
#Note: player is always X because no point making it work for O also
def main():
    board=[[" "," "," "],[" "," "," "],[" "," "," "]]
    while boardState(board)==" ":
        printBoard(board)
        getInput(board)
        
        if boardState(board)==" ":   #want to maximise
            bestSpot=[0,0]
            bestValue=-2
            for y in range(3):
                for x in range(3):
                    if(board[y][x]==" "):
                        board[y][x]="O"
                        currValue=minimax(board,False)
                        print(currValue)
                        board[y][x]=" "
                        if currValue>bestValue:
                            bestValue=currValue
                            bestSpot=[y,x]
            board[bestSpot[0]][bestSpot[1]]="O"
    
    printBoard(board)
    if boardState(board)=="X":
        print("YOU WIN!")
    elif boardState(board)=="O":
        print("YOU LOSE!")
    else:
        print("TIE!")

main()