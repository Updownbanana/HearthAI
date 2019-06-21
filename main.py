'''
TODO:
Write a way to check all possible plays
Code more cards to accelerate gameplay
Add more features to HearthCards to allow these cards to work

FEATURES TO ADD TO HEARTHCARDS:
Rush
Choose One
Adding an effect to a minion as a buff (currently problematic if minion has a corresponding effect already)
Current system only allows drawing / targeting from battlecries and spell effects; this needs to be revamped to support all effects that need input
Silence (currently removes all effects; may cause problems with copying)
'''
import HearthCards as hc
import TestPlays as test
import Ai as ai

myClass = "Druid"
oppClass = "Mage"
me = hc.Hero(myClass)
me.mana += 1
me.maxMana += 1
opp = hc.Hero(oppClass)
field = hc.Game(me,opp)

alg = ai.train_model(0.1,1000)

def findName(name,arr):
  if name == 'face':
    return field.opponent
  elif name == 'self':
    return field.me
  else:
    for i in arr:
        if i.name == name:
            return i
  return -1

#Split a command into words, then remove underscores
def splitCommand(cmd):
  out = cmd.split(' ')
  for i in range(0,len(out)):
    out[i] = out[i].replace('_',' ')
  return out

#Find the position targeted in a command
def getPosition(cmd,arr):
  if cmd == 'end':
    return len(arr)
  else:
    name = cmd[1:len(cmd)]
    minion = findName(name,arr)
    if minion != -1 and cmd[0] == '<':
      return arr.index(minion)
    elif minion != -1 and cmd[0] == '>':
      return arr.index(minion)-1
    else:
      print("Invalid position.")
      return -1

#Find the minion targeted in a command
def getTarget(cmd):
  try:
    side = cmd[1]
    minion = cmd[2]
  except IndexError:
    return -1
  if side == 'my':
    return findName(minion,field.myBoard)
  elif side == 'enemy':
    return findName(minion,field.oppBoard)
  else:
    return -1

#Summon a minion based on a command
def summon(cmd):
  try:
    name = cmd[1]
    pos = getPosition(cmd[2],field.myBoard)
  except IndexError:
    print("summon [name] [position] OR summon [name] [position] [cost] [atk] [health]")
    return
  if pos == -1: 
    return
  try:
    mana = int(cmd[3])
    atk = int(cmd[4])
    health = int(cmd[5])
  except IndexError:
    card = findName(name,hc.cardDefs)
    if card != -1:
      field.summon(card,pos)
      print("Summoned "+card.name+".")
    else:
      print("Minion not in database. No stats given.")
    return

  field.summon(hc.Minion(name,mana,atk,health),pos)
  print('Summoned',str(mana)+'-cost',str(atk)+'/'+str(health),str(name))

#Play a card from the current hand based on a command
def play(cmd):

  #Attempt to find card, and return at all possible exceptions
  try: 
    card = findName(cmd[1],field.myHand)
  except IndexError:
    print('play [card] [position (optional)]')
    return
  try: 
    position = getPosition(cmd[2],field.myBoard)
    if position == -1:
      return
  except IndexError: 
    position = -1
  if card == -1:
    card = findName(cmd[1],hc.cardDefs)
    if card == -1:
      print('That card is not in your hand.')
      return
    else:
      print('Card not in hand, but found in database.')
      field.addToHand(card)
      card = findName(cmd[1],field.myHand)
  elif field.me.mana < card.cost:
    print("Not enough mana.")
    return 

  #Handle targeting effects, or set target to None
  if 'Target' in card.effects:
    target = splitCommand(input('Enter target: '))
    target.insert(0,'')
    target = getTarget(target)
    if target == -1 or ('Spell' in card.effects and 'Elusive' in target.effects):
      print('Invalid target.')
      return
  else:
    target = None
  #Handle draw effects
  if 'Draw' in card.effects:
    draw = []
    i = 0
    while i < card.effects['Draw'](card):
      draw.append(input('Enter card pulled: '))
      cmd = splitCommand(draw[i])
      draw[i] = findName(cmd[0],hc.cardDefs)
      if draw[i] == -1:
        try:
          name = cmd[0]
          cost = int(cmd[1])
          atk = int(cmd[2])
          hlth = int(cmd[3])
          draw[i] = hc.Minion(name,cost,atk,hlth)
        except IndexError:
          try:
            name = cmd[0]
            cost = int(cmd[1])
            draw[i] = hc.Spell(name,cost,field.me.hearthClass)
          except IndexError:
            print('Card not recognized.')
            i -= 1
            draw.pop(i)
      i += 1
  else:
    draw = None

  #Play the actual card
  if field.playCard(card,target,position,draw):
    print('Played '+card.name+'.')
  else:
    print('Card failed for unknown reason.')
  return

#Add a card to the current hand based on a command
def draw(cmd):
  try:
    name = cmd[1]
  except IndexError:
    print('draw [card] OR draw [card] [cost] OR draw [card] [cost] [attack] [health]')
    return
  try:
    mana = int(cmd[2])
  except IndexError:
    card = findName(name,hc.cardDefs)
    if card == -1:
      print("I don't recognize that card.")
      return
    else:
      field.addToHand(card)
      print('Added',name,'to hand.')
      return
  try:
    atk = int(cmd[3])
    health = int(cmd[4])
  except IndexError:
    field.myHand.append(hc.Spell(name,mana,'Neutral',sGame=field))
    print('Added '+str(mana)+'-cost "'+name+'" spell to hand.')
    return
  field.addToHand(hc.Minion(name,mana,atk,health))
  print('Added '+str(mana)+'-cost '+str(atk)+'/'+str(health)+' "'+name+'" to hand.')

#Damage a minion based on a command
def damage(cmd):
  try:
    side = cmd[1]
    minion = cmd[2]
    dmg = int(cmd[3])
  except IndexError:
    print('damage [side] [minion] [damage]')
    return
  minion = getTarget(cmd)
  if minion == -1:
    print('Minion not found.')
    return
  field.damage(minion,dmg)
  field.resolveDeath()

#Add stats to a minion based on a command
def buff(cmd):
  try:
    side = cmd[1]
    minion = cmd[2]
    atk = int(cmd[3])
    health = int(cmd[4])
  except IndexError:
    print('buff [side] [minion] [attack] [health]')
    return
  minion = getTarget(cmd)
  field.buff(minion,atk,health)
  print('Added +' + str(atk) + '/+' + str(health) + ' to ' + minion.name)

#Remove a card from the current hand based on a command
def discard(cmd):
  try: 
    card = cmd[1]
  except IndexError: 
    print('discard [card]')
    return
  card = findName(card,field.myHand)
  if card != -1:
    field.myHand.remove(card)
    print('Discarded '+card.name)
  else:
    print('That card is not in your hand.')

#Have a minion attack another minion or the opponent based on a command
def attack(cmd):
  try:
    attacker = findName(cmd[1],field.myBoard)
    defender = findName(cmd[2],field.oppBoard)
  except IndexError:
    print('attack [attacker] [defender]')
    return
  if attacker == -1 or defender == -1:
    print('Invalid attacker or defender')
    return
  if attacker.attack(defender):
    print(cmd[1],'attacks',cmd[2]+'.')
  else:
    print('Attack failed.')

#Gain mana
def mana(cmd):
  try:
    field.me.mana += int(cmd[1])
  except IndexError:
    print('mana [amount]')

def remove(cmd):
  try:
    side = cmd[1]
    minion = cmd[2]
  except IndexError:
    print('remove [side] [minion]')
    return
  minion = getTarget(cmd)
  if minion == -1: 
    print('Minion not found.')
    return
  field.kill(minion,False)
  print('Removed',minion.name+'.')

def testAll(cmd):
  results = test.playCards(field)
  print(test.checkResults(results,field,alg))
  return results
  
#Dict of all possible comands
commands = {
  'summon': lambda cmd:summon(cmd),
  'play': lambda cmd:play(cmd),
  'draw': lambda cmd:draw(cmd),
  'damage': lambda cmd:damage(cmd),
  'pass': lambda cmd:field.switchTurn(),
  'buff': lambda cmd:buff(cmd),
  'discard': lambda cmd:discard(cmd),
  'attack': lambda cmd:attack(cmd),
  'mana': lambda cmd:mana(cmd),
  'test': lambda cmd:testAll(cmd),
  'remove': lambda cmd:remove(cmd)
}

while True:
  command = splitCommand(input('>'))
  if command[0] in commands:
    commands[command[0]](command)

    print('========='+str(field.opponent.health)+'===='+str(field.opponent.mana)+'=====')
    for i in field.oppBoard:
      print(i.name,i.atk,i.health,end=' | ')
    print('\n')
    for i in field.myBoard:
      if 'Divine Shield' in i.effects:
        print('()',end='')
      if 'Frozen' in i.effects:
        print('~',end='')
      elif i.canAttack or ('Windfury' in i.effects and i.effects['Windfury']):
        print('*',end='')
      print(i.name,i.atk,i.health,end=' | ')
    print('')
    print('========='+str(field.me.health)+'===='+str(field.me.mana)+'=====')
    print('In hand:')
    for i in field.myHand:
      print(i.cost,i.name,end=' | ')
    print('')
  else:
    print('Unrecognized command.')