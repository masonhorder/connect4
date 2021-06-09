import os
import copy 
import numpy as np

board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],]

# find what row to place the marker at
def getRow(column, inputRow, inputBoard):
  if inputRow < 0:
    return None # return an error if the marker cannot be place in this column
  if inputBoard[inputRow][column] == 0:
    return inputRow # return the correct row to place marker
  else: 
    return getRow(column, inputRow-1, inputBoard) # move on to check the next available row




def printBoard():
  print("")
  for row in board:
    rowString = " \033[93m| "
    for spot in row:
      if spot == 0:
        rowString += "\033[90mO "

      elif spot == 1:
        rowString += "\033[91m* "

      elif spot == 2:
        rowString += "\033[94m* "

    rowString += "\033[93m| "
      
    print(rowString)
  
  print("\033[93m-------------------\033[0m")



def getGameStatus(inputBoard):
  gameStatus = 0 # 0 = active game; 1 = player 1 wins; 2 = player 2 wins; 3 = tie game




  # check if game is tie
  hasZero = False
  for row in inputBoard:
    for column in row:
      if column == 0:
        hasZero = True
  
  if hasZero == False:
    gameStatus = 3
    return gameStatus

  
  # check for horizontal win
  for row in inputBoard:
    previousColumn = 0
    streak = 1
    for column in row:
      if column == previousColumn:
        if column != 0:
          streak += 1
        if streak == 4: 
          return column
      else:
        streak = 1
        previousColumn = column


  # check for vertical wins
  for column in range(7):
    previousColumn = 0
    streak = 1
    for row in range(6):
      if inputBoard[row][column] == previousColumn:
        if inputBoard[row][column] != 0:
          streak += 1
        if streak == 4: 
          return inputBoard[row][column]
          
      else:
        streak = 1
        previousColumn = inputBoard[row][column]


  # check for diagonal wins
  for column in range(7):
    diagonalListRight = []
    diagonalListLeft = []
    row = 0
    newColumn = column
    canContinue = True
    while canContinue:
      if newColumn < 7 and row < 6:
        canContinue = True
        diagonalListRight.append(inputBoard[row][newColumn])
        row+=1
        newColumn+=1
      else:
        canContinue = False

    
    row = 0
    newColumn = column
    canContinue = True
    while canContinue:
      if newColumn >= 0 and row < 6:
        canContinue = True
        diagonalListLeft.append(inputBoard[row][newColumn])
        row+=1
        newColumn-=1
      else:
        canContinue = False

    
    def detectList(diagonalList):
      previousSpot = 0
      streak = 1
      for spot in diagonalList:
        if spot == previousSpot:
          if spot != 0:
            streak += 1
          if streak == 4: 
            return spot
        else:
          streak = 1
          previousSpot = spot
      
      return 0

    
    if detectList(diagonalListRight) == 1 or detectList(diagonalListRight) == 2:
      return detectList(diagonalListRight)
    if detectList(diagonalListLeft) == 1 or detectList(diagonalListLeft) == 2:
      return detectList(diagonalListLeft)



          


  return gameStatus #no one has won or tied


def botWinning(inputBoard):
  if getGameStatus(inputBoard) == 2:
    return 1000
  else:
    return 0

def isCenterColumn(column):
  if column == 3:
    return 2
  elif column >= 2 and column <= 4:
    return 1
  else:
    return 0

def getScore(inputBoard, column):

  score = 0
  newBoard = copy.deepcopy(inputBoard)
  if getRow(column, 5, inputBoard) == None:
    return None
  else:
    newBoard[getRow(column, 5, inputBoard)][column] = 2
  

  # 1000 for winning
  score += botWinning(inputBoard)

  # 6 for a 3 in a row
  # score += 

  # 3 for a 2 in a row


  # 2 for a center column
  # 1 inner 3 columns
  score += isCenterColumn(column)


  # -100 winnable 3
  return score

def placeMarker(player, message):
  os.system('clear')
  print(message)

  gameStatus = getGameStatus(board) # check if the game has been won or tied
  
  if gameStatus == 1:
    os.system('clear')
    printBoard()
    print("\033[91mcongrats player 1 won!\033[0m")
    return None
  
  elif gameStatus == 2:
    os.system('clear')
    printBoard()
    print("\033[94mcongrats player 2 won!\033[0m")
    return None
  
  elif gameStatus == 3:
    os.system('clear')
    printBoard()
    print("tie :(")
    return None



  newPlayer = 0
  column = 0

  if player == 1:
    printBoard()
    columnRaw = raw_input("Player " + str(player) + " choose a column(1-7): ")
    try:
      if int(columnRaw) > 7:
        placeMarker(player, "\033[91mColumn between 1 and 7\033[0m")
      elif int(columnRaw) < 1:
        placeMarker(player, "\033[91mColumn between 1 and 7\033[0m")
      else:
        column = int(columnRaw)
    except:
      placeMarker(player)


  else:
    scores = []
    for columnOption in range(7):
      scores.append(getScore(board, columnOption))

    highScore = scores[0]
    highScoreLocation = 0
    index = 0
    for score in scores:
      if score > highScore:
        highScore = score
        highScoreLocation = index
      elif score == highScore:
        highScoreLocation = index
      index+=1
      column = highScoreLocation + 1


  

  
  row = getRow(column-1, 5, board) # start checking for the row
  if row == None:
    placeMarker(player, "\033[91mColumn Already Fully Occupied, Go Again\033[0m") # restart trun as current player


  board[row][column-1] = player # place the marker


  # find next player
  if player == 2:
    newPlayer = 1
  else:
    newPlayer = 2
  placeMarker(newPlayer, "")





placeMarker(1, "\033[93mWelcome to connect four, two player edition\033[0m") # starts game