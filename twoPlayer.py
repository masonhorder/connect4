board = [[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],]

def printBoard():
  for row in board:
    print(row)

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

  


  return gameStatus #no one has won or tied
        



def placeMarker(player):
  gameStatus = getGameStatus() # check if the game has been won or tied
  
  if gameStatus == 1:
    print("congrats player 1 won!")
    return None
  
  elif gameStatus == 2:
    print("congrats player 2 won!")
    return None
  
  elif gameStatus == 3:
    print("tie :(")
    return None

  printBoard()
  newPlayer = 0
  column = int(input("Player " + str(player) + " choose a column(1-7): "))

  # find what height to place the marker at
  def getHeightOfColumn(column, inputHeight):
    if board[inputHeight][column] == 0:
      if inputHeight < 0:
        return None # return an error if the marker cannot be place in this column
      else:
        print("returning height")
        print(inputHeight)
        return inputHeight # return the correct height to place marker
    else: 
      getHeightOfColumn(column, inputHeight-1) # move on to check the next available height
  
  height = getHeightOfColumn(column-1, 5) # start checking for the height

  if height == None:
    print("Column Already Fully Occupied")
    placeMarker(player) # restart trun as current player


  board[height][column-1] = player # place the marker


  # find next player
  if player == 2:
    newPlayer = 1
  else:
    newPlayer = 2
  placeMarker(newPlayer)





print("Welcome to connect four, two player edition")
placeMarker(1) # starts game