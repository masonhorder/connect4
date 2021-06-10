import os
import copy 
import numpy as np


board = [
  [0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0],
  [0,0,0,0,2,1,1],
  [0,0,0,1,2,2,2],
  [1,0,1,2,1,1,2],
  [2,2,2,1,1,1,2],
]


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



print(getGameStatus(board))