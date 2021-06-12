import os
import copy 
import numpy as np
from math import inf as infinity
from datetime import datetime
import time
import random


board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],]

humanMoves = []

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
  

def getValidMoves(inputBoard):
  validMoves = []
  for column in range(7):
    if getRow(column, 5, inputBoard) != None:
      validMoves.append([getRow(column, 5, inputBoard), column])

  return validMoves

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
      

     
def evaluateSection(section):
  score = 0

  if section.count(2) == 4: # bot winning
    score += 10000

  elif section.count(1) == 3 and section.count(0) == 1: # human being set up to win
    score -= 20

  elif section.count(2) == 3 and section.count(0) == 1:
    score += 8

  elif section.count(2) == 2 and section.count(0) == 2:
    score += 3

  return score

def getScore(inputBoard):
  score = 0

  # Score center column
  centerColumnArray = []
  for row in inputBoard:
    centerColumnArray.append(row[3])

  score += centerColumnArray.count(2) * 3

  for column in range(7):
    columnArray = []
    for rowList in inputBoard:
      columnArray.append(rowList[column])
    for row in range(6-3):
      section = columnArray[row:row+4]
      score += evaluateSection(section)
      
  for row in inputBoard:
    for column in range(7-3):
      section = row[column:column+4]
      score += evaluateSection(section)

  for r in range(6-3):
    for c in range(7-3):
      section = [inputBoard[r+i][c+i] for i in range(4)]
      score += evaluateSection(section)

  for r in range(6-3):
    for c in range(7-3):
      section = [inputBoard[r+3-i][c+i] for i in range(4)]
      score += evaluateSection(section)

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


def getDepth(inputBoard):
  movesLeft = -1
  for row in inputBoard:
    for spot in row:
      if spot == 0:
        movesLeft +=1

  return movesLeft


def minimax(inputBoard, player, depth, alpha, beta):
  if player == 2:
    best = [None, None, -infinity]
  else:
    best = [None, None, +infinity]

  if getGameStatus(inputBoard) != 0:
    if getGameStatus(inputBoard) == 3:
      return [None, None, 0]
    elif getGameStatus(inputBoard) == 2:
      return [None, None, 10000000000000]
    elif getGameStatus(inputBoard) == 2:
      return [None, None, -10000000000000]
  
  if depth == 0:
    return [None, None, getScore(inputBoard)]

  for move in getValidMoves(inputBoard):
    newBoard = copy.deepcopy(inputBoard)
    newBoard[move[0]][move[1]] = player
    score = minimax(newBoard, nextPlayer(player), depth-1, alpha, beta)
    score[0], score[1] = move[0], move[1]

    if player == 2:
      if score[2] > best[2]:
        best = score
      alpha = max(alpha, score[2])
      if alpha >= beta:
        break


    else:
      if score[2] < best[2]:
        best = score
      beta = min(beta, score[2])
      if alpha >= beta:
        break

  return best





#####################
### MAIN FUNCTION ###
#####################
def makeMove(player, message):

  # os.system('clear')
  print(message)
  message = ""
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
    
    humanMoves.append(column+1)

  # bots turn to move
  if player == 2:
    startTime = time.time()
  
    move = minimax(board, 2, 5, -infinity, infinity)
    endTime = time.time()
    print("time to make move(seconds):" + str(endTime-startTime))
    # getDepth(board)
    row = move[0]
    column = move[1]
    message = "Bot went in column " + str(column)


  board[row][column] = player
  makeMove(nextPlayer(player), message)
  

makeMove(1, "\033[93mWelcome to connect four, single player edition\033[0m")

print("you played these moves: " + str(humanMoves))
