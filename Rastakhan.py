import HearthCards as hc
import copy
cardDefs = []

def addMinion(name,cost,atk,health,mType=[],effect=[],game=None,mClass='Neutral'):
  cardDefs.append(hc.Minion(name,cost,atk,health,mType,effect,game,mClass))
def addSpell(name,cost,sClass,sType=[],effect=[],game=None):
  cardDefs.append(hc.Spell(name,cost,sClass,sType,effect,game))
def addWeapon(name,cost,atk,health,wType=[],effects=[],hero=None,wClass='Neutral'):
  cardDefs.append(hc.Weapon(name,cost,atk,health,wType,effects,hero,wClass))

def New_Challenger(self,draws):
  self.game.addEffect(draws[0],'Taunt')
  self.game.addEffect(draws[0], 'Divine Shield')
  self.game.summon(draws[0])
addSpell('A New Challenger...',7,'Paladin',['Spell','Discover'],[lambda m,d:New_Challenger(m,d),{'Pool':'Random', 'Cost':7, 'Type':hc.Minion}])

#Pull cards from non-battlecries; code overkill
addMinion('Akali, the Rhino',8,5,5,mClass='Warrior')

#Add tribal synergies + card history to game class
addMinion('Arcanosaur',6,3,3,['Elemental'],mClass='Mage')

def Fanatic_Battlecry(self):
  for i in self.game.myHand:
    self.game.buff(i,1,1)
  return True
addMinion('Arena Fanatic',4,2,3,['Battlecry'],[lambda m:Fanatic_Battlecry(m)])

#Overkill
addMinion('Arena Patron',5,3,3,['Overkill'])

#Card draw weird
addMinion('Arena Treasure Chest',4,0,4)

#I have no idea how to code soulpriest or this card
addMinion('Auchenai Phantasm',2,3,2)

#Overkill
addSpell('Baited Arrow',5,'Hunter',['Spell','Target'],[lambda m,t:m.game.damage(t,3)])

#Not an error, but bananas are already in Classic, so don't need to add them
def Buffoon_Battlecry(self):
  for i in range(2):
    self.game.addToHand(hc.Spell('Bananas',1,'Neutral',['Spell','Target'],[lambda m,t:m.game.buff(t,1,1)]))
  return True
addMinion('Banana Buffoon',3,2,2,['Battlecry'],[lambda m:Buffoon_Battlecry(m)])

def Gnome_Battlecry(self):
  if len(self.game.oppBoard) >= 2:
    self.game.buff(self,1,0)
  return True
addMinion('Belligerent Gnome',2,1,4,['Battlecry','Taunt'],[lambda m:Gnome_Battlecry(m)])

#I'll eventually figure out how to code this one hoo boy
addSpell('Big Bad Voodoo',2,'Shaman')

#Need better draws and overkill
def Blast_Wave(self):
  for i in self.game.summonOrder:
    self.game.damage(i,2,True)
  return True
addSpell('Blast Wave',5,'Mage',['Spell','Draw'],[lambda m:Blast_Wave(m)])

def Sapper(self,origin):
  if self in self.game.myBoard:
    target = self.game.opponent
  else:
    target = self.game.me
  self.game.damage(target,2)
addMinion('Blood Troll Sapper',7,5,8,['Death'],[lambda m,o:Sapper(m,o)],mClass='Warlock')

addWeapon('Bloodclaw',1,2,2,['Battlecry'],[lambda m:m.game.damage(m.game.me,5)])

def Howler_Battlecry(self):
  for i in self.game.myBoard:
    if 'Pirate' in i.effects:
      self.game.buff(self,1,1)
  return True
addMinion('Bloodsail Howler',2,1,1,['Battlecry'],[lambda m:Howler_Battlecry(m)],mClass='Rogue')

def Strategist_Count(self):
  if self.game.checkWeapon(self.game.me):
    return 1
  else:
    return 0
addMinion('Bloodscalp Strategist',3,2,4,['Battlecry','Draw'],[lambda m,d:m.game.addToHand(d[0]),lambda m:Strategist_Count(m)],mClass='Hunter')

def Bog_Boy_Battlecry(self,target):
  if target not in self.game.myBoard: return False
  self.game.addToHand(target)
  self.game.buff(target,2,2)
  self.game.myBoard.remove(target)
  return True
addMinion('Bog Slosher',3,3,3,['Battlecry','Target','Elemental'],[lambda m,t:Bog_Boy_Battlecry(m,t)])

#Add The Coin to Classic set
addMinion('Booty Bay Bookie',2,3,3)

#Need a better drawing system
def Bwonsamdi_Battlecry(self,draws):
  for i in draws:
    self.game.addToHand(draws[i])
def Bwonsamdi_Count(self):
  return 10 - len(self.game.hand)
addMinion('Bwonsamdi, the Dead',7,7,7,['Battlecry','Draw'],[lambda m,d:Bwonsamdi_Battlecry(m,d),lambda m:Bwonsamdi_Count(m)],mClass='Priest')

#Multiple random targets
addSpell('Cannon Barrage',6,'Rogue')


addMinion('Captain Hooktusk',8,6,3,mClass='Rogue')

#Implement Lifesteal
addMinion('Cheaty Anklebiter',2,2,1,['Battlecry','Target','Lifesteal'],[lambda m,t:m.game.damage(t,1)])

#Weird conditional targeting
def Roaster_Battlecry(self,target):
  dragon = ['Dragon' in i.effects for i in self.game.myHand]
  if True not in dragon or not isinstance(target,hc.Minion):
    return True
  self.game.damage(target,7)
  return True
addMinion('Crowd Roaster',7,7,4,['Battlecry','Target','Dragon'],[lambda m,t:Roaster_Battlecry(m,t)])

#Need to implement a graveyard
addMinion('Da Undatakah',8,8,5)

#Haven't even implemented hero powers, so fire-eater can't work
addMinion('Daring Fire-Eater',1,1,1,mClass='Mage')

def Demonbolt_Aura(self):
  for i in self.game.myBoard:
    self.auraCost -= 1
def Demonbolt(self,target):
  if isinstance(target,hc.Minion):
    self.game.kill(target)
    return True
  return False
addSpell('Demonbolt',8,'Warlock',['Spell','Hand Aura','Target'],[lambda m,t:Demonbolt(m,t),lambda m:Demonbolt_Aura(m)])

def Devastate(self,target):
  if target.damage < 0 and isinstance(target,hc.Minion):
    self.game.damage(target,4)
addSpell('Devastate',1,'Warrior',['Spell','Target'],[lambda m,t:Devastate(m,t)])

def Marksman_Aura(self):
  if self.damage < 0:
    self.auraAtk += 4
addMinion('Dozing Marksman',2,0,4,['Aura'],[lambda m:Marksman_Aura(m)])

def Dragon_Roar(self,draws):
  for i in draws:
    self.game.addToHand(draws[i])
addSpell('Dragon Roar',2,'Warrior',['Spell','Draw'],[lambda m,d:Dragon_Roar(m,d),lambda m:2])

def Scorcher_Battlecry(self):
  for i in self.game.summonOrder:
    if i != self:
      self.game.damage(i,1)
  return True
addMinion('Dragonmaw Scorcher',5,3,6,['Battlecry','Dragon'],[lambda m:Scorcher_Battlecry(m)])

#Better draw system
addMinion('Drakkari Trickster',3,3,4)

#Need a way to code more complex / temporary auras
addSpell('Elemental Evocation',0,'Mage')

#Armor is not fully implemented yet
def Emberscale_Battlecry(self):
  dragon = ['Dragon' in i.effects for i in self.game.myHand]
  if True not in dragon:
    return True
  self.game.me.armor += 5
  return True
addMinion('Emberscale Drake',5,5,5,['Battlecry','Dragon'],[lambda m:Emberscale_Battlecry(m)],mClass='Warrior')

#Overkill not implemented
addWeapon('Farraki Battleaxe',5,3,3,wClass='Paladin')

addMinion('Firetree Witchdoctor',2,2,2,['Spell','Discover'],[lambda m,d:m.game.addToHand(d[0]),{'Pool':'Random', 'Type':hc.Spell}])

def Flash_of_Light(self,target,draw):
  self.game.damage(target,-4)
  self.game.addToHand(draw[0])
addSpell('Flash of Light',2,'Paladin',['Spell','Draw','Target'],[lambda m,t,d:Flash_of_Light(m,t,d),lambda m:1])

def Champ_Battlecry(self):
  hotshot = hc.Minion('Hotshot',5,5,5)
  self.game.summon(hotshot,self.game.getMinion(self))
addMinion('Former Champ',5,1,1,['Battlecry'],[lambda m:Champ_Battlecry(m)])

#how?????
addMinion('Gonk, the Raptor',7,4,9,['Beast'])

def Gral_Battlecry(self,draw):
  target = draw[0]
  self.game.buff(self,target.atk,target.health)
  self.target = target
def Gral_Deathrattle(self):
  self.game.addToHand(self.target)
addMinion('Gral, the Shark',5,2,2,['Battlecry','Deathrattle','Draw','Beast'],[lambda m,t:Gral_Battlecry(m,t),lambda m:Gral_Deathrattle(m),lambda m:1])

#Need a card history
addMinion('Grave Horror',12,7,8,['Taunt'])

#Griftah?
addMinion('Griftah',4,4,5)

def Grim_Rally(self,target):
  if target in self.game.myBoard:
    self.game.kill(target)
    for i in self.game.myBoard:
      self.game.buff(i,1,1)
addSpell('Grim Rally',1,'Warlock',['Spell','Target'],[lambda m,t:Grim_Rally(m,t)])

#Overkill
addMinion('Gurubashi Chicken',1,1,1,['Beast'])

def Hypemon_Battlecry(self,draws):
  draw = copy.deepcopy(draws[0])
  draw.buffAtk = -draw.baseAtk + 1
  draw.buffHealth = -draw.baseHealth + 1
  draw.buffCost = -draw.baseCost + 1
  self.game.addToHand(draw)
addMinion('Gurubashi Hypemon',7,5,7,['Battlecry','Discover'],[lambda m,d:Hypemon_Battlecry(m,d),{'Pool':'Random', 'Effects':['Battlecry']}],mClass='Rogue')

#Armor
def Offering(self):
  self.game.me.armor += 8
  self.game.kill(self)
addMinion('Gurubashi Offering',1,0,2,['Start of Turn'],[lambda m:Offering(m)])

#Track deck
addMinion('Hakkar, the Soulflayer',10,9,6)

def Halazzi_Battlecry(self):
  game = self.game
  lynx = hc.Minion('Lynx',1,1,1,['Rush','Beast'])
  while len(game.myHand) < 10:
    game.addToHand(lynx)
addMinion('Halazzi, the Lynx',5,3,2,['Battlecry','Beast'],[lambda m:Halazzi_Battlecry(m)],mClass='Hunter')

#Overkill
addMinion('Half-Time Scavenger',4,3,5,['Stealth'])

#Temp aura
addSpell('Haunting Visions',3,'Shaman',['Spell','Discover'],[lambda m,d:m.game.addToHand(d[0]),{'Pool':'Random', 'Type':hc.Spell}])

def Headhunter_Battlecry(self):
  beast = False
  for i in self.game.myBoard:
    if 'Beast' in i.effects:
      beast = True
  if beast:
    self.buffHealth += 1
  return True
addWeapon("Headhunter's Hatchet",2,2,2,['Battlecry'],[lambda m:Headhunter_Battlecry(m)],wClass='Hunter')

#Random minion
addSpell('Heavy Metal!',6,'Warrior')

#Weird random targeting effect
addMinion('Helpless Hatchling',1,1,1,['Beast'])

#Don't currently track opening hand
addMinion('Hex Lord Malacrass',8,5,5,mClass='Mage')

def Thekal_Battlecry(self):
  game = self.game
  start = game.me.health
  game.me.damage -= start - 1
  game.me.armor += start - 1
addMinion('High Priest Thekal',3,3,4,['Battlecry'],[lambda m:Thekal_Battlecry(m)],mClass='Paladin')

def Jeklik_Discard(self):
  second = copy.deepcopy(self)
  self.game.addToHand(self)
  self.game.addToHand(second)
addMinion('High Priestess Jeklik',4,3,4,['Discard','Taunt','Lifesteal'],[lambda m:Jeklik_Discard(m)],mClass='Warlock')

def Hireek_Battlecry(self):
  while len(self.game.myBoard) < 7:
    self.game.summon(copy.deepcopy(self))
  return True
addMinion("Hir'eek, the Bat",8,1,1,['Battlecry','Beast'],[lambda m:Hireek_Battlecry(m)],mClass='Warlock')

def Peddler_Battlecry(self):
  frozen = ['Frozen' in i.effects for i in self.game.myBoard]
  if True in frozen:
    self.game.me.armor += 8
  return True
addMinion('Ice Cream Peddler',4,3,5,['Battlecry'],[lambda m:Peddler_Battlecry(m)])

#Track deck
addMinion('Immortal Prelate',2,1,3,mClass='Paladin')

#Overkill
addMinion('Ironhide Direhorn',7,7,7,['Beast'])

#Hero Powers and Ragnaros aren't implemented
addMinion("Jan'alai, the Dragonhawk",7,4,4,['Beast'],mClass='Mage')

#Need card history / graveyard
addMinion("Krag'wa, the Frog",6,4,6,['Beast'],mClass='Shaman')

#Overload not implemented
addWeapon('Likkim',2,1,3,wClass='Shaman')

#Overkill
addMinion('Linecracker',7,5,10)

#Choose One
addSpell('Mark of the Loa',4,'Druid')

#Secret
addMinion('Masked Contender',3,2,4)

#Random targets
addSpell('Mass Hysteria',5,'Priest',['Random'])

def Masters_Call(self,draws):
  beasts = ['Beast' in i.effects for i in draws]
  if False not in beasts:
    for i in draws:
      self.game.addToHand(i)
    return True
  return self.game.addToHand(draws[0])
addSpell("Master's Call",3,'Hunter')

def Mojomaster_Battlecry(self):
  game = self.game
  for i in [game.me,game.opponent]:
    i.maxMana = 5
    i.mana = min(5,i.mana)
addMinion('Mojomaster Zihi',6,5,5,['Battlecry'],[lambda m:Mojomaster_Battlecry(m)])

#ogres.....
addMinion("Mosh'Ogg Announcer",5,6,5)

#Draw in non-battlecry
addMinion('Murloc Tastyfin',4,3,2,['Murloc'])

#Overkill
addMinion('Oondasta',9,7,7,['Rush','Beast'])

addMinion('Ornery Tortoise',3,3,5,['Battlecry','Beast'],[lambda m:m.game.damage(m.game.me,5)])

def Overlords_Whip(self,origin):
  if isinstance(origin,hc.Minion):
    self.game.damage(origin,1)
addWeapon("Overlord's Whip",3,2,4,['Play Card'],[lambda m,o:Overlords_Whip(m,o)],wClass='Warrior')

addSpell('Pounce',0,'Druid',['Spell'],[lambda m:m.game.buff(m.game.me,2,0)])

def Predatory_Instincts(self,draw):
  draw[0].buffHealth = draw[0].health
  self.game.addToHand(draw[0])
addSpell('Predatory Instincts',4,'Druid',['Spell','Draw'],[lambda m,d:Predatory_Instincts(m,d)])

#Track deck
addMinion('Princess Talanji',8,7,5,mClass='Priest')

#Hero power
addMinion('Pyromaniac',3,3,4,mClass='Mage')

def Rabble_Aura(self):
  for i in self.game.oppBoard:
    self.game.auraCost -= 1
addMinion('Rabble Bouncer',7,2,7,['Hand Aura','Taunt'],[lambda m:Rabble_Aura(m)])

#Draw / combo
addSpell('Raiding Party',3,'Rogue')

def Kragwall(self):
  for i in range(3):
    self.game.summon(hc.Minion('Toad',2,2,4,['Taunt','Beast']))
addSpell('Rain of Toads',6,'Shaman',['Spell','Overload'],[lambda m:Kragwall(m),3])

#Possibly random discard
addMinion('Reckless Diretroll',3,2,6,['Taunt'])

addSpell('Regenerate',0,'Priest',['Spell','Target'],[lambda m,t:m.game.damage(t,-3)])

addMinion("Regeneratin' Thug",4,3,5,['Start of Turn'],[lambda m:m.game.damage(m,-2)])

#Graveyard
addSpell('Revenge of the Wild',2,'Hunter')

def Shaker_Deathrattle(self):
  breaker = hc.Minion('Rumbletusk Breaker',2,3,2)
  pos = self.game.getMinion(self)
  self.game.summon(breaker,position=pos)
addMinion('Rumbletusk Shaker',4,3,2,['Deathrattle'],[lambda m:Shaker_Deathrattle(m)])

def Sand_Drudge(self,origin):
  if isinstance(origin,hc.Spell):
    zombie = hc.Minion('Zombie',1,1,1,['Taunt'])
    pos = self.game.getMinion(self)
    self.game.summon(zombie,position=pos)
addMinion('Sand Drudge',3,3,3,['Play Card'],[lambda m,o:Sand_Drudge(m,o)],mClass='Priest')

def Taskmaster_Deathrattle(self):
  agent = hc.Minion('Free Agent',0,0,3,['Taunt'])
  self.game.summon(agent,board=self.game.oppBoard)
addMinion('Saronite Taskmaster',1,2,3,['Deathrattle'],[lambda m:Taskmaster_Deathrattle(m)])

def Striker_Battlecry(self,target):
  if target not in self.game.oppBoard:
    return False
  self.game.damage(target,self.game.me.atk)
  return True
addMinion('Savage Striker',2,2,3,['Battlecry','Target'],[lambda m,t:Striker_Battlecry(m,t)])

def Scarabs_Deathrattle(self):
  scarab = hc.Minion('Scarab',1,1,1)
  pos = self.game.getMinion(self)
  board = self.game.getBoard(self)
  for i in range(3):
    self.game.summon(scarab,position=pos,board=board)
addMinion('Scarab Egg',2,0,2,['Deathrattle'],[lambda m:Scarabs_Deathrattle(m)])

#Elemental synergy; need card history
addSpell('Scorch',4,'Mage',['Spell','Target'],[lambda m,t:m.game.damage(t,4,True)])

#Need a copy minion function
def Seance(self,target):
  if not isinstance(target,hc.Minion):
    return False
  minion = copy.deepcopy(target)
  minion.buffHealth = 0
  minion.buffAtk = 0
  minion.buffCost = 0
  self.game.addToHand(minion)
addSpell('Seance',2,'Priest',['Spell','Target'],[lambda m,t:Seance(m,t)])

addMinion('Serpent Ward',2,0,2,['End of Turn','Totem'],[lambda m:m.game.damage(m.game.opponent,2)])

def Serrated_Deathrattle(self):
  for i in self.game.myBoard:
    self.game.addEffect(i,'Rush')
addWeapon('Serrated Tooth',1,1,3,['Deathrattle'],[lambda m:Serrated_Deathrattle(m)])

#Can't currently detect attacks from other characters
addMinion('Sharkfin Fan',2,2,2,['Pirate'])

def Shieldbreaker_Battlecry(self,target):
  if not isinstance(target,hc.Minion) or 'Taunt' not in target.effects:
    return False
  self.game.silence(target)
addMinion('Shieldbreaker',2,2,1,['Battlecry','Target'],[lambda m,t:Shieldbreaker_Battlecry(m,t)])

#Need a card history for Shirvallah to work
addMinion('Shirvallah, the Tiger',25,7,5,['Divine Shield','Rush','Lifesteal','Beast'],mClass='Paladin')

#Potentially random discard
def Shriek(self):
  for i in self.game.summonOrder:
    self.game.damage(i,2)
addSpell('Shriek',1,'Warlock',['Spell'],[lambda m:Shriek(m)])

#Overkill
addMinion('Sightless Ranger',5,3,4,['Rush'])

def Smolderthorn_Battlecry(self,target):
  dragon = ['Dragon' in i.effects for i in self.game.myHand]
  if True not in dragon:
    return True
  elif target.damage >= 0:
    return False
  self.game.kill(target)
  return True

#How do i code shellfighter
addMinion('Snapjaw Shellfighter',5,3,8)

#Need to track discarded cards
addMinion('Soulwarden',6,6,6,mClass='Warlock')

#huh
addMinion('Soup Vendor',2,1,4)

#Aura effects
addMinion('Spellzerker',2,2,3)

#Need temporary effects for the spirit stealth

#Random targets
addMinion('Spirit of the Bat',2,0,3,mClass='Warlock')

#Need to track deck
addMinion('Spirit of the Dead',1,0,3,mClass='Priest')

#Hero powers aren't implemented
addMinion('Spirit of the Dragonhawk',2,0,3,mClass='Mage')

def Frog_Spirit(self,draws):
  self.game.addToHand(draws[0])
addMinion('Spirit of the Frog',3,0,3,['Spell','Draw'],[lambda m,d:Frog_Spirit(m,d),lambda m:1],mClass='Shaman')

def Lynx_Spirit(self,origin):
  if 'Beast' in origin.effects:
    self.game.buff(origin,1,1)
addMinion('Spirit of the Lynx',3,0,3,['Summon'],[lambda m,o:Lynx_Spirit(m,o)],mClass='Hunter')

#Better draw / tracking hero attacks better
addMinion('Spirit of the Raptor',1,0,3,mClass='Druid')

#Temporary effects
addMinion('Spirit of the Rhino',1,0,3,mClass='Warrior')

#weird one to code
addMinion('Spirit of the Shark',4,0,3,mClass='Rogue')

def Tiger_Spirit(self,origin):
  if isinstance(origin,hc.Spell):
    cost = origin.cost
    pos = self.game.getMinion(self)
    self.game.summon(hc.Minion('Tiger',cost,cost,cost,['Beast']),pos)
addMinion('Spirit of the Tiger',4,0,3,['Play Card'],[lambda m,o:Tiger_Spirit(m,o)])

#Secret
addSpell('Splitting Image',3,'Mage',['Secret'])

def Springpaw_Battlecry(self):
  lynx = hc.Minion('Lynx',1,1,1,['Rush','Beast'])
  self.game.addToHand(lynx)
  return True
addMinion('Springpaw',1,1,1,['Battlecry','Rush','Beast'],[lambda m:Springpaw_Battlecry(m)])

#Random targeting
addSpell('Stampeding Roar',6,'Druid',['Random'])

#Can't be a rogue weapon
addSpell('Stolen Steel',2,'Rogue',['Spell','Discover'],[lambda m,d:m.game.addToHand(d),{'Pool':'Random', 'Type':hc.Weapon}])

#Overkill
addWeapon("Sul'thraze",6,4,4)

#Need to track deck
def Surrender_to_Madness(self):
  game = self.game
  game.me.maxMana -= 2
  game.me.mana = min(game.me.mana-2,game.me.maxMana)
addSpell('Surrender to Madness',3,'Priest',['Spell'],[lambda m:Surrender_to_Madness(m)])

#Random targets
def Beast_Within(self,target):
  if 'Beast' in target.effects:
    self.game.buff(target,1,1)
    return True
  return False
addSpell('The Beast Within',1,'Hunter',['Spell','Target'],[lambda m,t:Beast_Within(m,t)])

#Overkill
addMinion('Ticket Scalper',4,5,3,['Pirate'])

#Temporary effects
addSpell('Time Out!',3,'Paladin')

#Random summon + overkill
def Totemic_Smash(self,target):
  self.game.damage(target,2)
addSpell('Totemic Smash',1,'Shaman',['Spell','Target'],[lambda m,t:Totemic_Smash(m,t)])

#Treespeaker????
addMinion('Treespeaker',5,4,4,mClass='Druid')

#Draw effect???????????
addMinion('Untamed Beastmaster',3,3,4)

#Deck tracking
addSpell('Void Contract',8,'Warlock')

def Walk_the_Plank(self,target):
  if target.damage >= 0:
    self.game.kill(target)
    return True
  return False
addSpell('Walk the Plank',4,'Rogue',['Spell','Target'],[lambda m,t:Walk_the_Plank(m,t)])

def Voone_Battlecry(self):
  for i in self.game.myHand:
    if 'Dragon' in i.effects:
      self.game.addToHand(copy.deepcopy(i))
addMinion('War Master Voone',4,4,3,['Battlecry'],[lambda m:Voone_Battlecry(m)])

#Choose one
addMinion('Wardruid Loti',3,1,2,mClass='Druid')

#Card history
addMinion('Wartbringer',1,2,1,mClass='Shaman')

#Hero powers
addMinion('Waterboy',2,2,1)

#Can't track amount of healing throughout game
addMinion('Zandalari Templar',4,4,4,mClass='Paladin')

#??
addMinion('Zentimo',3,1,3,mClass='Shaman')

#Zul'jin is a hero card and requires a card history

addMinion('Amani War Bear',7,5,7,['Rush','Taunt','Beast'])
addMinion("Mosh'Ogg Enforcer",8,2,14,['Taunt','Divine Shield'])

#-----------------------Uncollectibles-----------------------

#Add temp auras to shuffle after drawing; track deck; better targeting for casts when drawn cards
def Corrupted_Blood(self):
  self.game.damage(self.game.me,5)
addSpell('Corrupted Blood',0,'Neutral',['Casts When Drawn'],[lambda m:Corrupted_Blood(m)])

addMinion('Hotshot',5,5,5)
addMinion('Rumbletusk Breaker',2,3,2)
addMinion('Zombie',1,1,1,['Taunt'])
addMinion('Free Agent',0,0,3,['Taunt'])