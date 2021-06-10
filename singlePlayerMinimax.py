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
          streakLength += 1
          
      else:
        streak = 1
        previousColumn = inputBoard[row][column]


  # TODO: CONDENSE BELOW CODE

  # check for diagonal wins top down
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



  # check for diagonal wins bottom up
  for column in range(7):
    diagonalListRight = []
    diagonalListLeft = []
    row = 5
    newColumn = column
    canContinue = True
    while canContinue:
      if newColumn < 7 and row > 0:
        canContinue = True
        diagonalListRight.append(inputBoard[row][newColumn])
        row-=1
        newColumn+=1
      else:
        canContinue = False

    


    row = 5
    newColumn = column
    canContinue = True
    while canContinue:
      if newColumn >= 0 and row > 0:
        canContinue = True
        diagonalListLeft.append(inputBoard[row][newColumn])
        row-=1
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
          

# check the state of the game
def getGameStatus(inputBoard):
  if isBoardFull(inputBoard):
    return 3

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
  rawColumn = raw_input("Choose a column: ")
  try:
    if int(columnRaw) > 7:
      placeMarker(player, "\033[91mColumn between 1 and 7\033[0m")
    elif int(columnRaw) < 1:
      placeMarker(player, "\033[91mColumn between 1 and 7\033[0m")
    else:
      column = int(columnRaw)
  except:
    placeMarker(1)

  return column

def nextPlayer(player):
  if player == 1:
    return 2
  else:
    return 1




#####################
### MAIN FUNCTION ###
#####################
def makeMove(player):

  # check if anyone is currently winning
  getGameStatus(inputBoard)

  # humans turn to move
  if player == 1:
    column = askPlayerColumn()
    row = getRow(column, 5, board)

    # verify row is not full
    if row == None:
      placeMarker(1)
    baord[row][column] = 1

  # bots turn to move
  if player == 2:

  baord[row][column] = 1
  makeMove(nextPlayer(player))

