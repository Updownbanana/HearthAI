import copy

def basicAttack(self,enemy):
  taunt = False
  #Check for taunt on enemy board
  for i in self.game.oppBoard:
    if 'Taunt' in i.effects:
      taunt = True
  #Cannot target attack if enemy is immune or stealthed, if a taunt is in the way, if frozen, or if regular and windfury attacks are both used up
  if (('Immune' or 'Stealth') in enemy.effects) or (taunt and 'Taunt' not in enemy.effects) or 'Frozen' in self.effects:
    return False
  elif self.canAttack:
    self.canAttack = False
  elif 'Windfury' in self.effects and self.effects['Windfury']:
    self.effects['Windfury'] = False
  else:
    return False
  #If this does not have a special attack, run a regular attack
  if 'Attack' in self.effects:
    return self.game.runEffect('Attack',self,enemy)
  else:
    self.game.damage(enemy,self.atk)
    self.game.damage(self,enemy.atk)
    self.game.resolveDeath()
    return True
def weaponAttack(self,enemy):
  self.game.damage(enemy,self.atk)
  self.game.damage(self,1)
  self.game.resolveDeath()
  
#----------Game element classes----------

class Minion:
  def __init__(self,mName,mCost,mAtk,mHealth,mType=[],mEffect=[],mGame=None,mClass='Neutral'):
    self.name = mName
    self.cost = mCost
    self.baseCost = mCost
    self.atk = mAtk
    self.baseAtk = mAtk
    self.health = mHealth
    self.baseHealth = mHealth
    self.maxHealth = mHealth
    self.hearthClass = mClass
    while len(mEffect) < len(mType):
      mEffect.append(None)
    self.effects = {etype:effect for etype,effect in zip(mType,mEffect)}
    self.game = mGame

  buffAtk = 0
  buffHealth = 0
  auraAtk = 0
  auraHealth = 0
  damage = 0
  buffCost = 0
  auraCost = 0
  
  canAttack = False

  def attack(self,enemy):
    basicAttack(self,enemy)

class Spell:
  def __init__(self,sName,sCost,sClass,sType=[None],sEffect=[None],sGame=None):
    self.name = sName
    self.cost = sCost
    self.baseCost = sCost
    self.hearthClass = sClass
    self.effectType = sType
    while len(sEffect) < len(sType):
      sEffect.append(None)
    self.effects = {etype:effect for etype,effect in zip(sType,sEffect)}
    self.game = sGame
  
  buffCost = 0
  auraCost = 0

class Weapon:
  def __init__(self,wName,wCost,wAtk,wHealth,wType=['Attack'],wEffects=[lambda m,t:weaponAttack(m,t)],wHero=None,wClass='Neutral'):
    self.name = wName
    self.cost = wCost
    self.baseCost = wCost
    self.atk = wAtk
    self.baseAtk = wAtk
    self.health = wHealth
    self.baseHealth = wHealth
    self.hearthClass = wClass
    self.hero = wHero
    while len(wEffects) < len(wType):
      wEffects.append(None)
    self.effects = {etype:effect for etype,effect in zip(wType,wEffects)}
        
  buffAtk = 0
  buffHealth = 0
  auraAtk = 0
  auraHealth = 0
  damage = 0
  buffCost = 0
  auraCost = 0
        
  def attack(self,enemy):
    self.atk += self.hero.atk
    basicAttack(self,enemy)


class Hero:
  def __init__(self,hClass='Neutral',hGame=None):
    self.hearthClass = hClass
    self.effects = {}
    self.game = hGame
  mana = 0
  maxMana = 0
  atk = 0
  health = 30
  maxHealth = 30
  armor = 0
  weapon = None
  
  buffAtk = 0
  buffHealth = 0
  auraAtk = 0
  auraHealth = 0
  damage = 0

  def attack(self,enemy):
    if self.game.checkWeapon(self):
      self.weapon.attack(self,enemy)
    else:
      basicAttack(self,enemy)

#----------Game class with useful functions----------

class Game:
  def __init__(self,gMe,gOpponent):
    self.hero1 = gMe
    self.hero1.game = self
    self.hero2 = gOpponent
    self.hero2.game = self
    self.me = self.hero1
    self.opponent = self.hero2

    self.board1 = []
    self.board2 = []
    self.myBoard = self.board1
    self.oppBoard = self.board2

    self.hand1 = []
    self.hand2 = []
    self.myHand = self.hand1
    self.oppHand = self.hand2

    self.summonOrder = []

  #Run a specific effect of a card, if it has that effect
  def runEffect(self,effect,card,arg1=None,arg2=None,arg3=None,default=False,resolve=True):
    succ = default
    if effect in card.effects:
      if arg3 != None and arg2 != None and arg1 != None:
        succ = card.effects[effect](card,arg1,arg2,arg3)
      elif arg2 != None and arg1 != None:
        succ = card.effects[effect](card,arg1,arg2)
      elif arg1 != None:
        succ = card.effects[effect](card,arg1)
      else:
        succ = card.effects[effect](card)
    if succ and resolve: self.resolveDeath()
    return succ

  #Use the runEffect function on all cards in a list
  def runEffectAll(self,effect,origin=None,order=None):
    if order == None:
      order = self.summonOrder
    if origin == None:
      for card in order:
        self.runEffect(effect,card)
    else:
      for card in order:
        self.runEffect(effect,card,origin)

  def checkWeapon(hero):
    return hero.weapon != None
  
  #Add a card to the current hand
  def addToHand(self,card,hand=None):
    if hand == None:
      hand = self.myHand
    if self.runEffect('Casts When Drawn',card):
      return True
    elif(len(hand) < 10):
      card = copy.deepcopy(card)
      if not isinstance(card,Weapon):
        card.game = self
      hand.append(card)
      self.checkAuras()
      return True
    return False

  #Summon a minion in a specific position, or just at the end if no position is specified
  def summon(self,minion,position=-1,board=None):
    if board == None:
      board = self.myBoard
    if len(board) < 7:
      minion = copy.deepcopy(minion)
      minion.game = self
      if position < 0:
        board.append(minion)
      else:
        board.insert(position,minion)
      self.summonOrder.append(minion)
      if 'Charge' in minion.effects:
        minion.canAttack = True
        if 'Windfury' in minion.effects:
          minion.effects['Windfury'] = True
      elif 'Windfury' in minion.effects:
        minion.effects['Windfury'] = False
      self.runEffectAll('Summon',minion)
      return True
    return False

  #Equip a weapon to the current hero
  def equip(self,weapon,hero=None):
    if hero == None:
      hero = self.me
    if self.checkWeapon(hero):
      self.kill(hero.weapon)
    hero.weapon = weapon
    weapon.hero = hero
    return True

  #Play a card; run battlecry or spell effect, targeting or not, then summon if it is a minion
  def playCard(self,card,arg1=None,position=-1,arg2=None,arg3=None):
    if self.me.mana < card.cost: 
      return False
    succ = True
    succ = self.runEffect('Spell',card,arg1,arg2,arg3,succ)
    if isinstance(card,Minion):
      succ = self.summon(card,position)
    elif isinstance(card,Weapon):
      succ = self.equip(card)
    if succ:
      succ = self.runEffect('Battlecry',card,arg1,arg2,arg3,succ)
    if succ:
      self.runEffectAll('Play Card',card)
      self.myHand.remove(card)
      self.me.mana -= card.cost
    self.checkAuras()
    return succ
  
  #Deal damage to a minion
  def damage(self,minion,dmg,spell=False):
    if spell and dmg > 0:
      for i in self.myBoard:
        if 'Spell Damage' in i.effects:
          dmg += i.effects['Spell Damage']
    if 'Divine Shield' in minion.effects and dmg > 0:
      del minion.effects['Divine Shield']
      dmg = 0
    minion.damage = min(minion.damage-dmg,0)
    minion.health = minion.maxHealth + minion.damage
    if dmg > 0:
      self.runEffectAll('Damage',minion)
    elif dmg < 0:
      self.runEffectAll('Heal',minion)
    return True
  
  #Kill all minions with 0 health or less
  def resolveDeath(self):
    dummy = copy.copy(self.summonOrder)
    for minion in dummy:
      if minion.health <= 0:
        self.kill(minion)
        print(dummy)
    for weapon in [self.me.weapon,self.opponent.weapon]:
      if weapon != None and weapon.health <= 0:
        self.kill(weapon)
    self.checkAuras()

  #Kill a minion after running its deathrattle (unless specified otherwise)
  def kill(self,minion,dr=True):
    #Do not kill heroes
    if isinstance(minion,Hero):
      return
    #Otherwise, remove from its board and the summon order
    if isinstance(minion,Weapon):
      if self.me.weapon == minion:
        self.me.weapon = None
      elif self.opponent.weapon == minion:
        self.opponent.weapon = None
    elif minion in self.myBoard:
      self.runEffectAll('Death',minion)
      self.myBoard.remove(minion)
      self.summonOrder.remove(minion)
    elif minion in self.oppBoard:
      self.runEffectAll('Death',minion)
      self.oppBoard.remove(minion)
      self.summonOrder.remove(minion)
    #Execute deathrattle, unless otherwise specified
    if dr:
      self.runEffect('Deathrattle',minion)

  #Add or remove stats from a minion
  def buff(self,target,atk,health,cost=0):
    if isinstance(target,Minion or Hero):
      target.buffAtk += atk
      target.buffHealth += health
      target.atk = target.baseAtk + target.buffAtk + target.auraAtk
      target.atk = max(target.atk,0)
      target.maxHealth = target.baseHealth + target.buffHealth + target.auraHealth
      if target.maxHealth <= 0:
        self.kill(target,self.myBoard.count(target)>0)
      else:
        target.health = target.maxHealth + target.damage
    if not isinstance(target,Hero):
      target.buffCost += cost
      target.cost = max(target.baseCost + target.buffCost + target.auraCost, 0)
    return True

  def checkAuras(self):
    #Reset aura buffs, including card cost
    for i in self.summonOrder:
      i.auraAtk = 0
      i.auraHealth = 0
    for i in self.myHand:
      i.auraCost = 0
    for i in self.oppHand:
      i.auraCost = 0
    #Run all aura effects and in-hand cost reduction effects
    self.runEffectAll('Aura')
    self.runEffectAll('Hand Aura',order=self.myHand)
    self.runEffectAll('Hand Aura',order=self.oppHand)
    #Use the buff method to re-calculate all minion stats
    for i in self.summonOrder:
      self.buff(i,0,0)
    for i in self.myHand:
      self.buff(i,0,0)
    for i in self.oppHand:
      self.buff(i,0,0)
    
  def addEffect(self,card,eType,effect=None):
    if eType not in card.effects:
      card.effects[eType] = effect
    elif effect in card.effects:
      return
    else:
      #what the fuck
      return

  #Switch the turn to the other player by switching the heroes and boards
  def switchTurn(self):
    self.runEffectAll('End of Turn')

    #Remove frozen status if minions could have attacked this turn
    for i in self.myBoard:
      if 'Frozen' in i.effects and i.canAttack:
        i.effects.remove('Frozen')

    #Switch boards
    if self.myBoard == self.board1:
      self.myBoard = self.board2
      self.oppBoard = self.board1
    elif self.myBoard == self.board2:
      self.myBoard = self.board1
      self.oppBoard = self.board2

    #Switch heroes
    if self.me == self.hero1:
      self.me = self.hero2
      self.opponent = self.hero1
    elif self.me == self.hero2:
      self.me = self.hero1
      self.opponent = self.hero2

    #Switch hands
    if self.myHand == self.hand1:
      self.myHand = self.hand2
      self.oppHand = self.hand1
    elif self.myHand == self.hand2:
      self.myHand = self.hand1
      self.oppHand = self.hand2

    #Reset all minion's attacks
    for i in self.myBoard:
      i.canAttack = True
      if 'Windfury' in i.effects:
        i.effects['Windfury'] = True

    #Gain 1 mana
    self.me.maxMana = min(10,self.me.maxMana+1)
    self.me.mana = self.me.maxMana

    self.runEffectAll('Start of Turn')

  #Discard a card from the current hand
  def discard(self,card):
    self.myHand.remove(card)
    self.runEffect('Discard',card)

  #Find the minions adjacent to a specific minion
  def getAdjacent(self,minion):
    if minion in self.myBoard:
      board = self.myBoard
    elif minion in self.oppBoard:
      board = self.oppBoard
    else:
      return []
    pos = board.index(minion)
    targets = []
    try:
      targets.append(board[pos-1])
    except IndexError:
      pass
    try:
      targets.append(board[pos+1])
    except IndexError:
      pass
    return targets

  #Silence a minion (this will currently cause problems with copying / adding to hand)
  def silence(self,target):
    target.buffAtk = 0
    target.buffHealth = 0
    target.effects = {}

  #Get the position of a minion anywhere on the board
  def getMinion(self,minion):
    if minion in self.myBoard:
      return self.myBoard.index(minion)
    elif minion in self.oppBoard:
      return self.oppBoard.index(minion)
    return -1

  #Return which board a minion is on
  def getBoard(self,minion):
    if minion in self.myBoard:
      return self.myBoard
    elif minion in self.oppBoard:
      return self.oppBoard
    return -1

#Take card definitions from other files
import Classic
import Rastakhan
cardDefs = [i for i in Classic.cardDefs]
for i in Rastakhan.cardDefs:
  cardDefs.append(i)
