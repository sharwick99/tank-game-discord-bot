# Tank Tactics Discord Bot

This is a discord bot that was inspired by tank turn tactics, a prototype game that was cancelled.

https://www.youtube.com/watch?v=aOYbR-Q_4Hs&t=3s&ab_channel=PeopleMakeGames
This youtube video explains the game^.

https://docs.google.com/document/d/1lxSeXA_7QfV4SBzh311vfT8645aGC0BfIenh324gU5g/edit?usp=sharing
The rules to the game^.

# How to add the bot to your discord server
1. Download main.py and save.txt
2. Create a discord bot (Optionally 2, one for testing and one for the actual bot)
3. In main.py, there is a section that looks like this
	```
	#fill these in with the respective values. if you only want to use one bot, you can just fill one in and only use that mode.
	#you can get ids by turning on developer mode in discord settings, then right clicking on the element you want in the app
	#for example, put the information for your test server in the "test_mode == True" category, and put the information for the actual bot and actual server in the "else" section

	if test_mode == False: #switches between the 2 bots, testing and normal
		channel_id = 0
		token = ""
		guild_id = 0
		admin_id = 0  #person who can start and end games
		print("test mode FALSE")
	else:
		channel_id = 0
		token = ""
		guild_id = 0
		admin_id = 0
		print("test mode TRUE")
	```
	Fill in the channel_id, token, guild_id, and admin_id. 
	
	*channel_id* - the id of the channel that you want your bot to function in
  
	*token* - the token of the bot
  
	*guild_id* - the id of your server
  
	*admin_id* - the person who you want to be able to start and end games
	
	There are two sections for the two  bots, so if you have a test bot and a normal bot, fill in each section respectivley.  When you start the bot, make sure to set "test_mode" correctly. Or, you can just have one bot and fill in just one section, it is optional to have two .
4. Run main.py
# How to start games and play
Use !commandlist and !rules for a list of all of the commands and the rules. Watching the youtube video linked above may also help.

To start a game, the admin must use the !start command. The parameters are !start <amount\> <units\> <heart_delay_multiplier\>

*amount* - amount of the units

*units* - units for the time delay

*heart_delay_multiplier* - multiplier for how long the heart takes to respawn, calculated as: heart_delay_multiplier * amount

The amount and units determine how long it takes for AP to be distributed. The heart multiplier also determines this, but it takes the amount and multiplies it by the multiplier to determine the time.

For example, the command
		```!start 1 minute 2```
will start a game with AP distributing every 1 minute, and the Heart spawning every 2 minutes, and the command 
```!start 45 seconds 4```
will start a game with AP distributing every 45 seconds, and the Heart spawning every 3 minutes

After the game is originally started, players can join. Then when everyone is in, the admin needs to use the command
```!start```
again, with no parameters to fully start the game. 
