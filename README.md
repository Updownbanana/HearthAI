# HearthAI
This project will eventually be an AI that learns how to play Hearthstone from a database of recorded plays. Unfortunately, it currently does not have an AI implemented; it just functions as an accurate simulation of Hearthstone. 

## How to use
The current Hearthstone simulator functions using keyboard commands. All names of cards are spelled and capitalized exactly as they are in-game, with spaces replaced with underscores (_). If a command takes a position as an input, it will either accept "end" to select the farthest right space, or the characters < and > followed by the name of a card to select the left or right of a minion (e.g. "<Savannah_Highmane" selects the position left of Savannah Highmane). If a command takes a target as an input, input either "enemy" or "my" followed by the name of the targeted minion (e.g. "my Gnomish_Inventor"). The same applies when asked for a target for a spell or battlecry. The commands are listed below:
- **summon [minion name] [position]**: Summons the named minion in the specified position. Does not execute Battlecries. 
- **summon [minion name] [position] [attack] [health] [cost]**: Summons a minion with the specified name and stats in the specified position. 
- **play [card name] [position]**: Plays the named card in the specified position, if the player has enough mana. Position is optional; minions will be summoned at the right end by default. If the card is not in the player's hand, it will be added and then played. 
- **draw [card name]**: Adds the named card to the player's hand. 
- **damage [target] [amount]**: Damages the named target by the amount specified. Negative amounts will heal instead. 
- **pass**: Passes the turn to the other player. User will gain control of the other player, and they will gain 1 mana crystal if they have less than 10. 
- **buff [target] [attack] [health]**: Gives the named target the specified amount of attack and health. Negative amounts will debuff instead. 
- **discard [card]**: Removes the named card from the player's hand. 
- **attack [attacker] [victim]**: Causes the named attacker on the player's side to attack the named victim on the opponent's side, if it can. Minions that can currently attack are marked by an asterisk (*). 
- **mana [amount]**: Gives the player the specified amount of mana. 
- **remove [target]**: Removes the named minion from the game. Does not execute Deathrattles. 
- **test**: (DEBUG) Runs the current system for testing all possible plays and passing data to the AI. May crash the program. 
Currently all cards from the Basic, Classic, and Rastakhan's Rumble sets are implemented in some form (except Zul'jin, since hero cards will not function properly). Not all of these are fully programmed, however, and some may be broken. 

## Todo
Features I need to add to HearthCards:
- Rush
- Choose One
- Overkill
- Silence (works, but causes problems with copying minions)
- Complex effects that can be applied to a minion permanently
- Drawing cards from effects other than battlecries/spells

Other than this, I need to finish the system for testing all plays, as well as adding an actual AI. After this, I may consider adding more features, or even implementing a neural network. 
