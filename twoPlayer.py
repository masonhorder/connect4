import os

board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],]

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

def getGameStatus():
  gameStatus = 0 # 0 = active game; 1 = player 1 wins; 2 = player 2 wins; 3 = tie game




  # check if game is tie
  hasZero = False
  for row in board:
    for column in row:
      if column == 0:
        hasZero = True
  
  if hasZero == False:
    gameStatus = 3
    return gameStatus

  
  # check for horizontal win
  for row in board:
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
      if board[row][column] == previousColumn:
        if board[row][column] != 0:
          streak += 1
        if streak == 4: 
          return board[row][column]
          
      else:
        streak = 1
        previousColumn = board[row][column]


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
        diagonalListRight.append(board[row][newColumn])
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
        diagonalListLeft.append(board[row][newColumn])
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
        diagonalListRight.append(board[row][newColumn])
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
        diagonalListLeft.append(board[row][newColumn])
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
          


  return gameStatus #no one has won or tied
        



def placeMarker(player):
  gameStatus = getGameStatus() # check if the game has been won or tied
  
  if gameStatus == 1:
    os.system('clear')
    printBoard()
    print("congrats player 1 won!")
    return None
  
  elif gameStatus == 2:
    os.system('clear')
    printBoard()
    print("congrats player 2 won!")
    return None
  
  elif gameStatus == 3:
    os.system('clear')
    printBoard()
    print("tie :(")
    return None



  printBoard()
  newPlayer = 0
  columnRaw = raw_input("Player " + str(player) + " choose a column(1-7): ")
  column = 0
  try:
    if int(columnRaw) > 7:
      placeMarker(player)
    elif int(columnRaw) < 1:
      placeMarker(player)
    else:
      column = int(columnRaw)
  except:
    placeMarker(player)

  # find what row to place the marker at
  def getRow(column, inputRow):
    if inputRow < 0:
      return None # return an error if the marker cannot be place in this column
    if board[inputRow][column] == 0:
      return inputRow # return the correct row to place marker
    else: 
      return getRow(column, inputRow-1) # move on to check the next available row
  
  row = getRow(column-1, 5) # start checking for the row
  if row == None:
    print("Column Already Fully Occupied")
    placeMarker(player) # restart trun as current player


  board[row][column-1] = player # place the marker


  # find next player
  if player == 2:
    newPlayer = 1
  else:
    newPlayer = 2
  placeMarker(newPlayer)





print("Welcome to connect four, two player edition")
placeMarker(1) # starts game