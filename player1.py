import csv
import copy


board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],]


with open("player1.csv", 'w') as file:
  writer = csv.writer(file) 


  def getRow(column, inputRow, inputBoard):
    if inputBoard[inputRow][column] == 0:
      return inputRow # return the correct row to place marker
    else: 
      return getRow(column, inputRow-1, inputBoard)


  def getBoard(inputBoard, player, depth):
    print(depth)
    if depth <= 4:
      for i in range(7):
        newBoard = copy.deepcopy(inputBoard)
        newBoard[getRow(i, 5, newBoard)][i] = player
        writer.writerow([newBoard])
        newPlayer = 0
        if player == 1:
          newPlayer = 2
        else:
          newPlayer = 1    
        getBoard(newBoard, newPlayer, depth+1)
    else:
      return None


  getBoard(board, 1, 1)