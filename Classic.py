import HearthCards as hc
import copy
#----------Classic card code and definitions----------

cardDefs = []

def addMinion(name,cost,atk,health,mType=[],effect=[],game=None,mClass='Neutral'):
  cardDefs.append(hc.Minion(name,cost,atk,health,mType,effect,game,mClass))
def addSpell(name,cost,sClass,sType=[],effect=[],game=None):
  cardDefs.append(hc.Spell(name,cost,sClass,sType,effect,game))
def addWeapon(name,cost,atk,health,wType=[],effects=[],hero=None,wClass='Neutral'):
  cardDefs.append(hc.Weapon(name,cost,atk,health,wType,effects,hero,wClass))

def Snipe_Secret(self,target):
  self.game.damage(target,4)
addSpell("Snipe",2,'Hunter',["Secret"],[lambda me,target:Snipe_Secret(me,target)])

def Abomination_Deathrattle(self):
  game = self.game
  for i in game.summonOrder:
    game.damage(i,2)
  game.damage(game.me,2)
  game.damage(game.opponent,2)
  return True
addMinion('Abomination',5,4,4,['Deathrattle','Taunt'],[lambda me:Abomination_Deathrattle(me)])

#Need to fix by adding temporary buffs
def Sergeant_Battlecry(self,target):
  target.auraAttack += 2
  return True
addMinion('Abusive Sergeant',1,1,1,['Battlecry','Target'],[lambda me,target:Sergeant_Battlecry(me,target)])

#Touch up draw effects to be able to run anytime
def Acolyte(self,card):
  return self.game.addToHand(card[0])
addMinion('Acolyte of Pain',3,1,3)

#Another effect that pulls a random card and isn't a battlecry
addMinion('Alarm-o-Bot',3,0,3,['Mech'])

def Aldor_Battlecry(self,target):
  if isinstance(target,hc.Minion):
    target.atk = 1
    return True
  return False
addMinion('Aldor Peacekeeper',3,3,3,['Battlecry','Target'],[lambda me,target:Aldor_Battlecry(me,target)],mClass='Paladin')

def Alexstrasza_Battlecry(self,target):
  if isinstance(target,hc.Hero):
    target.health = 15
    return True
  return False
addMinion('Alexstrasza',9,8,8,['Battlecry','Target','Dragon'],[lambda me,target:Alexstrasza_Battlecry(me,target)])

def Amani_Berserker_Enrage(self):
  if self.damage < 0:
    self.auraAtk += 3
addMinion('Amani Berserker',2,2,3,['Aura'],[lambda me:Amani_Berserker_Enrage(me)])

#Copying is currently weird
def Ancestral_Deathrattle(self):
  game = self.game
  if self in game.myBoard:
    pos = game.myBoard.index(self)
    board = game.myBoard
  else:
    pos = game.oppBoard.index(self)
    board = game.oppBoard
  self.buffHealth = 0
  self.buffAtk = 0
  return game.summon(self,pos,board)
def Ancestral_Spirit(self,target):
  self.game.addEffect('Deathrattle',lambda m:Ancestral_Deathrattle(m))
addSpell('Ancestral Spirit',2,'Shaman',['Spell','Target'],[lambda me,target:Ancestral_Spirit(me,target)])

#Doesn't pull a fresh copy of the minion, only returns a copy to hand. Needs improvement. 
def Brewmaster_Battlecry(self,target):
  game = self.game
  if target in game.myBoard:
    game.addToHand(target)
    game.myBoard.remove(target)
    target.buffHealth = 0
    target.buffAtk = 0
    target.auraHealth = 0
    target.auraAtk = 0
    target.damage = 0
    return True
  return False
addMinion('Ancient Brewmaster',4,5,4,['Battlecry','Target'],[lambda me,target:Brewmaster_Battlecry(me,target)])
addMinion('Youthful Brewmaster',2,3,2,['Battlecry','Target'],[lambda me,target:Brewmaster_Battlecry(me,target)])

def Ancient_Mage_Battlecry(self):
  targets = self.game.getAdjacent(self)
  for left in targets:
    if 'Spell Damage' in left.effects:
      left.effects['Spell Damage'] += 1
    else:
      left.effects['Spell Damage'] = 1
  return True
addMinion('Ancient Mage',4,2,5,['Battlecry'],[lambda me:Ancient_Mage_Battlecry(me)])

#Need choose one effects; ancients of lore and war go here
addMinion('Ancient of Lore',7,5,5,mClass='Druid')
addMinion('Ancient of War',7,5,5,mClass='Druid')

def Angry_Chicken_Enrage(self):
  if self.damage < 0:
    self.auraAtk += 5
addMinion('Angry Chicken',1,1,1,['Aura'])

def Weaponsmith_Battlecry(self):
  self.game.equip(hc.Weapon('Battle Ax',1,2,2,wClass='Warrior',wHero=self.game.me))
addMinion('Arathi Weaponsmith',4,3,3,['Battlecry'],[lambda me:Weaponsmith_Battlecry(me)])

def Arcane_Golem_Battlecry(self):
  self.game.opponent.maxMana += 1
addMinion('Arcane Golem',3,4,4,['Battlecry'],[lambda me:Arcane_Golem_Battlecry(me)])

def Antonidas(self,card):
  if isinstance(card,hc.Spell):
    self.game.addToHand(hc.Spell('Fireball',4,'Mage',['Spell','Target'],[lambda me,target:Fireball(me,target)]))
addMinion('Archmage Antonidas',7,5,7,['Play Card'],[lambda m,o:Antonidas(m,o)],mClass='Mage')

def Argent_Protector_Battlecry(self,target):
  if target in self.game.myBoard and 'Divine Shield' not in target.effects:
    target.effects['Divine Shield'] = None
    return True
  return False
addMinion('Argent Protector',2,2,2,['Battlecry','Target'],[lambda me,target:Argent_Protector_Battlecry(me,target)],mClass='Paladin')

def Armorsmith(self,origin):
  if (origin in self.game.myBoard and self in self.game.myBoard):
    self.game.me.armor += 1
  elif (origin in self.game.oppBoard and self in self.game.oppBoard):
    self.game.opponent.armor += 1
addMinion('Armorsmith',2,1,4,['Damage'],[lambda me,origin:Armorsmith(me,origin)])

#Auchenai Soulpriest goes here, but I need to figure out auras
addMinion('Auchenai Soulpriest',4,3,5,mClass='Priest')

#Also multi target random effects, since random effects can't actually be random in this program
addSpell('Avenging Wrath',6,'Paladin',['Spell'])

#Draw effects need reworking; may change this card
def Bane_of_Doom(self,target,draw):
  self.game.damage(target,2,True)
  if target.health <= 0:
    self.game.summon(draw[0])
  return True
addSpell('Bane of Doom',5,'Warlock',['Spell','Draw','Target'],[lambda me,t,d:Bane_of_Doom(me,t,d),{'Pool':'Random', 'Effects':['Demon']}])

def Baron_Geddon(self):
  game = self.game
  for i in game.summonOrder:
    if i != self:
      game.damage(i,2)
  game.damage(game.me,2)
  game.damage(game.opponent,2)
  return True
addMinion('Baron Geddon',7,7,5,['End of Turn','Elemental'],[lambda me:Baron_Geddon(me)])

def Battle_Rage_Count(self):
  count = 0
  for i in self.game.myBoard:
    if i.health < i.maxHealth:
      count += 1
  hero = self.game.me
  if hero.health < hero.maxHealth:
    count += 1
  return count
def Battle_Rage(self,draws):
  if len(draws) <= 0: return False
  for i in draws:
    self.game.addToHand(i)
  return True
addSpell('Battle Rage',2,'Warrior',['Spell','Draw'],[lambda me,draws:Battle_Rage(me,draws),{'Pool':'myDeck', 'Count':lambda m:Battle_Rage_Count(m)}])

#Still need to rework minion buffs, so won't code the immune here for now
def Bestial_Wrath(self,target):
  if 'Beast' in target.effects:
    self.game.buff(target,2,0)
    return True
  return False
addSpell('Bestial Wrath',1,'Hunter',['Spell','Target'],[lambda me,t:Bestial_Wrath(me,t)])

def Betrayal(self,target):
  board = self.game.oppBoard
  if target not in board: 
    return False
  victims = []
  pos = board.index(target)
  traitor = copy.deepcopy(target)
  try:
    victims.append(board[pos-1])
  except IndexError:
    pass
  try:
    victims.append(board[pos+1])
  except IndexError:
    pass
  if len(victims) <= 0:
    return False
  for i in victims:
    traitor.attack(i)
  return True
addSpell('Betrayal',2,'Rogue',['Spell','Target'],[lambda me,t:Betrayal(me,t)])

def BGH_Battlecry(self,target):
  if target.attack >= 7:
    self.game.kill(target)
    return True
  return False
addMinion('Big Game Hunter',5,4,2,['Battlecry','Target'],[lambda me,t:BGH_Battlecry(me,t)])

def Bite(self):
  self.game.me.atk += 4
  self.game.me.armor += 4
  return True
addSpell('Bite',4,'Druid',['Spell'],[lambda me:Bite(me)])

def Blade_Flurry(self):
  for i in self.game.oppBoard:
    weapon = copy.copy(self.game.me.weapon)
    weapon.attack(i)
  self.game.kill(self.game.me.weapon)
addSpell('Blade Flurry',4,'Rogue',['Spell'],[lambda me:Blade_Flurry(me)])

def Blessed_Champion(self,target):
  self.game.buff(target,target.atk,0)
addSpell('Blessed Champion',5,'Paladin',['Spell','Target'],[lambda me,t:Blessed_Champion(me,t)])

#Draw effect
addSpell('Blessing of Wisdom',1,'Paladin')

def Blizzard(self):
  for i in self.game.oppBoard:
    self.game.damage(i,2,True)
    self.game.addEffect(i,'Frozen')
  return True
addSpell('Blizzard',6,'Mage',['Spell'],[lambda m:Blizzard(m)])

#Stealth must be implemented; targeting effects outside of battlecries
addMinion('Blood Imp',1,0,1,['Stealth','Demon'],mClass='Warlock')

#Divine Shield isn't fully implemented yet
def Blood_Knight_Battlecry(self):
  for i in self.game.summonOrder:
    if i.effects.pop('Divine Shield', 'Nope') != 'Nope':
      self.game.buff(self,3,3)
addMinion('Blood Knight',3,3,3,['Battlecry'],[lambda me:Blood_Knight_Battlecry(me)])

#Need to be able to draw from other effects
addMinion('Bloodmage Thalnos',2,1,1,['Spell Damage'],[1])

def Corsair_Battlecry(self):
  game = self.game
  if game.checkWeapon(game.opponent):
    self.game.opponent.weapon.health -= 1
addMinion('Bloodsail Corsair',1,1,2,['Battlecry','Pirate'],[lambda me:Corsair_Battlecry(me)])

def Raider_Battlecry(self):
  game = self.game
  if game.checkWeapon(game.me):
    game.buff(self,game.me.weapon.atk)
    return True
  return False
addMinion('Bloodsail Raider',2,2,3,['Battlecry','Pirate'],[lambda me:Raider_Battlecry(me)])

def Brawl(self,target):
  game = self.game
  for i in game.summonOrder:
    if i != target:
      game.kill(i)
addSpell('Brawl',5,'Warrior',['Spell','Target'],[lambda me,t:Brawl(me,t)])

def Shadow_Priest_Battlecry(self,target):
  if target.atk <= 2 and len(self.game.myBoard) < 7:
    self.game.oppBoard.remove(target)
    self.game.myBoard.append(target)
    return True
  return False
addMinion('Cabal Shadow Priest',6,4,5,['Battlecry'],[lambda me,t:Shadow_Priest_Battlecry(me,t)],mClass='Priest')

def Cairne_Deathrattle(self):
  pos = self.game.myBoard.index(self)
  self.game.summon(hc.Minion('Baine Bloodhoof',4,4,5),pos)
addMinion('Cairne Bloodhoof',6,4,5,['Deathrattle'],[lambda me:Cairne_Deathrattle(me)])

addSpell('Call of the Void',1,'Warlock',['Spell','Draw'],[lambda m,d:m.game.addToHand(d[0]),{'Pool':'Random','Effects':['Demon']}])

def Greenskin_Battlecry(self):
  if self.game.checkWeapon(self.game.me):
    self.game.buff(self.game.me.weapon,1,1)
addMinion('Captain Greenskin',5,5,4,['Battlecry','Pirate'])

#And choose ones
addMinion('Cenarius',9,5,8,mClass='Druid')

def Circle_of_Healing(self):
  for i in self.game.summonOrder:
    self.game.damage(i,-4)
addSpell('Circle of Healing',0,'Priest',['Spell'],[lambda me: Circle_of_Healing(me)])

def Coldlight_Seer_Battlecry(self):
  for i in self.game.myBoard:
    if 'Murloc' in i.effects:
      self.game.buff(i,0,2)
addMinion('Coldlight Seer',3,2,3,['Battlecry'],[lambda me:Coldlight_Seer_Battlecry(me)])

#Auras aren't really perfect whoops
addSpell('Commanding Shout',2,'Warrior')

def Cone_of_Cold(self,target):
  targets = self.game.getAdjacent(target)
  for i in targets:
    self.game.damage(i,1,True)
    self.game.addEffect(target,'Frozen')
  return True
addSpell('Cone of Cold',4,'Mage',['Spell','Target'],[lambda m,t:Cone_of_Cold(m,t)])

#Combos aren't a thing yet
addSpell('Cold Blood',1,'Rogue')

#Neither are secrets oh my god
addSpell('Counterspell',3,'Mage',['Secret'])

#Might cause problems with copying
def Crazed_Alchemist_Battlecry(self,target):
  base = target.baseHealth
  buff = target.buffHealth
  target.baseHealth = target.baseAtk
  target.buffHealth = target.buffAtk
  target.baseAtk = base
  target.buffAtk = buff
addMinion('Crazed Alchemist',2,2,2,['Battlecry','Target'],[lambda me,t:Crazed_Alchemist_Battlecry(me,t)])

def Taskmaster_Battlecry(self,target):
  self.game.buff(target,2,0)
  self.game.damage(target,1)
addMinion('Cruel Taskmaster',2,2,2,['Battlecry','Target'],[lambda me,t:Taskmaster_Battlecry(me,t)],mClass='Warrior')

#Draw effects
addMinion('Cult Master',4,4,2)

#Auras aren't perfect; this one might change
def Dark_Iron_Dwarf_Battlecry(self,target):
  target.auraAtk += 2
addMinion('Dark Iron Dwarf',4,4,4,['Battlecry','Target'],[lambda me,t:Dark_Iron_Dwarf_Battlecry(me,t)])

def Deadly_Shot(self,target):
  self.game.kill(target)
addSpell('Deadly Shot',3,'Hunter',['Spell','Target'],[lambda me,t:Deadly_Shot(me,t)])

def Deathwing_Battlecry(self):
  game = self.game
  for i in game.summonOrder:
    if i != self:
      game.kill(i)
  for i in game.myHand:
    game.discard(i)
addMinion('Deathwing',10,12,12,['Battlecry'],[lambda me:Deathwing_Battlecry(me)])

def Defender_Argus_Battlecry(self):
  targets = self.game.getAdjacent(self)
  for i in targets:
    self.game.buff(i,1,1)
    i.effects['Taunt'] = None
addMinion('Defender of Argus',4,2,3,['Battlecry'],[lambda me:Defender_Argus_Battlecry(me)])

#Combos aren't a thing
addMinion('Defias Ringleader',2,2,2,mClass='Rogue')

#Need targeting effects outside of battlecries (this one is low priority though)
addMinion('Demolisher',3,1,4)

def Demonfire(self,target):
  if target in self.game.myBoard and 'Demon' in target.effects:
    return self.game.buff(target,2,2)
  else:
    return self.game.damage(target,2,True)
addSpell('Demonfire',2,'Warlock',['Spell','Target'],[lambda me,t:Demonfire(me,t)])

def Alpha_Aura(self):
  targets = self.game.getAdjacent(self)
  for i in targets:
    i.auraAtk += 1
addMinion('Dire Wolf Alpha',2,2,2,['Aura'],[lambda me:Alpha_Aura(me)])

def Divine_Favor_Count(self):
  game = self.game
  count = len(game.oppHand) - len(game.myHand)
  return max(count,0)
def Divine_Favor(self,draws):
  for i in draws:
    self.game.addToHand(i)
addSpell('Divine Favor',3,'Paladin',['Spell','Draw'],[lambda me,d:Divine_Favor(me,d),{'Pool':'myDeck','Count':lambda m:Divine_Favor_Count(m)}])

#Don't really have discard planned out
addMinion('Doomguard',5,5,7,['Battlecry','Charge'],mClass='Warlock')

def Doomsayer(self):
  game = self.game
  if self in game.myBoard:
    for i in game.summonOrder:
      game.kill(i)
addMinion('Doomsayer',2,0,7,['Start of Turn'],[lambda me:Doomsayer(me)])

def Corsair_Aura(self):
  game = self.game
  if game.checkWeapon(game.me):
    game.buff(self,0,0,-game.me.weapon.atk)
addMinion('Dread Corsair',4,3,3,['Hand Aura','Taunt'],[lambda m:Corsair_Aura(m)])

#Neither do Choose One effects
addMinion('Druid of the Claw',5,4,4,mClass='Druid')

#Or secrets
addWeapon('Eaglehorn Bow',3,3,2,wClass='Hunter')

def Earth_Shock(self,target):
  self.game.silence(target)
  self.game.damage(target,1,True)
addSpell('Earth Shock',1,'Shaman',['Spell','Target'],[lambda me,t:Earth_Shock(me,t)])

def Farseer_Battlecry(self,target):
  self.game.damage(target,-3)
addMinion('Earthen Ring Farseer',3,3,3,['Battlecry','Target'],[lambda me,t:Farseer_Battlecry(me,t)])

#Combos aren't working
addMinion('Edwin VanCleef',3,2,2,mClass='Rogue')

def Equality(self):
  for i in self.game.summonOrder:
    i.buffHealth = 0
    self.game.buff(i,0,-1*(i.maxHealth-1))
  return True
addSpell('Equality',2,'Paladin',['Spell'],[lambda me:Equality(me)])

#Secrets aren't yet implemented
addMinion('Ethereal Arcanist',4,3,3,mClass='Mage')

#Neither are combos
addSpell('Eviscerate',2,'Rogue')

def Explosive_Shot(self,target):
  for i in self.game.getAdjacent(target):
    self.game.damage(i,2,True)
  self.game.damage(target,5,True)
  return True
addSpell('Explosive Shot',5,'Hunter',['Spell','Target'],[lambda me,t:Explosive_Shot(me,t)])

#Secrets aren't implemented
def Explosive_Trap(self):
  for i in self.game.myBoard:
    self.game.damage(i,2,True)
addSpell("Explosive Trap",2,'Hunter',["Secret"],[lambda me:Explosive_Trap(me)])

#Another secret
addSpell('Eye for an Eye',1,'Paladin',['Secret'])

#Not sure of the best way to code Faceless Manipulator just yet; copies are weird
addMinion('Faceless Manipulator',5,3,3)

def Far_Sight(self,draw):
  draw[0].buffCost -= 3
  return self.game.addToHand(draw[0])
addSpell('Far Sight',3,'Shaman',['Spell','Draw'],[lambda m,d:Far_Sight(m,d),{'Pool':'myDeck'}])

def Felguard_Battlecry(self):
  game = self.game
  game.me.maxMana -= 1
  if game.me.mana > game.me.maxMana:
    game.me.mana -= 1
addMinion('Felguard',3,3,5,['Battlecry','Taunt','Demon'],[lambda m:Felguard_Battlecry(m)])

#Overload card; not implemented yet but it should work
def Feral_Spirit(self):
  succ = False
  for i in range(2):
    if(self.game.summon(hc.Minion('Spirit Wolf',2,2,3,['Taunt']))):
      succ = True
  return succ
addSpell('Feral Spirit',3,'Shaman',['Spell','Overload'],[lambda m:Feral_Spirit(m),2])

def Flame_Imp_Battlecry(self):
  self.game.damage(self.game.me,3)
  return True
addMinion('Flame Imp',1,3,2,['Battlecry','Demon'],[lambda m:Flame_Imp_Battlecry(m)])

#Not sure how to remove an effect like Stealth; also secrets aren't implemented
addSpell('Flare',2,'Hunter')

def Flesheating_Ghoul(self,origin):
  if isinstance(origin,hc.Minion):
    self.game.buff(self,1,0)
addMinion('Flesheating Ghoul',3,2,3,['Death'],[lambda m,o:Flesheating_Ghoul(m,o)])

def Force_of_Nature(self):
  succ = False
  for i in range(3):
    if(self.game.summon(hc.Minion('Treant',2,2,2))):
      succ = True
  return succ
addSpell('Force of Nature',5,'Druid',['Spell'],[lambda m:Force_of_Nature(m)])

#Multiple random tarets hahaaaa
addSpell('Forked Lightning',1,'Shaman')

#And another secret
def Freezing_Trap(self,target):
  self.game.kill(target,True,False)
addSpell("Freezing Trap",2,'Hunter',['Secret'],[lambda me,target:Freezing_Trap(me,target)])

addMinion('Frost Elemental',6,5,5,['Battlecry','Target','Elemental'],[lambda m,t:m.game.addEffect(t,'Frozen')])

def Frothing_Berserker(self,origin):
  if isinstance(origin,hc.Minion):
    self.game.buff(self,1,0)
addMinion('Frothing Berserker',3,2,4,['Damage'],[lambda me,o:Frothing_Berserker(me,o)],mClass='Warrior')

#Drawing from another effect
addMinion('Gadgetzan Auctioneer',6,4,4,['Cast Spell'])

def Longbow_Attack(self,target):
  self.hero.game.damage(target,self.atk)
addWeapon("Gladiator's Longbow",7,5,2,['Attack'],[lambda m,t:Longbow_Attack(m,t)],wClass='Hunter')

def Gorehowl_Attack(self,target):
  game = self.hero.game
  game.damage(target,self.atk)
  if isinstance(target,hc.Minion):
    game.buff(self,-1,0)
  else:
    game.damage(self,1)
addWeapon('Gorehowl',7,7,1,['Attack'],[lambda m,t:Gorehowl_Attack(m,t)],wClass='Warrior')

def Grommash_Enrage(self):
  if self.health < self.maxHealth:
    self.auraAtk += 6
addMinion('Grommash Hellscream',8,4,9,['Aura'],[lambda m:Grommash_Enrage(m)],mClass='Warrior')

def Gruul(self):
  self.game.buff(self,1,1)
addMinion('Gruul',8,7,7,['End of Turn'],[lambda m:Gruul(m)])

def Harrison_Count(self):
  game = self.game
  if game.checkWeapon(game.opponent):
    return game.opponent.weapon.health
  return 0
def Harrison_Battlecry(self,draw):
  game = self.game
  if game.checkWeapon(game.opponent):
    game.kill(game.opponent.weapon)
    for i in draw:
      game.addToHand(i)
    return True
  return False
addMinion('Harrison Jones',5,5,4,['Battlecry','Draw'],[lambda m,d:Harrison_Battlecry(m,d),{'Pool':'myDeck','Count':lambda m:Harrison_Count(m)}])

#This always summons on the friendly side right now
def Harvest_Golem_Deathrattle(self):
  pos = self.game.getMinion(self)
  mech = hc.Minion('Damaged Golem',1,2,1,['Mech'])
  return self.game.summon(mech,pos)
addMinion('Harvest Golem',3,2,3,['Deathrattle','Mech'],[lambda m:Harvest_Golem_Deathrattle(m)])

#Combo effect
addSpell('Headcrack',3,'Rogue')

#This also can't summon on the enemy side
addMinion('Hogger',6,4,4)

def Holy_Fire(self,target):
  self.game.damage(target,5,True)
  self.game.damage(self.game.me,-5)
  return True
addSpell('Holy Fire',6,'Priest',['Spell','Target'],[lambda me,t:Holy_Fire(me,t)])

def Holy_Wrath(self,target,draw):
  return self.game.damage(target,draw[0].cost,True)
addSpell('Holy Wrath',5,'Paladin',['Spell','Draw','Target'],[lambda m,t,d:Holy_Wrath(m,t,d),{'Pool':'myDeck'}])

def Hungry_Crab_Battlecry(self,target):
  if 'Murloc' in target.effects:
    self.game.kill(target)
    self.game.buff(self,2,2)
  return True
addMinion('Hungry Crab',1,1,2,['Battlecry','Target'],[lambda m,t:Hungry_Crab_Battlecry(m,t)])

#Another secret I can't implement
addSpell('Ice Barrier',3,'Mage',['Secret'])

def Icicle(self,target,draw):
  self.game.damage(target,2)
  if 'Frozen' in target.effects:
    self.game.addToHand(draw[0])
addSpell('Icicle',2,'Mage',['Spell','Draw','Target'],[lambda m,t,d:Icicle(m,t,d),{'Pool':'myDeck'}])

def Illidan(self,origin):
  game = self.game
  pos = game.myBoard.index(self)
  flame =hc.Minion('Flame of Azzinoth',1,2,1)
  self.game.summon(flame,pos)
addMinion('Illidan Stormrage',6,7,5,['Play Card','Demon'],[lambda me,o:Illidan(me,o)])

def Imp_Master(self):
  self.game.damage(self,1)
  pos = self.game.getMinion(self)
  self.game.summon(hc.Minion('Imp',1,1,1,['Demon']),pos)
addMinion('Imp Master',3,1,5,['End of Turn'],[lambda m:Imp_Master(m)])

def Blademaster_Battlecry(self):
  self.game.damage(self,4)
addMinion('Injured Blademaster',3,4,7,['Battlecry'],[lambda m:Blademaster_Battlecry(m)])

def Inner_Fire(self,target):
  health = target.health
  atk = target.baseAtk
  target.buffAtk = health - atk
addSpell('Inner Fire',1,'Priest',['Spell','Target'],[lambda m,t:Inner_Fire(m,t)])

def Inner_Rage(self,target):
  self.game.damage(target,1,True)
  self.game.buff(target,2,0)
addSpell('Inner Rage',0,'Warrior',['Spell','Target'],[lambda m,t:Inner_Rage(m,t)])

def Ironbeak_Battlecry(self,target):
  self.game.silence(target)
addMinion('Ironbeak Owl',3,2,1,['Battlecry','Target','Beast'],[lambda m,t:Ironbeak_Battlecry(m,t)])

#Choose one effect
addMinion('Keeper of the Grove',4,2,2,mClass='Druid')

#Combo effect
addMinion('Kidnapper',6,5,3,mClass='Rogue')

def Banana(self,target):
  self.game.buff(target,1,1)
def Mukla_Battlecry(self):
  banana =hc.Spell('Bananas',1,'Neutral',['Spell','Target'],[lambda m,t:Banana(m,t)])
  for i in range(2):
    self.game.addToHand(banana,self.game.oppHand)
addMinion('King Mukla',3,5,5,['Battlecry','Beast'],[lambda m:Mukla_Battlecry(m)])

#Aura effect that I'm not sure how to implement yet
addMinion('Kirin Tor Mage',3,4,3,mClass='Mage')

#Random targeting effect outside of battlecry
addMinion('Knife Juggler',2,2,2)

def Lava_Burst(self,target):
  self.game.damage(target,5,True)
addSpell('Lava Burst',3,'Shaman',['Spell','Overload','Target'],[lambda m,t:Lava_Burst(m,t),2])

def Lay_On_Hands(self,target,draws):
  self.game.damage(target,-8)
  for i in draws:
    self.game.addToHand(i)
addSpell('Lay on Hands',8,'Paladin',['Spell','Draw','Target'],[lambda m,t,d:Lay_On_Hands(m,t,d),{'Pool':'myDeck','Count':lambda m:3}])

def Leeroy_Battlecry(self):
  whelp =hc.Minion('Whelp',1,1,1,['Dragon'])
  for i in range(2):
    self.game.summon(whelp,board=self.game.oppBoard)
  return True
addMinion('Leeroy Jenkins',5,6,2,['Battlecry','Charge'],[lambda m:Leeroy_Battlecry(m)])

def Leper_Deathrattle(self):
  game = self.game
  if self in game.myBoard:
    return game.damage(game.opponent,2)
  elif self in game.oppBoard:
    return game.damage(game.me,2)
  return False
addMinion('Leper Gnome',1,1,1,['Deathrattle'],[lambda m:Leper_Deathrattle(m)])

def Lightning_Bolt(self,target):
  self.game.damage(target,3,True)
  return True
addSpell('Lightning Bolt',1,'Shaman',['Spell','Overload','Target'],[lambda m,t:Lightning_Bolt(m,t),1])

#Not sure how best to code the random damage from Lightning Storm; for now it just deals a straight 2 damage
def Lightning_Storm(self):
  for i in self.game.oppBoard:
    self.game.damage(i,2,True)
  return True
addSpell('Lightning Storm',3,'Shaman',['Spell'],[lambda m:Lightning_Storm(m)])

def Lightspawn_Aura(self):
  self.buffAtk += self.health
addMinion('Lightspawn',4,0,5,['Aura'],[lambda m:Lightspawn_Aura(m)],mClass='Priest')

def Lightwarden(self):
  self.buffAtk += 2
addMinion('Lightwarden',1,1,2,['Heal'],[lambda m:Lightwarden(m)])

#Random targeting effect
addMinion('Lightwell',2,0,5,mClass='Priest')

#Draw effect in deathrattle
addMinion('Loot Hoarder',2,2,1)

#Hero powers are not yet implemented, so this card will change in the future
def Jaraxxus_Battlecry(self):
  jaraxxus = hc.Hero(hClass='Warlock',hGame=self.game)
  jaraxxus.maxHealth = 15
  jaraxxus.health = 15
  jaraxxus.mana = self.game.me.mana
  jaraxxus.maxMana = self.game.me.mana
  bigpunch = hc.Weapon('Blood Fury',3,3,8,wHero=jaraxxus,wClass='Warlock')
  jaraxxus.weapon = bigpunch
  self.game.me = jaraxxus
  return True
addMinion('Lord Jaraxxus',9,3,15,['Battlecry','Demon'],[lambda m:Jaraxxus_Battlecry(m)],mClass='Warlock')

def Lorewalker_Cho(self,origin):
  if isinstance(origin,hc.Spell):
    self.game.addToHand(origin,self.game.oppHand)
addMinion('Lorewalker Cho',2,0,4,['Play Card'],[lambda m,o:Lorewalker_Cho(m,o)])

#Mad Bomber has multiple random targets
addMinion('Mad Bomber',2,3,2)

#Not sure on the best way to code Mana Addict
addMinion('Mana Addict',2,1,3)

#Card draw from a non-battlecry effect
addMinion('Mana Tide Totem',3,0,3,mClass='Shaman')

#Weird aura effect
addMinion('Mana Wraith',2,2,2)

def Mana_Wyrm(self,origin):
  if isinstance(origin,hc.Spell) and self in self.game.myBoard:
    self.game.buff(self,1,0)
addMinion('Mana Wyrm',2,1,3,['Play Card'],[lambda m,o:Mana_Wyrm(m,o)],mClass='Mage')

#Choose One effect
addSpell('Mark of Nature',3,'Druid')

def Mass_Dispel(self):
  for i in self.game.oppBoard:
    self.game.silence(i)
  return True
addSpell('Mass Dispel',4,'Priest',['Spell'],[lambda m:Mass_Dispel(m)])

#Temporary effect; not sure how to implement
addMinion('Master of Disguise',4,4,4)

#Random targeting effect
addMinion('Master Swordsmith',2,1,3)

#This is a temporary aura that I don't know how to code but who gives a shit it's Millhouse Manastorm
addMinion('Millhouse Manastorm',2,4,4)

def MCTech_Battlecry(self,target):
  if len(self.game.oppBoard) >= 4:
    self.game.oppBoard.remove(target)
    self.game.myBoard.append(target)
  return True
addMinion('Mind Control Tech',3,3,3,['Battlecry','Target'],[lambda m,t:MCTech_Battlecry(m,t)])

def Mindgames(self,draw):
  self.game.summon(draw[0])
  return True
addSpell('Mindgames',4,'Priest',['Spell','Draw'],[lambda m,d:Mindgames(m,d),{'Pool':'oppDeck','Type':hc.Minion}])

#Another secret
addSpell('Mirror Entity',3,'Mage',['Secret'])

#And another secret
addSpell('Misdirection',2,'Hunter',['Secret'])

def Mortal_Strike(self,target):
  game = self.game
  if game.me.health <= 12:
    game.damage(target,6)
  else:
    game.damage(target,4)
  return True

def Mountain_Giant_Aura(self):
  game = self.game
  if self in game.myBoard:
    hand = game.myHand
  elif self in game.oppBoard:
    hand = game.oppHand
  else:
    return False
  for i in hand:
    if i != self:
      self.auraCost -= 1
addMinion('Mountain Giant',12,8,8,['Hand Aura','Elemental'],[lambda m:Mountain_Giant_Aura(m)])

def Tidecaller(self,origin):
  if 'Murloc' in origin.effects:
    self.game.buff(self,1,0)
addMinion('Murloc Tidecaller',1,1,2,['Summon','Murloc'],[lambda m,o:Tidecaller(m,o)])

def Warleader_Aura(self):
  game = self.game
  if self in game.myBoard:
    board = game.myBoard
  elif self in game.oppBoard:
    board = game.oppBoard
  for i in board:
    if 'Murloc' in i.effects:
      i.auraAtk += 2
addMinion('Murloc Warleader',3,3,3,['Aura','Murloc'],[lambda m:Warleader_Aura(m)])

#I have no idea how to code Nat Pagle but whatever no one plays him
addMinion('Nat Pagle',2,0,4)

#Naturalize doesn't work like the original card because all draws are based on player input, and the player can't see the opponent's cards. Might change later. 
def Naturalize(self,target):
  return self.game.kill(target)
addSpell('Naturalize',1,'Druid',['Spell','Target'],[lambda m,t:Naturalize(m,t)])

#Aaaand another secret
addSpell('Noble Sacrifice',1,'Paladin',['Secret'])

#Choose One effect
addSpell('Nourish',6,'Druid')

#Need to check which side Onyxia summons on first in game
def Onyxia_Battlecry(self):
  whelp =hc.Minion('Whelp',1,1,1,['Dragon'])
  pos = self.game.getMinion(self)
  while len(self.game.myBoard) < 7:
    self.game.summon(whelp,pos)
    pos += 1
    self.game.summon(whelp,pos)
    pos -= 1
  return True
addMinion('Onyxia',9,8,8,['Battlecry'],[lambda m:Onyxia_Battlecry(m)])

#Combo card alert
addWeapon("Perdition's Blade",3,2,2,wClass='Rogue')

#How to use opponent's class?
def Pilfer(self,draw):
  self.game.addToHand(draw[0])
addSpell('Pilfer',1,'Rogue',['Spell','Draw'],[lambda m,d:Pilfer(m,d),lambda m:1])

def Summoner_Start(self):
  if self in self.game.myBoard:
    self.enable = True
    return True
  return False
def Summoner_Aura(self):
  for i in self.game.myHand:
    if isinstance(i,hc.Minion) and self.enable:
      i.auraCost -= 2
  return True
def Summoner_End(self,origin):
  if isinstance(origin,hc.Minion):
    self.enable = False
  return True
addMinion('Pint-Sized Summoner',2,2,2,['Start of Turn','Aura','Play Card'],[lambda m:Summoner_Start(m),lambda m:Summoner_Aura(m),lambda m:Summoner_End(m)])

def Pit_Lord_Battlecry(self):
  self.game.damage(self.game.me,5)
  return True
addMinion('Pit Lord',4,5,6,['Battlecry','Demon'],[lambda m:Pit_Lord_Battlecry(m)],mClass='Warlock')

#Choose one effect
addSpell('Power of the Wild',2,'Druid')

#Preparation is a weird aura that idk how to code
addSpell('Preparation',0,'Rogue')

def Priestess_Battlecry(self):
  self.game.damage(self.game.me,-4)
  return True
addMinion('Priestess of Elune',6,5,4,['Battlecry'],[lambda m:Priestess_Battlecry(m)])

#Prophet Velen is another weird aura
addMinion('Prophet Velen',7,7,7,mClass='Priest')

def Pyroblast(self,target):
  self.game.damage(target,10,True)
  return True
addSpell('Pyroblast',10,'Mage',['Spell','Target'],[lambda m,t:Pyroblast(m,t)])

def Adventurer(self,origin):
  game = self.game
  if self in game.myBoard:
    game.buff(self,1,1)
    return True
  return False
addMinion('Questing Adventurer',3,2,2,['Play Card'],[lambda m,o:Adventurer(m,o)])

#This one has Windfury while damaged, so not sure how to do that exactly
def Raging_Worgen_Aura(self):
  if self.health < self.maxHealth:
    self.auraAtk += 1
    return True
  return False
addMinion('Raging Worgen',3,3,3,['Aura'],[lambda m:Raging_Worgen_Aura(m)])

def Rampage(self,target):
  if target.health < target.maxHealth:
    self.game.buff(target,3,3)
    return True
  return False

#Secret
addSpell('Redemption',1,'Paladin',['Secret'])

#Secret again
addSpell('Repentance',1,'Paladin',['Secret'])

def Savagery(self,target):
  dmg = self.game.me.atk
  if isinstance(target,hc.Minion):
    self.game.damage(target,dmg,True)
    return True
  return False
addSpell('Savagery',1,'Druid',['Spell','Target'],[lambda m,t:Savagery(m,t)])

def Highmane_Deathrattle(self):
  game = self.game
  position = game.myBoard.index(self)
  hyena =hc.Minion("Hyena",2,2,2,['Beast'])
  for i in range(0,2):
    game.summon(hyena,position)
  return True
addMinion("Savannah Highmane",6,6,5,['Deathrattle','Beast'],[lambda me:Highmane_Deathrattle(me)],mClass='Hunter')

#Need to change this card to only trigger on a friendly beast
def Scavenging_Hyena(self,origin):
  if 'Beast' in origin.effects:
    self.game.buff(self,2,1)
addMinion('Scavenging Hyena',2,2,2,['Death'],[lambda m,o:Scavenging_Hyena(m,o)],mClass='Hunter')

def Sea_Giant_Aura(self):
  board = self.game.getBoard(self)
  for i in board:
    self.auraCost -= 1
addMinion('Sea Giant',10,8,8,['Hand Aura'],[lambda m:Sea_Giant_Aura(m)])

def Secretkeeper(self,origin):
  if 'Secret' in origin.effects:
    self.game.buff(self,1,1)
addMinion('Secretkeeper',1,1,2,['Play Card'],[lambda m,o:Secretkeeper(m,o)])

def Sense_Demons(self,draws):
  for i in draws:
    self.game.addToHand(i)
  return True
addSpell('Sense Demons',3,'Warlock',['Spell','Draw'],[lambda m,d:Sense_Demons(m,d),{'Pool':'myDeck','Count':lambda m:2,'Effects':['Demon']}])

#Shadow Madness has a weird temporary effect
addSpell('Shadow Madness',4,'Priest')

def Shadowflame(self,target):
  if target in self.game.myBoard:
    dmg = target.atk
    for i in self.game.oppBoard:
      self.game.damage(i,dmg,True)
    self.game.kill(target)
    return True
  return False
addSpell('Shadowflame',4,'Warlock',['Spell','Target'],[lambda m,t:Shadowflame(m,t)])

#Hero Powers aren't implemented
addSpell('Shadowform',3,'Priest')

#Copying is weird rn so this card might change
def Shadowstep(self,target):
  if target in self.game.myBoard:
    self.game.myBoard.remove(target)
    target.buffAtk = 0
    target.buffHealth = 0
    target.auraAtk = 0
    target.auraHealth = 0
    target.damage = 0
    self.game.addToHand(target)
    self.game.buff(target,0,0,-2)
    return True
  return False
addSpell('Shadowstep',0,'Rogue',['Spell','Target'],[lambda m,t:Shadowstep(m,t)])

def Shield_Slam(self,target):
  if target.isinstance(hc.Minion):
    self.game.damage(target,self.game.me.armor,True)
    return True
  return False
addSpell('Shield Slam',1,'Warrior',['Spell','Target'],[lambda m,t:Shield_Slam(m,t)])

#Combo
addMinion('SI:7 Agent',3,3,3)

addSpell('Silence',0,'Priest',['Spell','Target'],[lambda m,t:m.game.silence(t)])

def Silver_Knight_Battlecry(self):
  pos = self.game.findMinion(self)
  self.game.summon(hc.Minion('Squire',2,2,2),pos)
  return True
addMinion('Silver Hand Knight',5,4,4,['Battlecry'],[lambda m:Silver_Knight_Battlecry(m)])

def Siphon_Soul(self,target):
  self.game.kill(target)
  self.game.damage(self.game.me,-3)
  return True
addSpell('Siphon Soul',6,'Warlock',['Spell','Target'],[lambda m,t:Siphon_Soul(m,t)])

def Slam(self,target,draw):
  self.game.damage(target,2,True)
  if(target.health > 0):
    self.game.addToHand(draw[0])
  return True
addSpell('Slam',2,'Warrior',['Spell','Draw','Target'],[lambda m,t,d:Slam(m,t,d),{'Pool':'myDeck'}])

#Secret
addSpell('Snake Trap',2,'Hunter',['Secret'])

#Another secret
addSpell('Snipe',2,'Hunter',['Secret'])

#Aura that I don't know how to code
addMinion("Sorcerer's Apprentice",2,3,2,mClass='Mage')

#Gives a deathrattle; need a way to add effects
addSpell('Soul of the Forest',4,'Druid')

def Captain_Aura(self):
  game = self.game
  if self in game.myBoard:
    board = game.myBoard
  elif self in game.oppBoard:
    board = game.oppBoard
  for i in board:
    if 'Pirate' in i.effects:
      i.auraAtk += 1
      i.auraHealth += 1
addMinion('Southsea Captain',3,3,3,['Aura','Pirate'],[lambda m:Captain_Aura(m)])

#Don't know how to make a minion that only sometimes has charge; need to figure out better auras
addMinion('Southsea Deckhand',1,2,1,['Pirate'])

#Secret again
addSpell('Spellbender',3,'Mage',['Secret'])

def Spellbreaker_Battlecry(self,target):
  self.game.silence(target)
  return True
addMinion('Spellbreaker',4,4,3,['Battlecry','Target'],[lambda m,t:Spellbreaker_Battlecry(m,t)])

def Spiteful_Enrage(self):
  if self.damage < 0 and self.game.checkWeapon(self.game.me):
    self.game.me.weapon.auraAtk += 2
addMinion('Spiteful Smith',5,4,6,['Aura'],[lambda m:Spiteful_Enrage(m)])

def Kodo_Battlecry(self,target):
  if target.atk <= 2:
    self.game.kill(target)
    return True
  return False
addMinion('Stampeding Kodo',5,3,5,['Battlecry','Target'],[lambda m,t:Kodo_Battlecry(m,t)])

#Choose One
addSpell('Starfall',5,'Druid')

def Portal_Aura(self):
  game = self.game
  if self in game.myBoard:
    hand = game.myHand
  elif self in game.oppBoard:
    hand = game.oppHand
  else:
    return False
  for i in hand:
    count = 0
    while i.baseCost + i.buffCost + i.auraCost > 1 and count < 2:
      i.auraCost -= 1
      count += 1
addMinion('Summoning Portal',4,0,4,['Aura'],[lambda m:Portal_Aura(m)])

def Sunfury_Battlecry(self):
  targets = self.game.getAdjacent(self)
  for i in targets:
    i.effects['Taunt'] = None
  return True
addMinion('Sunfury Protector',2,2,3,['Battlecry'],[lambda m:Sunfury_Battlecry(m)])

def Sword_of_Justice(self,origin):
  self.game.buff(origin,1,1)
  self.game.damage(self,1)
addWeapon('Sword of Justice',3,1,5,['Summon'],[lambda me,o:Sword_of_Justice(me,o)])

def Tauren_Enrage(self):
  if self.damage < 0:
    self.auraAtk += 3
addMinion('Tauren Warrior',3,2,3,['Aura','Taunt'],[lambda m:Tauren_Enrage(m)])

def Enforcer_Battlecry(self,target):
  if target in self.game.myBoard:
    self.game.buff(target,0,3)
    return True
  return False
addMinion('Temple Enforcer',6,6,6,['Battlecry','Target'],[lambda m,t:Enforcer_Battlecry(m,t)])

def Beast_Deathrattle(self):
  game = self.game
  board = self.game.getBoard(self)
  finkle =hc.Minion('Finkle Einhorn',3,3,3)
  game.summon(finkle,board=board)
addMinion('The Beast',6,9,7,['Deathrattle','Beast'],[lambda m:Beast_Deathrattle(m)])

def Black_Knight_Battlecry(self,target):
  if 'Taunt' in target.effects:
    self.game.kill(target)
    return True
  return False
addMinion('The Black Knight',6,4,5,['Battlecry'],[lambda m,t:Black_Knight_Battlecry(m,t)])

def Thoughtsteal(self,draws):
  succ = False
  for i in draws:
    if self.game.addToHand(i):
      succ = True
  return succ
addSpell('Thoughtsteal',3,'Priest',['Spell','Draw'],[lambda m,d:Thoughtsteal(m,d),{'Pool':'oppDeck','Count':lambda m:2}])

#Don't know how to take the additional input needed for Overspark to work; might just use an input here because I don't really need to predict this type of random effect.
addMinion('Tinkmaster Overspark',3,3,3)

def Tirion_Deathrattle(self):
  game = self.game
  if self in game.myBoard:
    hero = game.me
  elif self in game.oppBoard:
    hero = game.opponent
  game.equip(hc.Weapon('Ashbringer',5,5,3),hero)
addMinion('Tirion Fordring',8,6,6,['Deathrattle','Divine Shield','Taunt'],[lambda me:Tirion_Deathrattle(me)])

def Tome_of_Intellect(self,draw):
  self.game.addToHand(draw[0])
addSpell('Tome of Intellect',1,'Mage',['Spell','Draw'],[lambda m,d:Tome_of_Intellect(m,d),{'Pool':'Random', 'Class':'Mage'}])

def Twilight_Drake_Battlecry(self):
  game = self.game
  game.buff(self,0,len(game.myHand))
addMinion('Twilight Drake',4,4,1,['Battlecry','Dragon'],[lambda m:Twilight_Drake_Battlecry(m)])

def Twisting_Nether(self):
  for i in self.game.summonOrder:
    self.game.kill(i)

def Unbound(self,origin):
  if 'Overload' in origin.effects and self in self.game.myBoard:
    self.game.buff(self,1,1)
addMinion('Unbound Elemental',3,2,4,['Play Card'],[lambda m,o:Unbound(m,o)])

def Unleash_the_Hounds(self):
  size = len(self.game.oppBoard)
  if size <= 0 or len(self.game.myBoard) >= 7: return False
  hound =hc.Minion("Hound",1,1,1,['Charge','Beast'])
  for i in range(0,size):
    self.game.summon(hound)
  return True
addSpell('Unleash the Hounds',3,'Hunter',['Spell'],[lambda me:Unleash_the_Hounds(me)])

def Upgrade(self):
  game = self.game
  if game.checkWeapon(game.me):
    game.buff(game.me.weapon,1,1)
  else:
    game.equip(hc.Weapon('Heavy Axe',1,1,3))
addSpell('Upgrade!',1,'Warrior',['Spell'],[lambda m:Upgrade(m)])

#Secret
addSpell('Vaporize',3,'Mage',['Secret'])

def Mercenary_Aura(self):
  game = self.game
  if self in game.myBoard:
    hand = game.myHand
  elif self in game.oppBoard:
    hand = game.oppHand
  else:
    return False
  for i in hand:
    i.auraCost += 3
addMinion('Venture Co. Mercenary',5,7,6,['Aura'],[lambda m:Mercenary_Aura(m)])

def Violet_Teacher(self,origin):
  if isinstance(origin,hc.Spell) and self in self.game.myBoard:
    self.game.summon(hc.Minion('Violet Apprentice',1,1,1))
addMinion('Violet Teacher',4,3,5,['Play Card'],[lambda m,o:Violet_Teacher(m,o)])

def Void_Terror_Battlecry(self):
  targets = self.game.getAdjacent(self)
  for i in targets:
    self.game.buff(self,i.atk,i.health)
    self.game.kill(i)
addMinion('Void Terror',3,3,3,['Battlecry','Demon'],[lambda m:Void_Terror_Battlecry(m)])

def Wild_Pyro(self,origin):
  if isinstance(origin,hc.Spell) and self in self.game.myBoard:
    for i in self.game.summonOrder:
      self.game.damage(i,1)
addMinion('Wild Pyromancer',2,3,2,['Play Card'],[lambda m,o:Wild_Pyro(m,o)])

#Choose One
addSpell('Wrath',2,'Druid')

#Random targeting effect
addMinion('Young Priestess',1,2,1)

#Draw effect at end of turn; also need to add all the dream cards
addMinion('Ysera',9,4,12,['Dragon'])

addMinion("Dire Mole",1,1,3,['Beast'])
addMinion("Ironfur Grizzly",3,3,3,["Taunt",'Beast'])
addMinion("Al'Akir the Windlord",8,3,5,['Windfury','Charge','Divine Shield','Taunt','Elemental'])
addMinion('Ancient Watcher',2,4,5,["Can't attack"])
addMinion('Argent Commander',6,4,2,['Charge','Divine Shield'])
addMinion('Argent Squire',1,1,1,['Divine Shield'])
addMinion('Emperor Cobra',3,2,3,['Poisonous'])
addMinion('Faerie Dragon',2,3,2,['Elusive','Dragon'])
addMinion('Fen Creeper',5,3,6,['Taunt'])
addMinion('Jungle Panther',3,4,2,['Stealth','Beast'])
addMinion('King Krush',9,8,8,['Charge'],mClass='Hunter')
addMinion("Mogu'shan Warden",4,1,7,['Taunt'])
addMinion('Nozdormu',9,8,8,['Dragon'])
addMinion('Patient Assassin',2,1,1,['Stealth','Poisonous'],mClass='Rogue')
addMinion('Ravenholdt Assassin',7,7,5,['Stealth'])
addMinion('Scarlet Crusader',3,3,1,['Divine Shield'])
addMinion('Shieldbearer',1,0,4,['Taunt'])
addMinion('Silvermoon Guardian',4,3,3,['Divine Shield'])
addMinion('Stranglethorn Tiger',5,5,5,['Stealth'])
addMinion('Sunwalker',6,4,5,['Taunt','Divine Shield'])
addMinion('Thrallmar Farseer',3,2,3,['Windfury'])
addMinion('Windfury Harpy',6,4,5,['Windfury'])
addMinion('Wisp',0,1,1)
addMinion('Worgen Infiltrator',1,2,1,['Stealth'])
addMinion('Young Dragonhawk',1,1,1,['Windfury','Beast'])
#Spell damage not implemented; putting SD cards here for now
addMinion('Malygos',9,4,12,['Spell Damage','Dragon'],[5])
#All my overload cards that don't have a function will go here for now. 
addWeapon('Doomhammer',5,2,8,['Overload','Windfury'],[2],wClass='Shaman')
addMinion('Dust Devil',1,3,1,['Overload','Windfury'],[2])
addMinion('Earth Elemental',5,7,8,['Overload','Taunt'],[3])
addWeapon('Stormforged Axe',2,2,3,['Overload'],[1])

#--------------------Uncollectible classic cards--------------------

def Dream(self,target):
  if target in self.game.myBoard:
    hand = self.game.myHand
    board = self.game.myBoard
  elif target in self.game.oppBoard:
    hand = self.game.oppHand
    board = self.game.oppBoard
  else:
    return False
  board.remove(target)
  self.game.addToHand(target,hand)
  return True
addSpell('Dream',0,'Dream',['Spell','Target'],[lambda m,t:Dream(m,t)])

#Need to be able to add an effect as a buff
def Nightmare(self,target):
  self.game.buff(target,5,5)
  return True
addSpell('Nightmare',0,'Dream',['Spell','Target'],[lambda m,t:Nightmare(m,t)])

def Ysera_Awakens(self):
  for i in self.game.summonOrder:
    if i.name != 'Ysera':
      self.game.damage(i,5,True)
  self.game.damage(self.game.me,5,True)
  self.game.damage(self.game.opponent,5,True)
addSpell('Ysera Awakens',2,'Dream',['Spell'],[lambda m:Ysera_Awakens(m)])

addMinion('Emerald Drake',4,7,6,['Dragon'],mClass='Dream')
addMinion('Laughing Sister',3,3,5,['Elusive'],mClass='Dream')

addMinion('Wolf',3,3,3,['Beast'])
addMinion('Baine Bloodhoof',4,4,5)
addMinion('Spirit Wolf',2,2,3,['Taunt'])
addMinion('Treant',2,2,2)
addMinion('Damaged Golem',1,2,1,['Mech'])
addMinion('Flame of Azzinoth',1,2,1)
addMinion('Imp',1,1,1,['Demon'])
addMinion('Whelp',1,1,1,['Dragon'])
addMinion('Hyena',2,2,2,['Beast'])
addMinion('Squire',2,2,2)
addMinion('Finkle Einhorn',3,3,3)
addMinion('Hound',1,1,1,['Charge','Beast'])
addMinion('Violet Apprentice',1,1,1)
addWeapon('Battle Ax',1,2,2,wClass='Warrior')
addWeapon('Ashbringer',5,5,3)
addWeapon('Heavy Axe',1,1,3)

#-------------Basic cards--------------

def Swamp_Ooze_Battlecry(self):
  if self.game.checkWeapon(self.game.opponent):
    self.game.kill(self.game.opponent.weapon)
  return True
addMinion('Acidic Swamp Ooze',2,3,2,['Battlecry'],[lambda m:Swamp_Ooze_Battlecry(m)])

#Adds an effect as a buff; this particular one shouldn't cause problems though
def Ancestral_Healing(self,target):
  self.game.damage(target,target.damage)
  self.game.addEffect(target,'Taunt')
addSpell('Ancestral Healing',0,'Shaman',['Spell','Target'],[lambda m,t:Ancestral_Healing(m,t)])

#Need to add the animal companions as uncollectibles; need to figure out how to draw them also
def Animal_Companion(self,draw):
  self.game.summon(draw[0])
  return True
addSpell('Animal Companion',3,'Hunter',['Spell','Draw'],[lambda m,d:Animal_Companion(m,d),lambda m:1])

def Arcane_Explosion(self):
  for i in self.game.oppBoard:
    self.game.damage(i,1,True)
addSpell('Arcane Explosion',2,'Mage',['Spell'],[lambda m:Arcane_Explosion(m)])

def Intellect(self,draws):
  for i in draws:
    if self.game.addToHand(i):
      succ = True
  return succ
addSpell('Arcane Intellect',3,'Mage',['Spell','Draw'],[lambda m,d:Intellect(m,d),{'Pool':'myDeck','Count':lambda m:2}])

#3 random targets
addSpell('Arcane Missiles',1,'Mage')

def Arcane_Shot(self,target):
  self.game.damage(target,2,True)
  return True
addSpell('Arcane Shot',1,'Hunter',['Spell','Target'],[lambda m,t:Arcane_Shot(m,t)])

def Assassinate(self,target):
  return self.game.kill(target)
addSpell('Assassinate',5,'Rogue',['Spell','Target'],[lambda m,t:Assassinate(m,t)])

def Backstab(self,target):
  if target.damage <= 0:
    self.game.damage(target,2,True)
    return True
  return False
addSpell('Backstab',0,'Rogue',['Spell','Target'],[lambda m,t:Backstab(m,t)])

def Blessing_of_Kings(self,target):
  self.game.buff(target,4,4)
  return True
addSpell('Blessing of Kings',4,'Paladin',['Spell','Target'],[lambda m,t:Blessing_of_Kings(m,t)])

def Blessing_of_Might(self,target):
  self.game.buff(target,3,0)
addSpell('Blessing of Might',1,'Paladin',['Spell','Target'],[lambda m,t:Blessing_of_Might(m,t)])

#Temporary buff; not sure how to do this
addSpell('Bloodlust',5,'Shaman')

#Temporary effect; can't attack heroes for 1 turn. Needs to be separate from rush. 
addSpell('Charge',1,'Warrior')

def Claw(self):
  game = self.game
  game.me.armor += 2
  game.me.atk += 2
addSpell('Claw',1,'Druid',['Spell'],[lambda m:Claw(m)])

#Multi target
addSpell('Cleave',2,'Warrior')

def Consecration(self):
  for i in self.game.oppBoard:
    self.game.damage(i,2,True)
addSpell('Consecration',4,'Paladin',['Spell'],[lambda m:Consecration(m)])

#Not sure how to code corruption
addSpell('Corruption',1,'Warlock')

def Darkscale_Battlecry(self):
  self.game.damage(self.game.me,-2)
  for i in self.game.myBoard:
    self.game.damage(i,-2)
  return True
addMinion('Darkscale Healer',5,4,5,['Battlecry'],[lambda m:Darkscale_Battlecry(m)])

addSpell('Deadly Poison',1,'Rogue',['Spell'],[lambda m:m.game.buff(m.game.me.weapon,2,0)])

def Divine_Spirit(self,target):
  self.game.buff(target,0,target.health)
addSpell('Divine Spirit',2,'Priest',['Spell','Target'],[lambda m,t:Divine_Spirit(m,t)])

def Mechanic_Battlecry(self):
  pos = self.game.findMinion(self)
  dragonling = hc.Minion('Mechanical Dragonling',2,2,1,['Mech'])
  self.game.summon(dragonling,pos)
addMinion('Dragonling Mechanic',4,2,4,['Battlecry'],[lambda m:Mechanic_Battlecry(m)])

def Drain_Life(self,target):
  self.game.damage(target,2,True)
  self.game.damage(self.game.me,-2)
addSpell('Drain Life',3,'Warlock',['Spell','Target'],[lambda m,t:Drain_Life(m,t)])

def Dread_Infernal_Battlecry(self):
  for i in self.game.summonOrder:
    self.game.damage(i,1)
  self.game.damage(self.game.me,1)
  self.game.damage(self.game.opponent,1)
addMinion('Dread Infernal',6,6,6,['Battlecry'],[lambda m:Dread_Infernal_Battlecry(m)])

addMinion('Elven Archer',1,1,1,['Battlecry','Target'],[lambda m,t:m.game.damage(t,1)])

def Execute(self,target):
  if target.damage < 0:
    self.game.kill(target)
    return True
  return False
addSpell('Execute',2,'Warrior',['Spell','Target'],[lambda m,t:Execute(m,t)])

def Fan_of_Knives(self,draw):
  for i in self.game.oppBoard:
    self.game.damage(i,1,True)
  self.game.addToHand(draw[0])
addSpell('Fan of Knives',3,'Rogue',['Spell','Draw'],[lambda m,d:Fan_of_Knives(m,d),{'Pool':'myDeck'}])

addMinion('Fire Elemental',6,6,5,['Battlecry','Target'],[lambda m,t:m.game.damage(t,3)])

def Fireball(self,target):
  self.game.damage(target,6,True)
  return True
addSpell('Fireball',4,'Mage',['Spell','Target'],[lambda me,target:Fireball(me,target)])

def Flamestrike(self):
  for i in self.game.oppBoard:
    self.game.damage(i,4,True)
  return True
addSpell('Flamestrike',7,'Mage',['Spell'],[lambda m:Flamestrike(m)])

def Flametongue_Aura(self):
  targets = self.game.getAdjacent(self)
  for i in targets:
    i.auraAtk += 2
  return True
addMinion('Flametongue Totem',3,0,3,['Aura'],[lambda m:Flametongue_Aura(m)])

def Frost_Nova(self):
  for i in self.game.oppBoard:
    self.game.addEffect(i,'Frozen')
  return True
addSpell('Frost Nova',3,'Mage',['Spell'],[lambda m:Frost_Nova(m)])

def Frost_Shock(self,target):
  if target in self.game.oppBoard:
    self.game.damage(target,1)
    self.game.addEffect(target,'Frozen')
    return True
  return False
addSpell('Frost Shock',1,'Shaman',['Spell','Target'],[lambda m,t:Frost_Shock(m,t)])

def Frostbolt(self,target):
  self.game.damage(target,3,True)
  self.game.addEffect(target,'Frozen')
addSpell('Frostbolt',2,'Mage',['Spell','Target'],[lambda m,t:Frostbolt(m,t)])

def Frostwolf_Warlord_Battlecry(self):
  for i in self.game.myBoard:
    self.game.buff(self,1,1)
addMinion('Frostwolf Warlord',5,4,4,['Battlecry'],[lambda m:Frostwolf_Warlord_Battlecry(m)])

addMinion('Gnomish Inventor',4,2,4,['Battlecry','Draw'],[lambda m,d:m.game.addToHand(d[0]),{'Pool':'myDeck'}])

def Grimscale_Aura(self):
  for i in self.game.myBoard:
    if 'Murloc' in i.effects:
      i.auraAtk += 1
addMinion('Grimscale Oracle',1,1,1,['Aura','Murloc'],[lambda m:Grimscale_Aura(m)])

def Guardian_Battlecry(self):
  self.game.damage(self.game.me,-6)
addMinion('Guardian of Kings',7,5,6,['Battlecry'],[lambda m:Guardian_Battlecry(m)])

def Gurubashi_Berserker(self,origin):
  if origin == self:
    self.game.buff(self,3,0)
addMinion('Gurubashi Berserker',5,2,7,['Damage'],[lambda m,o:Gurubashi_Berserker(m,o)])

def Hammer_of_Wrath(self,target,draw):
  self.game.damage(target,3,True)
  self.game.addToHand(draw[0])
addSpell('Hammer of Wrath',4,'Paladin',['Spell','Draw','Target'],[lambda m,t,d:Hammer_of_Wrath(m,t,d),{'Pool':'myDeck'}])

addSpell('Hand of Protection',1,'Paladin',['Battlecry','Target'],[lambda m,t:m.game.addEffect(t,'Divine Shield')])

addSpell('Healing Touch',3,'Druid',['Spell','Target'],[lambda m,t:m.game.damage(t,-8)])

def Hellfire(self):
  self.game.damage(self.game.me,3,True)
  self.game.damage(self.game.opponent,3,True)
  for i in self.game.summonOrder:
    self.game.damage(i,3)
  return True
addSpell('Hellfire',4,'Warlock',['Spell'],[lambda m:Hellfire(m)])

addSpell('Heroic Strike',2,'Warrior',['Spell'],[lambda m:m.game.buff(m.game.me,4,0)])

#I don't know how to code transformation spells big oof
addSpell('Hex',4,'Shaman')

addSpell('Holy Light',2,'Paladin',['Spell','Target'],[lambda m,t:m.game.damage(t,-6)])

def Holy_Nova(self):
  for i in self.game.myBoard:
    self.game.damage(i,-2)
  self.game.damage(self.game.me,-2)
  for i in self.game.oppBoard:
    self.game.damage(i,2,True)
  self.game.damage(self.game.opponent,2,True)
addSpell('Holy Nova',5,'Priest',['Spell'],[lambda m:Holy_Nova(m)])

addSpell('Holy Smite',1,'Priest',['Spell','Target'],[lambda m,t:m.game.damage(t,2,True)])

def Houndmaster_Battlecry(self,target):
  if 'Beast' in target.effects and target in self.game.myBoard:
    self.game.buff(target,2,2)
    self.game.addEffect(target,'Taunt')
    return True
  return False
addMinion("Houndmaster",4,4,3,["Battlecry",'Target'],[lambda me,target:Houndmaster_Battlecry(me,target)],mClass='Hunter')

def Humility(self,target):
  target.buffAtk = -(target.baseAtk - 1)
addSpell('Humility',1,'Paladin',['Spell','Target'],[lambda m,t:Humility(m,t)])

def Hunters_Mark(self,target):
  target.buffHealth = -(target.baseHealth - 1)
  target.damage = 0
addSpell("Hunter's Mark",2,'Hunter')

#Should implement a way to add mana without going over 10
def Innervate(self):
  self.game.me.mana += 1
addSpell('Innervate',0,'Druid',['Spell'],[lambda m:Innervate(m)])

addMinion('Ironforge Rifleman',3,2,2,['Battlecry'],[lambda m,t:m.game.damage(t,1)])

def Kill_Command(self,target):
  game = self.game
  beast = False
  for i in game.myBoard:
    if 'Beast' in i.effects: beast = True
  if beast: game.damage(target,5,True)
  else: game.damage(target,3,True)
  return True
addSpell("Kill Command",3,'Hunter',["Spell",'Target','Damage'],[lambda me,target:Kill_Command(me,target)])

def Mark_of_the_Wild(self,target):
  self.game.addEffect(target,'Taunt')
  self.game.buff(target,2,2)
  return True
addSpell('Mark of the Wild',2,'Druid',['Spell','Target'],[lambda m,t:Mark_of_the_Wild(m,t)])

addSpell('Mind Blast',2,'Priest',['Spell'],[lambda m:m.game.damage(m.game.opponent,5,True)])

def Mind_Control(self,target):
  game = self.game
  if target not in game.oppBoard:
    return False
  game.oppBoard.remove(target)
  game.myBoard.append(target)
  return True
addSpell('Mind Control',10,'Priest',['Spell','Target'],[lambda m,t:Mind_Control(m,t)])

def Mind_Vision(self,draw):
  self.game.addToHand(draw[0])
  return True
addSpell('Mind Vision',1,'Priest',['Spell','Draw'],[lambda m,d:Mind_Vision(m,d),{'Pool':'oppHand'}])

def Mirror_Image(self):
  image =hc.Minion('Mirror Image',0,0,2,['Taunt'])
  for i in range(2):
    self.game.summon(image)
  return True
addSpell('Mirror Image',1,'Mage',['Spell'],[lambda m:Mirror_Image(m)])

addSpell('Moonfire',0,'Druid',['Spell','Target'],[lambda m,t:m.game.damage(t,1,True)])

def Mortal_Coil(self,target,draw):
  self.game.damage(target,1,True)
  if target.health <= 0:
    self.game.addToHand(draw[0])
addSpell('Mortal Coil',1,'Warlock',['Spell','Draw','Target'],[lambda m,t,d:Mortal_Coil(m,t,d),{'Pool':'myDeck'}])

#Multiple random targets
addSpell('Multi-Shot',4,'Hunter')

def Tidehunter_Battlecry(self):
  pos = self.game.findMinion(self)
  self.game.summon(hc.Minion('Murloc Scout',1,1,1,['Murloc']),pos)
  return True
addMinion('Murloc Tidehunter',2,2,1,['Battlecry','Murloc'],[lambda m:Tidehunter_Battlecry(m)])

addMinion('Nightblade',5,4,4,['Battlecry'],[lambda m:m.game.damage(m.game.opponent,3)])

#Draw effect outside of battlecry
addMinion('Northshire Cleric',1,1,3,mClass='Priest')

addMinion('Novice Engineer',2,1,1,['Battlecry','Draw'],[lambda m,d:m.game.addToHand(d[0]),{}])

#How do i do transformations?????
addSpell('Polymorph',4,'Mage')

def PW_Shield(self,target,draw):
  self.game.buff(target,0,2)
  self.game.addToHand(draw[0])
addSpell('Power Word: Shield',1,'Priest',['Spell','Draw','Target'],[lambda m,t,d:PW_Shield(m,t,d),{}])

def Raid_Leader_Aura(self):
  game = self.game
  if self in game.myBoard:
    board = game.myBoard
  elif self in game.oppBoard:
    board = game.oppBoard
  else:
    return False
  for i in board:
    i.auraAtk += 1
addMinion('Raid Leader',3,2,2,['Aura'],[lambda m:Raid_Leader_Aura(m)])

def Razorfen_Battlecry(self):
  pos = self.game.findMinion(self)
  self.game.summon(hc.Minion('Boar',1,1,1,['Beast']),pos)
addMinion('Razorfen Hunter',3,2,3,['Battlecry'],[lambda m:Razorfen_Battlecry(m)])

#One-turn effect?
def Rockbiter_Weapon(self,target):
  self.game.buff(target,3,0)

def Sac_Pac(self,target):
  if 'Demon' in target.effects:
    self.game.kill(target)
    self.game.damage(self.game.me,-5)
    return True
  return False
addSpell('Sacrificial Pact',0,'Warlock',['Spell','Target'],[lambda m,t:Sac_Pac(m,t)])

def Sap(self,target):
  if target in self.game.oppBoard:
    self.game.kill(target,False)
    self.game.addToHand(target,self.game.oppHand)
    return True
  return False
addSpell('Sap',2,'Rogue',['Spell','Target'],[lambda m,t:Sap(m,t)])

#Another temporary buff
def Savage_Roar(self):
  for i in self.game.myBoard:
    self.game.buff(i,2,0)
  self.game.buff(self.game.me,2,0)
addSpell('Savage Roar',3,'Druid',['Spell'],[lambda m:Savage_Roar(m)])

def Shadow_Bolt(self,target):
  if isinstance(target,hc.Minion):
    return self.game.damage(target,4,True)
  return False
addSpell('Shadow Bolt',3,'Warlock',['Spell','Target'],[lambda m,t:Shadow_Bolt(m,t)])

def SW_Death(self,target):
  if isinstance(target,hc.Minion) and target.atk >= 5:
    self.game.kill(target)
    return True
  return False
addSpell('Shadow Word: Death',3,'Priest',['Spell','Target'],[lambda m,t:SW_Death(m,t)])

def SW_Pain(self,target):
  if isinstance(target,hc.Minion) and target.atk <= 3:
    self.game.kill(target)
    return True
  return False
addSpell('Shadow Word: Pain',2,'Priest',['Spell','Target'],[lambda m,t:SW_Pain(m,t)])

addMinion('Shattered Sun Cleric',3,3,2,['Battlecry','Target'],[lambda m,t:m.game.buff(t,1,1)])

def Shield_Block(self,draw):
  self.game.me.armor += 5
  self.game.addToHand(draw[0])
  return True
addSpell('Shield Block',3,'Warrior',['Spell','Draw'],[lambda m,d:Shield_Block(m,d),{}])

def Shiv(self,target,draw):
  self.game.damage(target,1,True)
  self.game.addToHand(draw[0])
  return True
addSpell('Shiv',2,'Rogue',['Spell','Draw','Target'],[lambda m,t,d:Shiv(m,t,d),{}])

addSpell('Sinister Strike',1,'Rogue',['Spell'],[lambda m:m.game.damage(m.game.opponent,3,True)])

def Soulfire(self,target,draw):
  self.game.damage(target,4,True)
  if draw[0] in self.game.myHand:
    self.game.discard(draw[0])
  return True
addSpell('Soulfire',1,'Warlock',['Spell','Draw','Target'],[lambda m,t,d:Soulfire(m,t,d),{'Pool':'myHand'}])

def Sprint(self,draws):
  succ = False
  for i in draws:
    if self.game.addToHand(i):
      succ = True
  return succ
addSpell('Sprint',7,'Rogue',['Spell','Draw'],[lambda m,d:Sprint(m,d),{'Count':lambda m:4}])

def Starfire(self,target,draw):
  self.game.damage(target,5,True)
  self.game.addToHand(draw[0])
  return True
addSpell('Starfire',6,'Druid',['Spell','Draw','Target'],[lambda m,t,d:Starfire(m,t,d),{}])

#Draw effect but who cares starving buzzard is unplayable now
addMinion('Starving Buzzard',5,3,2,['Beast'])

addMinion('Stormpike Commando',5,4,2,['Battlecry','Target'],[lambda m,t:m.game.damage(t,2)])

def Stormwind_Aura(self):
  board = self.game.findBoard(self)
  for i in board:
    i.auraAtk += 1
    i.auraHealth += 1
  return True
addMinion('Stormwind Champion',7,6,6,['Aura'],[lambda m:Stormwind_Aura(m)])

def Succubus_Battlecry(self,draw):
  if draw[0] in self.game.myHand:
    self.game.discard(draw[0])
  return True
addMinion('Succubus',2,4,3,['Battlecry','Draw'],[lambda m,d:Succubus_Battlecry(m,d),{'Pool':'myHand'}],mClass='Warlock')

def Swipe(self,target):
  for i in self.game.oppBoard:
    if i != target:
      self.game.damage(i,1,True)
  self.game.damage(target,4,True)
addSpell('Swipe',4,'Druid',['Spell','Target'],[lambda m,t:Swipe(m,t)])

def Timberwolf_Aura(self):
  for i in self.game.findBoard(self):
    if 'Beast' in i.effects:
      i.auraAtk += 1
addMinion('Timber Wolf',1,1,1,['Aura','Beast'],[lambda m:Timberwolf_Aura(m)],mClass='Hunter')

def Totemic_Might(self):
  for i in self.game.myBoard:
    if 'Totem' in i.effects:
      self.game.buff(i,0,2)
addSpell('Totemic Might',0,'Shaman',['Spell'],[lambda m:Totemic_Might(m)])

#Weird draw spell
addSpell('Tracking',1,'Hunter',['Spell','Draw'],[lambda m,d:m.game.addToHand(d[0]),lambda m:1])

def Truesilver_Attack(self,target):
  self.game.damage(self.game.me,2)
  hc.weaponAttack(self,target)

#Aura effect ?????
addMinion('Tundra Rhino',5,2,5,['Beast','Charge'],mClass='Hunter')

def Vanish(self):
  for i in self.game.myBoard:
    self.game.addToHand(i)
    self.game.myBoard.remove(i)
  for i in self.game.oppBoard:
    self.game.addToHand(i,self.game.oppHand)
    self.game.oppBoard.remove(i)
addSpell('Vanish',6,'Rogue',['Spell'],[lambda m:Vanish(m)])

addMinion('Voodoo Doctor',1,2,1,['Battlecry','Target'],[lambda m,t:m.game.damage(t,-2)])

def RIP_Warsong_Aura(self):
  for i in self.game.findBoard(self):
    if 'Charge' in i.effects:
      i.auraAtk += 1
addMinion('Warsong Commander',3,2,3,['Aura'],[lambda m:RIP_Warsong_Aura],mClass='Warrior')

def Water_Elemental_Attack(self,target):
  self.game.damage(target,self.atk)
  self.game.damage(self,target.atk)
  self.game.addEffect(target,'Frozen')
  return True
addMinion('Water Elemental',4,3,6,['Attack','Elemental'],[lambda m,t:Water_Elemental_Attack(m,t)],mClass='Mage')

def Whirlwind(self):
  for i in self.game.summonOrder:
    self.game.damage(i,1,True)
  return True
addSpell('Whirlwind',1,'Warrior',['Spell'],[lambda m:Whirlwind(m)])

def Wild_Growth(self):
  self.game.me.maxMana += 1
  return True
addSpell('Wild Growth',3,'Druid',['Spell'],[lambda m:Wild_Growth(m)])

def Windfury(self,t):
  return self.game.addEffect(t,'Windfury')
addSpell('Windfury',2,'Shaman',['Spell','Target'],[lambda m,t:Windfury(m,t)])
addMinion('Windspeaker',4,'Shaman',['Battlecry','Target'],[lambda m,t:Windfury(m,t)])

addWeapon('Arcanite Reaper',5,5,2)
addMinion('Archmage',6,4,7,['Spell Damage'],[1])
addWeapon("Assassin's Blade",5,3,4)
addMinion('Bloodfen Raptor',2,3,2,['Beast'])
addMinion('Bluegill Warrior',2,2,1,['Charge','Murloc'])
addMinion('Booty Bay Bodyguard',5,5,4,['Taunt'])
addMinion('Boulderfist Ogre',6,6,7)
addMinion('Chillwind Yeti',4,4,5)
addMinion('Core Hound',7,9,5,['Beast'])
addMinion('Dalaran Mage',3,1,4,['Spell Damage'],[1])
addWeapon('Fiery War Axe',3,3,2)
addMinion('Frostwolf Grunt',2,2,2,['Taunt'])
addMinion('Goldshire Footman',1,1,2)
addMinion('Ironbark Protector',8,8,8,['Taunt'],mClass='Druid')
addMinion('Ironfur Grizzly',3,3,3,['Taunt','Beast'])
addMinion('Kobold Geomancer',2,2,2,['Spell Damage'],[1])
addMinion("Kor'kron Elite",4,4,3,['Charge'],mClass='Warrior')
addWeapon("Light's Justice",1,1,4)
addMinion('Lord of the Arena',6,6,5,['Taunt'])
addMinion('Magma Rager',3,5,1,['Elemental'])
addMinion('Murloc Raider',1,2,1,['Murloc'])
addMinion('Oasis Snapjaw',4,2,7,['Beast'])
addMinion('Ogre Magi',4,4,4,['Spell Damage'],[1])
addMinion('Reckless Rocketeer',6,5,2,['Charge'])
addMinion('River Crocolisk',2,2,3,['Beast'])
addMinion("Sen'jin Shieldmasta",4,3,5,['Taunt'])
addMinion('Silverback Patriarch',3,1,4,['Taunt'])
addMinion('Stonetusk Boar',1,1,1,['Beast','Charge'])
addMinion('Stormwind Knight',4,2,5,['Charge'])
addMinion('Voidwalker',1,1,3,['Taunt','Demon'],mClass='Warlock')
addMinion('War Golem',7,7,7)
addMinion('Wolfrider',3,3,1,['Charge'])

#----------------Classic uncollectibles----------------

addMinion('Mechanical Dragonling',2,2,1,['Mech'])
addMinion('Boar',1,1,1,['Beast'])
addMinion('Murloc Scout',1,1,1,['Murloc'])

#Animal companions
def Leokk_Aura(self):
  for i in self.game.myBoard:
    if i != self:
      i.auraAtk += 1
addMinion('Huffer',3,4,2,['Charge','Beast'])
addMinion('Misha',3,4,4,['Taunt','Beast'])
addMinion('Leokk',3,2,4,['Aura','Beast'],[lambda m:Leokk_Aura(m)])

#------------------Various cards from my deck------------------

def Boisterous_Battlecry(self):
  for i in self.game.myBoard:
    if i != self:
      self.game.buff(i,0,1)
  return True
addMinion('Boisterous Bard',3,3,2,['Battlecry'],[lambda m:Boisterous_Battlecry(m)])

def Dire_Frenzy(self,target):
  if 'Beast' in target.effects:
    self.game.buff(target,3,3)
addSpell('Dire Frenzy',4,'Hunter',['Spell','Target'],[lambda m,t:Dire_Frenzy(m,t)])

def Wing_Blast(self,target):
  self.game.damage(target,4)
addSpell('Wing Blast',4,'Hunter',['Spell','Target'],[lambda m,t:Wing_Blast(m,t)])

def Hydra_Attack(self,enemy):
  game = self.game
  i = game.oppBoard.index(enemy)
  try:
    game.damage(game.oppBoard[i-1],self.atk)
  except IndexError:
    pass
  try:
    game.damage(game.oppBoard[i+1],self.atk)
  except IndexError:
    pass
  game.damage(enemy,self.atk)
  game.damage(self,enemy.atk)
  return
addMinion("Cave Hydra",3,2,4,["Attack",'Beast'],[lambda me,enemy:Hydra_Attack(me,enemy)])

def Flanking_Strike(self,target):
  game = self.game
  game.damage(target,3,True)
  wolf = hc.Minion("Wolf",3,3,3)
  game.summon(wolf)
  return True
addSpell("Flanking Strike",4,'Hunter',["Spell",'Target','Damage'],[lambda me,target:Flanking_Strike(me,target)])

addMinion("Bearshark",3,4,3,["Elusive",'Beast'],mClass='Hunter')