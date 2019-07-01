import copy
#import Ai as ai

#KeyError: 1

def copyBoard(board):
  #Create initial copy
  out = copy.deepcopy(board)

  #Make sure objects in board and summon order are the same
  newOrder = copy.deepcopy(board.summonOrder)
  newMyBoard = copy.deepcopy(board.myBoard)
  newOppBoard = copy.deepcopy(board.oppBoard)
  for i in range(len(board.summonOrder)):
    if board.summonOrder[i] in board.myBoard:
      index = board.myBoard.index(board.summonOrder[i])
      replace = copy.deepcopy(board.summonOrder[i])
      replace.game = out
      newMyBoard[index] = replace
    elif board.summonOrder[i] in board.oppBoard:
      index = board.oppBoard.index(board.summonOrder[i])
      replace = copy.deepcopy(board.summonOrder[i])
      replace.game = out
      newOppBoard[index] = replace
    newOrder[i] = replace
  out.summonOrder = newOrder
  out.myBoard = newMyBoard
  out.oppBoard = newOppBoard
      
  #Change game for cards in both hands, and for both players
  out.myHand = copy.deepcopy(out.myHand)
  for i in out.myHand:
    i.game = out
  out.oppHand = copy.deepcopy(out.oppHand)
  for i in out.oppHand:
    i.game = out
  out.me.game = out
  out.opponent.game = out

  return out

def playCards(field):
  newPlays = ['']
  newResults = [field]
  allPlays = []
  allResults = []
  while newResults != []:
    plays = newPlays
    results = newResults
    allPlays.append(plays)
    allResults.append(results)
    newPlays = []
    newResults = []
    for game in results:
      newGame = copyBoard(game)
      i = results.index(game)
      for card in newGame.myHand:
        if 'Target' not in card.effects and newGame.playCard(card):
          newResults.append(newGame)
          newPlays.append(plays[i]+', '+card.name)
        else:
          for target in newGame.summonOrder:
            if newGame.playCard(card,target):
              newResults.append(newGame)
              newPlays.append(plays[i]+', '+card.name+' > '+target.name)
  allPlays.append(newPlays)
  allResults.append(newResults)
  out = {}
  for i in range(len(allPlays)):
    for j in range(len(allPlays[i])):
      out[allPlays[i][j]] = allResults[i][j]
  return out

#Check all results from playCards against the original board and find the one that the algorithm considers best
def checkResults(results,orig,alg):
  print(results.keys())
  algResults = []
  for i in results.values():
    #Take change in hero health values
    dMyHealth = i.me.health - orig.me.health
    dOppHealth = i.opponent.health - orig.opponent.health
    
    #Take change in number of minions on each side
    dMyMinions = len(i.myBoard) - len(orig.myBoard)
    dOppMinions = len(i.oppBoard) - len(orig.oppBoard)

    #Take change in total health of minions on each side
    dMyBoardHealth = sum([minion.health for minion in i.myBoard]) - sum(minion.health for minion in orig.myBoard)
    dOppBoardHealth = sum([minion.health for minion in i.oppBoard]) - sum([minion.health for minion in orig.oppBoard])

    input_fn = lambda:ai.my_input_fn([[dMyHealth],[dOppHealth],[dMyBoardHealth],[dOppBoardHealth],[dMyMinions],[dOppMinions]],[0],num_epochs=1)

    #Pass all values to the algorithm
    algResults.append(alg.predict(input_fn))

  print(algResults)
  i = algResults.index(max(algResults))
  return list(results.keys())[i]

#OLD PLAYCARDS FUNCTION (uses recursion, confusing and limited by python recursion limit)
##def playCards(field,results={},i=0):
##  #On the first iteration, insert a copy of the initial board
##  if i == 0:
##    results[''] = copyBoard(field)
##  #Count the current step in the play
##  i += 1
##  #Create lists of the keys and values from results so that they can be manipulated individually and based on index
##  plays = list(results.keys())
##  boards = list(results.values())
##  #Insert a copy of the previous result to play cards on
##  boards.insert(i,copyBoard(boards[i-1]))
##  plays.insert(i,plays[i-1])
##  boardState = boards[i]
##  #Iterate through cards in hand
##  for c in range(len(boardState.myHand)):
##    try:
##      card = boardState.myHand[c]
##    except IndexError:
##      break
##    #If the card targets a minion, iterate through all possible targets
##    if 'Target' in card.effects:
##      for t in range(len(boardState.summonOrder)):
##        #Verify that variables point to the correct board and card
##        boardState = boards[i]
##        card = boardState.myHand[c]
##        #Select a target; number of targets will not change between iterations of this loop, as the board being used should always be a copy of the previous board
##        target = boardState.summonOrder[t]
##        succ = boardState.playCard(card,target)
##        #If the card is successfully played, process the next played card and setup for next attempted target
##        if succ: 
##          #Add the current card's name to the current dictionary key (the textual representation of this play)
##          if plays[i] == '':
##            plays[i] = card.name+' > '+target.name
##          else:
##            plays[i] += ', '+card.name+' > '+target.name
##          #Create dict out of keys and values and play another card by setting this dict to the output of the next play
##          results = {play:result for play,result in zip(plays,boards)}
##          results = playCards(boardState,results,i)
##          #Setup lists to match the new results dict, then insert another copy of the previous result, which will be the same as it was at the beginning of this loop
##          plays = list(results.keys())
##          boards = list(results.values())
##          boards.insert(i,copyBoard(boards[i-1]))
##          plays.insert(i,plays[i-1])
##    else:
##      #Verify that boardState points to the correct board, then play a card
##      boardState = boards[i]
##      succ = boardState.playCard(card)
##      if succ: 
##        #Add the current card's name to the current dictionary key
##        if plays[i] == '':
##          plays[i] = card.name
##        else:
##          plays[i] += ', '+card.name
##        #Create dict from keys and values and play another card
##        results = {play:result for play,result in zip(plays,boards)}
##        results = playCards(boardState,results,i)
##        #Setup lists to match the new results dict, then insert another copy so that new plays can be created with the next card
##        plays = list(results.keys())
##        boards = list(results.values())
##        boards.insert(i,copyBoard(boards[i-1]))
##        plays.insert(i,plays[i-1])
##  return results
