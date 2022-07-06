package com.company;
import java.util.HashMap;

public class Board {
    char [][] board={{' ',' ',' ',' ',' ',' ',' '},{' ',' ',' ',' ',' ',' ',' '},{' ',' ',' ',' ',' ',' ',' '},
            {' ',' ',' ',' ',' ',' ',' '},{' ',' ',' ',' ',' ',' ',' '},{' ',' ',' ',' ',' ',' ',' '}};
    int [] stack={0,0,0,0,0,0,0};   //records height of every column on board
    int score=0;
    HashMap<String, Integer> evalPieceX = new HashMap<String, Integer>();
    HashMap<String, Integer> evalPieceO = new HashMap<String, Integer>();
    public void Main(){
        char[] bank={'O','X',' '};
        char[] temp={' ',' ',' '};
        int tempScore;
        char goodChar;
        int[] values={-99999,-10,-1,0,0,0,1,10,99999};
        for (int x=0;x<3;x++){
            for (int y=0;y<3;y++){
                for (int z=0;z<3;z++){
                    for (int a=0;a<3;a++){
                        temp[0]=bank[x];
                        temp[1]=bank[y];
                        temp[2]=bank[z];
                        temp[3]=bank[a];
                        tempScore=0;
                        goodChar=' ';

                        for (int b=0;b<4;b++){
                            if (temp[b]=='X'){
                                if (goodChar=='O'){
                                    evalWinArr.put(,0)
                                }
                            }
                        }

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
                    }
                }
            }
        }
    }


    public void placePiece(int slot, char piece){
        board[stack[slot]][slot]=piece;
        score+=scoreInc(slot, stack[slot]);
        stack[slot]+=1;
    }

    public void removePiece(int slot, int oldScore){
        stack[slot]-=1;
        board[stack[slot]][slot]=' ';
        score=oldScore;
    }

    //gets the board score change from a specific piece placement
    public int scoreInc(int slot, int height) {
        int scoreInc=0;
        //16 possible win conditions (4-in-a-rows) containing one slot, but only some are possible based on
        // the slot position. Find which part of the board (of 6) the new piece is in,
        // to know which win conditions to check.  (top/bottom, left/middle/right)
        if (slot<3){
            if(height<3){
                for (int y=0;y<3;y++){
                    for (int x=0;x<7;x++){
                        scoreInc+=evalWin([board[y][x],board[y+1][x],board[y+2][x],board[y+3][x]])
                    }
                }


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
            }
            else{

            }
        }
        else if (slot==3){
            if(height<3){

            }
            else{

            }
        }
        else{
            if(height<3){

            }
            else{

            }
        }

        //check for victories, then return score
        if (score>9999){
            return 9999;
        }
        if (score<-9999){
            return -9999;
        }
        return scoreInc;
    }

    public void print(){
        System.out.println("\n1 2 3 4 5 6 7");
        for(int y=5;y>-1;y--){
            for(int x=0;x<7;x++){
                System.out.print(board[y][x]+"|");
            }
            System.out.println("|");
        }
    }
};