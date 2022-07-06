/*
connect 4 game against AI, using minimax algorithm
used research for understanding minimax, all code designed by me
V1.1 updates: board is now an object to store more data, including its score
score is stored for the board so it can be updated with piece placement instead of recalculated
fully every time
Alexander Breeze, 2021
*/
package com.company;
import java.util.Scanner;

public class Main {
    //custom minimax algorithm
    public int minimax(Board board, boolean maxi, int depth){
            if (depth==0 || board.score==9999 || board.score==-9999){
                return board.score;
            }

            int oldScore=board.score;
            int currValue,bestValue;
            if (maxi){
                bestValue=-999999;
                for (int x=0;x<7;x++){
                    if (board.board[5][x]==' '){
                        board.placePiece(x,'O');
                        currValue=minimax(board,false,depth-1);
                        board.removePiece(x, oldScore);
                        if (currValue>bestValue){
                            bestValue=currValue;
                        }
                    }
                }
            }
            else{
                bestValue=999999;
                for (int x=0;x<7;x++){
                    if (board.board[5][x]==' '){
                        board.placePiece(x,'X');
                        currValue=minimax(board,true,depth-1);
                        board.removePiece(x, oldScore);
                        if (currValue<bestValue){
                            bestValue=currValue;
                        }
                    }
                }
            }
            return bestValue;
    }

    public static int getInput(Board board){
        Scanner scan = new Scanner(System.in);
        int uinput=-5;
        while (uinput<0 || uinput>6 || board.stack[uinput]==6){
            uinput=scan.nextInt()-1;
            if (uinput<0){
                java.lang.System.exit(0); //to crash game if bored
            }
        }
        return uinput;
    }

    public static void main(String[] args) {
        Board board = new Board();
        while (board.score<9999 && board.score>-9999){
            board.print();
            System.out.println(board.score);
            board.placePiece(getInput(board),'X');

            if (board.score<9999 && board.score>-9999){
                board.print();
                System.out.println(board.score);
                board.placePiece(getInput(board),'O');

                /*bestValue=-999999
                currValue=0
                bestSlot=-1
                for x in range(7):
                if boardStack[x]!=6:
                placePiece(board,boardStack,x,"O")
                currValue=minimax(board,boardStack,False,8)
                removePiece(board,boardStack,x)
                if currValue>bestValue:
                bestValue=currValue
                bestSlot=x
                placePiece(board,boardStack,bestSlot,"O")
                state=boardState(board)*/
            }
        }
        board.print();
        if (board.score==-9999){
            System.out.println("YOU WIN!");
        }
        else if (board.score==9999){
            System.out.println("YOU LOSE!");
        }
        else{
            System.out.println("TIE!");
        }
    }
}