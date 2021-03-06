import os
import copy 
import numpy as np


board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],]


# check to make sure the board is not full
def isBoardFull(inputBoard):
  hasZero = False
  for row in inputBoard:
    for column in row:
      if column == 0:
        hasZero = True
  if hasZero:
    return False
  else: 
    return True
  
# check for a streak at a certain length
def getStreak(inputBoard, streakLength, player):
  streakCount = 0
  # check for horizontal streak
  for row in inputBoard:
    previousColumn = 0
    streak = 1
    for column in row:
      if column == previousColumn:
        if column == player:
          streak += 1
        if streak == streakLength: 
          streakCount += 1
      else:
        streak = 1
        previousColumn = column

  # check for vertical streak
  for column in range(7):
    previousColumn = 0
    streak = 1
    for row in range(6):
      if inputBoard[row][column] == previousColumn:
        if inputBoard[row][column] == player:
          streak += 1
        if streak == streakLength: 
          streakCount += 1
          
      else:
        streak = 1
        previousColumn = inputBoard[row][column]


  for rowStatus in range(2):
    if rowStatus == 0:
      startRow = 5
      additionAmount = -1
    else:
      startRow = 0
      additionAmount = 1

    for column in range(7):
      diagonalListRight = []
      diagonalListLeft = []
      row = startRow
      newColumn = column
      canContinue = True
      while canContinue:
        if newColumn < 7 and row < 6 and row > -1 and newColumn > -1:
          canContinue = True
          diagonalListLeft.append(inputBoard[row][newColumn])
          row+=additionAmount
          newColumn+=1
        else:
          canContinue = False

      row = startRow
      newColumn = column
      canContinue = True
      while canContinue:
        if newColumn < 7 and row < 6 and row > -1 and newColumn > -1:
          canContinue = True
          diagonalListRight.append(inputBoard[row][newColumn])
          row+=additionAmount
          newColumn-=1
        else:
          canContinue = False

      
      def detectStreakInList(diagonalList, streakLength, player):
        streakCount = 0
        previousSpot = 0
        streak = 1
        for spot in diagonalList:
          if spot == previousSpot:
            if spot == player:
              streak += 1
            if streak == streakLength: 
              streakCount += 1
          else:
            streak = 1
            previousSpot = spot
        return streakCount
        
      streakCount += detectStreakInList(diagonalListLeft, streakLength, player)
      streakCount += detectStreakInList(diagonalListRight, streakLength, player)

  return streakCount
      

     



def getScore(inputBoard, column, inverseBoard):
  score = 0

  if column == 3:
    score += 3
  elif column == 2 or column == 4:
    score += 1
  
  # score is a win for bot or blocks opponent
  win = 0
  currentSetStreak = 4
  while currentSetStreak <= 7:
    if getStreak(inverseBoard, currentSetStreak, 1) > 0:
      win = 1
    if getStreak(inputBoard, currentSetStreak, 2) > 0:
      win = 2
    currentSetStreak += 1

  if win == 1:
    score += 100
  elif win == 2:
    score +=1000

  score+=getStreak(inputBoard, 3, 2)*6
  score+=getStreak(inverseBoard, 3, 1)*4
  score+=getStreak(inputBoard, 2, 2)*3
  score+=getStreak(inverseBoard, 3, 1)*1

  return score




          

# check the state of the game
def getGameStatus(inputBoard):
  if isBoardFull(inputBoard):
    return 3
  
  currentSetStreak = 4
  while currentSetStreak <= 7:
    if getStreak(inputBoard, currentSetStreak, 1) > 0:
      return 1
    if getStreak(inputBoard, currentSetStreak, 2) > 0:
      return 2
    currentSetStreak += 1

  return 0

# print out the connect 4 board in a nice style
def printBoard():
  print("")
  print("   1 2 3 4 5 6 7")
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

def getRow(column, inputRow, inputBoard):
  if inputRow < 0:
    return None # return an error if the marker cannot be place in this column
  if inputBoard[inputRow][column] == 0:
    return inputRow # return the correct row to place marker
  else: 
    return getRow(column, inputRow-1, inputBoard) # move on to check the next available row

# get player 1 move location
def askPlayerColumn():
  rawColumn = input("Choose a column: ")
  try:
    if int(rawColumn) > 7:
      makeMove(1, "\033[91mColumn between 1 and 7\033[0m")
    elif int(rawColumn) < 1:
      makeMove(1, "\033[91mColumn between 1 and 7\033[0m")
    else:
      column = int(rawColumn)
  except:
    makeMove(1, "\033[91mError interpretting\033[0m")

  return column - 1

def nextPlayer(player):
  if player == 1:
    return 2
  else:
    return 1




#####################
### MAIN FUNCTION ###
#####################
def makeMove(player, message):

  # check if anyone is currently winning
  os.system('clear')

  print(message)

  gameStatus = getGameStatus(board)
  if gameStatus == 1:
    os.system('clear')
    printBoard()
    print("\033[91mcongrats player 1 won!\033[0m")
    return None
  
  elif gameStatus == 2:
    os.system('clear')
    printBoard()
    print("\033[94mLOSER!!! player 2 beat you!\033[0m")
    return None
  
  elif gameStatus == 3:
    os.system('clear')
    printBoard()
    print("tie :(")
    return None
  

  # humans turn to move
  if player == 1:
    printBoard()
    column = askPlayerColumn()
    row = getRow(column, 5, board)

    # verify row is not full
    if row == None:
      makeMove(1, "\033[91mColumn Already Fully Occupied, Go Again\033[0m")

  # bots turn to move
  if player == 2:
    highestScore = -100000000000000000
    highestScoreLocation = 0
    for potentialColumn in range(7):
      potentialRow = getRow(potentialColumn, 5, board)
      if potentialRow != None:
        newBoard = copy.deepcopy(board)
        newBoard[potentialRow][potentialColumn] = 2
        inverseBoard = copy.deepcopy(board)
        inverseBoard[potentialRow][potentialColumn] = 1


        newScore = getScore(newBoard, potentialColumn, inverseBoard)
        if newScore > highestScore:
          highestScore = newScore
          highestScoreLocation = potentialColumn
    column = highestScoreLocation
    row = getRow(highestScoreLocation, 5, board)

        

  
  board[row][column] = player
  makeMove(nextPlayer(player), "")

makeMove(1, "\033[93mWelcome to connect four, single player edition\033[0m")