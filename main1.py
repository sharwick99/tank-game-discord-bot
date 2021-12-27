#written by sharwick99 on github
#inspired by https://www.youtube.com/watch?v=aOYbR-Q_4Hs&t=3s&ab_channel=PeopleMakeGames

import discord
from discord.ext import commands, tasks
from discord.ui import Button
from discord.utils import get
import random as rand
import asyncio
import math
import json
import emojis
import copy


test_mode = True    #switches between bots, used for testing


#discord bot, sets up bot
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "!", intents = intents)

#main matrix to represent the board of the game
board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

#used to determine starting positions of players, gets shuffled then popped
board_coords = [
    (0,0),(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),(0,11),(0,12),
    (1,0),(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(1,11),(1,12),
    (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(2,1),(2,11),(2,12),
    (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),(3,6),(3,7),(3,8),(3,9),(3,1),(3,11),(3,12),
    (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),(4,6),(4,7),(4,8),(4,9),(4,1),(4,11),(4,12),
    (5,0),(5,1),(5,2),(5,3),(5,4),(5,5),(5,6),(5,7),(5,8),(5,9),(5,1),(5,11),(5,12),
    (6,0),(6,1),(6,2),(6,3),(6,4),(6,5),(6,6),(6,7),(6,8),(6,9),(6,1),(6,11),(6,12),
    (7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7),(7,8),(7,9),(7,1),(7,11),(7,12),
    (8,0),(8,1),(8,2),(8,3),(8,4),(8,5),(8,6),(8,7),(8,8),(8,9),(8,1),(8,11),(8,12),
    (9,0),(9,1),(9,2),(9,3),(9,4),(9,5),(9,6),(9,7),(9,8),(9,9),(9,1),(9,11),(9,12),
    (10,0),(10,1),(10,2),(10,3),(10,4),(10,5),(10,6),(10,7),(10,8),(10,9),(10,10),(10,11),(10,12),
    (11,0),(11,1),(11,2),(11,3),(11,4),(11,5),(11,6),(11,7),(11,8),(11,9),(11,10),(11,11),(11,12),
    (12,0),(12,1),(12,2),(12,3),(12,4),(12,5),(12,6),(12,7),(12,8),(12,9),(12,10),(12,11),(12, 12)
]

rand.shuffle(board_coords)

channel = None #setting global variables to avoid error
board_string = ""
board_message = None
game_state = "null"
event_already_occurred = False

time_delay = 10
heart_delay = 10


#user banks
users = {}

default_user_stats = {  #default template for user stats
    "emoji": "",
    "hp": 3,
    "ap": 0,
    "range": 2,
    "speed": 1,
    "coords": {"y": 0, "x": 0},
    "turn": False
}

save_dict = { #template for the dictionary used in the save file
    "board": None,
    "users": None,
    "game_state": None,
    "time_delay": None
}




#fill these in with the respective values. if you only want to use one bot, you can just fill one in and only use that mode.
#you can get ids by turning on developer mode in discord settings, then right clicking on the element you want in the app
#for example, put the information for your test server in the "test_mode == True" category, and put the information for the actual bot and actual server in the "else" sectiom
if test_mode == False:      #switches between the 2 bots, testing and normal
    channel_id = 0
    token = ""
    guild_id = 0
    admin_id = 0   #person who can start and end games
    print("test mode FALSE")
else:
    channel_id = 0
    token = ""
    guild_id = 0
    admin_id = 0
    print("test mode TRUE")

async def button_up(interaction): #moves the player up 1
    if interaction.user.id not in users:  #only allows users in the game to use the button
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started":  #only allows use if game is started
        await channel.send("The game has not started yet")
        return
    if users[interaction.user.id]["ap"] < 1:  #movement cost is 1 ap
        await channel.send("You do not have enough AP to do that")
        return
    if users[interaction.user.id]["coords"]["y"] - users[interaction.user.id]["speed"] < 0: #prevents moving out of bounds
        await channel.send("You cannot move out of bounds")
        return
    for user in users: #prevents movement into other players squares
        if (users[interaction.user.id]["coords"]["y"] - users[interaction.user.id]["speed"], users[interaction.user.id]["coords"]["x"]) == (users[user]["coords"]["y"], users[user]["coords"]["x"]):
            await channel.send("You cannot move into another player's square")
            return

    #checks if player is collecting a heart
    if board[users[interaction.user.id]["coords"]["y"] - users[interaction.user.id]["speed"]][users[interaction.user.id]["coords"]["x"]] == 1:
        await channel.send(f"**{interaction.user.name}** has collected a heart!")
        users[interaction.user.id]["hp"] += 1
    


    board[users[interaction.user.id]["coords"]["y"]][users[interaction.user.id]["coords"]["x"]] = 0 #sets board coordinate to 0 (0 represents fog)
    users[interaction.user.id]["coords"]["y"] -= users[interaction.user.id]["speed"] #moves player according to their speed
    board[users[interaction.user.id]["coords"]["y"]][users[interaction.user.id]["coords"]["x"]] = interaction.user.id #sets new coords as their id (represents their emoji)
    users[interaction.user.id]["ap"] -= 1 #cost is 1 ap

    save() #saves to the save file and updates the board
    await update_board_string()

async def button_down(interaction): #see button_up for comments on the functionality
    if interaction.user.id not in users:
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started":
        await channel.send("The game has not started yet")
        return
    if users[interaction.user.id]["ap"] < 1:
        await channel.send("You do not have enough AP to do that")
        return
    if users[interaction.user.id]["coords"]["y"] + users[interaction.user.id]["speed"] > 12:
        await channel.send("You cannot move out of bounds")
        return
    for user in users:
        if (users[interaction.user.id]["coords"]["y"] + users[interaction.user.id]["speed"], users[interaction.user.id]["coords"]["x"]) == (users[user]["coords"]["y"], users[user]["coords"]["x"]):
            await channel.send("You cannot move into another player's square")
            return

    if board[users[interaction.user.id]["coords"]["y"] + users[interaction.user.id]["speed"]][users[interaction.user.id]["coords"]["x"]] == 1:
        await channel.send(f"**{interaction.user.name}** has collected a heart!")
        users[interaction.user.id]["hp"] += 1

    board[users[interaction.user.id]["coords"]["y"]][users[interaction.user.id]["coords"]["x"]] = 0
    users[interaction.user.id]["coords"]["y"] += users[interaction.user.id]["speed"]
    board[users[interaction.user.id]["coords"]["y"]][users[interaction.user.id]["coords"]["x"]] = interaction.user.id
    users[interaction.user.id]["ap"] -= 1

    save()
    await update_board_string()

async def button_left(interaction): #see button_up for comments on the functionality
    if interaction.user.id not in users:
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started":
        await channel.send("The game has not started yet")
        return
    if users[interaction.user.id]["ap"] < 1:
        await channel.send("You do not have enough AP to do that")
        return
    if users[interaction.user.id]["coords"]["x"] - users[interaction.user.id]["speed"] < 0:
        await channel.send("You cannot move out of bounds")
        return
    for user in users:
        if (users[interaction.user.id]["coords"]["y"], users[interaction.user.id]["coords"]["x"] - users[interaction.user.id]["speed"]) == (users[user]["coords"]["y"], users[user]["coords"]["x"]):
            await channel.send("You cannot move into another player's square")
            return

    if board[users[interaction.user.id]["coords"]["y"]][users[interaction.user.id]["coords"]["x"] - users[interaction.user.id]["speed"]] == 1:
        await channel.send(f"**{interaction.user.name}** has collected a heart!")
        users[interaction.user.id]["hp"] += 1

    board[users[interaction.user.id]["coords"]["y"]][users[interaction.user.id]["coords"]["x"]] = 0
    users[interaction.user.id]["coords"]["x"] -= users[interaction.user.id]["speed"]
    board[users[interaction.user.id]["coords"]["y"]][users[interaction.user.id]["coords"]["x"]] = interaction.user.id
    users[interaction.user.id]["ap"] -= 1

    save()
    await update_board_string()

async def button_right(interaction): #see button_up for comments on the functionality
    if interaction.user.id not in users:
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started":
        await channel.send("The game has not started yet")
        return
    if users[interaction.user.id]["ap"] < 1:
        await channel.send("You do not have enough AP to do that")
        return
    if users[interaction.user.id]["coords"]["x"] + users[interaction.user.id]["speed"] > 12:
        await channel.send("You cannot move out of bounds")
        return
    for user in users:
        if (users[interaction.user.id]["coords"]["y"], users[interaction.user.id]["coords"]["x"] + users[interaction.user.id]["speed"]) == (users[user]["coords"]["y"], users[user]["coords"]["x"]):
            await channel.send("You cannot move into another player's square")
            return

    if board[users[interaction.user.id]["coords"]["y"]][users[interaction.user.id]["coords"]["x"] + users[interaction.user.id]["speed"]] == 1:
        await channel.send(f"**{interaction.user.name}** has collected a heart!")
        users[interaction.user.id]["hp"] += 1

    board[users[interaction.user.id]["coords"]["y"]][users[interaction.user.id]["coords"]["x"]] = 0
    users[interaction.user.id]["coords"]["x"] += users[interaction.user.id]["speed"]
    board[users[interaction.user.id]["coords"]["y"]][users[interaction.user.id]["coords"]["x"]] = interaction.user.id
    users[interaction.user.id]["ap"] -= 1

    save()
    await update_board_string()

async def upgrade_range(interaction): #upgrades the players range by 1
    if interaction.user.id not in users: #only allows players in the game to use
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started": #only allows pressing if game is started
        await channel.send("The game has not started yet")
        return
    if users[interaction.user.id]["ap"] < 3: #cost is 3 ap
        await channel.send("You do not have enough AP to do that")
        return

    users[interaction.user.id]["range"] += 1 #adds 1 to range
    users[interaction.user.id]["ap"] -= 3 #cost is 3 ap

    await channel.send(f"**{interaction.user.name}** upgraded their range to {users[interaction.user.id]['range']}") #sends confirmation message

    save() #saves to the save file and updates the board
    await update_board_string()

async def upgrade_speed(interaction): #see upgrade_range for comments on the functionality
    if interaction.user.id not in users:
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started":
        await channel.send("The game has not started yet")
        return
    if users[interaction.user.id]["ap"] < 3:
        await channel.send("You do not have enough AP to do that")
        return

    users[interaction.user.id]["speed"] += 1
    users[interaction.user.id]["ap"] -= 3

    await channel.send(f"**{interaction.user.name}** upgraded their speed to {users[interaction.user.id]['speed']}")

    save() #saves to the save file and updates the board
    await update_board_string()

async def upgrade_hp(interaction): #see upgrade_range for comments on the functionality
    if interaction.user.id not in users:
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started":
        await channel.send("The game has not started yet")
        return
    if users[interaction.user.id]["ap"] < 3:
        await channel.send("You do not have enough AP to do that")
        return

    users[interaction.user.id]["hp"] += 1
    users[interaction.user.id]["ap"] -= 3

    await channel.send(f"**{interaction.user.name}** bought a heart, increasing their HP to {users[interaction.user.id]['hp']}")

    save() #saves to the save file and updates the board
    await update_board_string()

async def button_shoot(interaction): #shoots closest player
    if interaction.user.id not in users: #only allows shooting for players in the game
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started": #only allows pressing for started games
        await channel.send("The game has not started yet")
        return
    if users[interaction.user.id]["ap"] < 1: #cost is 1 ap
        await channel.send("You do not have enough AP to do that")
        return

    users_in_range = {} #creates users in range dict, keys are id, values are distance
    for user in users:
        if user == interaction.user.id: #disregards the player who pressed the button
            continue

        # if the user is within the players range, add the distance to the users in range dictionary. keys are id, values are distance
        if abs(users[interaction.user.id]["coords"]["x"] - users[user]["coords"]["x"]) <= users[interaction.user.id]["range"] and abs(users[interaction.user.id]["coords"]["y"] - users[user]["coords"]["y"]) <= users[interaction.user.id]["range"]:
            users_in_range[user] = math.sqrt(abs(((users[interaction.user.id]["coords"]["x"] - users[user]["coords"]["x"]) ^ 2) + ((users[interaction.user.id]["coords"]["y"] - users[user]["coords"]["y"]) ^ 2)))

    if len(users_in_range) == 0: #if there is nobody in the range
        await channel.send("Nobody is in your range")
        return

    #sorts through the users in range dict and finds the closest player
    closest_user = list(users_in_range.keys())[0] #first player in range
    for user in users_in_range: #loops through all players in range, finds the one with the least distance
        if users_in_range[user] < users_in_range[closest_user]:
            closest_user = user

    users[interaction.user.id]["ap"] -= 1 #cost is 1 ap
    users[closest_user]["hp"] -= 1 #takes away targets health

    user_object = client.get_user(closest_user)

    if users[closest_user]["hp"] == 0: #checks for death
        await channel.send(f":skull: **{interaction.user.name}** shot and killed **{user_object.name}**")

        board[users[closest_user]["coords"]["y"]][users[closest_user]["coords"]["x"]] = 0 #sets dead player to fog

        users[interaction.user.id]["ap"] += users[closest_user]["ap"] #gives all ap to killer

        del users[closest_user] #deletes dead player from the main user dictionary

        if len(users) == 1: #checks if that was the last player alive
            await channel.send(f":trophy::trophy::trophy:  **{interaction.user.name} won!!!**  :trophy::trophy::trophy:")
            
        await update_board_string() #saves and updates
        save()
    else:
        await channel.send(f":broken_heart: **{interaction.user.name}** shot **{user_object.name}**") #send confirmation message
 
        await update_board_string() #saves and updates
        save()

async def button_give(interaction): #see button_shoot  for comments on the functionality
    if interaction.user.id not in users:
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started":
        await channel.send("The game has not started yet")
        return

    users_in_range = {}
    for user in users:
        if user == interaction.user.id:
            continue
    
        if abs(users[interaction.user.id]["coords"]["x"] - users[user]["coords"]["x"]) <= users[interaction.user.id]["range"] and abs(users[interaction.user.id]["coords"]["y"] - users[user]["coords"]["y"]) <= users[interaction.user.id]["range"]:
            users_in_range[user] = math.sqrt(abs(((users[interaction.user.id]["coords"]["x"] - users[user]["coords"]["x"]) ^ 2) + ((users[interaction.user.id]["coords"]["y"] - users[user]["coords"]["y"]) ^ 2)))

    if len(users_in_range) == 0:
        await channel.send("Nobody is in your range")
        return

    closest_user = list(users_in_range.keys())[0]
    for user in users_in_range:
        if users_in_range[user] < users_in_range[closest_user]:
            closest_user = user

    users[interaction.user.id]["ap"] -= 1
    users[closest_user]["ap"] += 1

    user_object = client.get_user(closest_user)

    await channel.send(f":dizzy: **{interaction.user.name}** gave 1 AP to **{user_object.name}**")

async def button_leaderboard(interaction):

    if interaction.user.id not in users:
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started":
        await channel.send("The game has not started yet")
        return

    if game_state != "null":
        leaderboard_string = "Leaderboard (Not Sorted)"
        for user in users:
            user_object = client.get_user(user)
            leaderboard_string += f"\n**{user_object.name}**:  Emoji: {users[user]['emoji']}  HP: {users[user]['hp']}  AP: {users[user]['ap']}  Range: {users[user]['range']}  Speed: {users[user]['speed']}"
        print(leaderboard_string)
        await channel.send(leaderboard_string)


def view_init(): #view is a message component that holds the buttons, this function initializes and returns the buttons for the message

    left_button = discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⬅️")
    left_button.callback = button_left

    up_button = discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⬆️")
    up_button.callback = button_up

    down_button = discord.ui.Button(style=discord.ButtonStyle.primary, emoji="⬇️")
    down_button.callback = button_down

    right_button = discord.ui.Button(style=discord.ButtonStyle.primary, emoji="➡️")
    right_button.callback = button_right

    range_button = discord.ui.Button(label="Upgrade Range (3 AP)", style=discord.ButtonStyle.green, emoji="⏫")
    range_button.callback = upgrade_range

    speed_button = discord.ui.Button(label="Upgrade Speed (3 AP)", style=discord.ButtonStyle.green, emoji="⏫")
    speed_button.callback = upgrade_speed

    heart_button = discord.ui.Button(label="Buy Heart (3 AP)", style=discord.ButtonStyle.green, emoji="❤️")
    heart_button.callback = upgrade_hp

    give_button = discord.ui.Button(label="Give 1 AP to Closest", style=discord.ButtonStyle.green, emoji="💫")
    give_button.callback = button_give

    shoot_button = discord.ui.Button(label="Shoot Closest", style=discord.ButtonStyle.danger, emoji="🗡️")
    shoot_button.callback = button_shoot

    leaderboard_button = discord.ui.Button(label="Leaderboard", style=discord.ButtonStyle.secondary, emoji="📜")
    leaderboard_button.callback = button_leaderboard

    view = discord.ui.View()
    view.add_item(left_button)
    view.add_item(up_button)
    view.add_item(down_button)
    view.add_item(right_button)
    view.add_item(leaderboard_button)
    view.add_item(heart_button)
    view.add_item(range_button)
    view.add_item(speed_button)
    view.add_item(give_button)
    view.add_item(shoot_button)
    

    return view

def save(): #saves to save.txt
    global save_dict
    global board
    global users
    global game_state
    global time_delay
    global heart_delay

    with open("save.txt","w", encoding='utf-8') as save:

        save_dict["board"] = board #writes everything to the save dict
        save_dict["users"] = users
        save_dict["game_state"] = game_state
        save_dict["time_delay"] = time_delay
        save_dict["heart_delay"] = heart_delay

        save.write(str(save_dict) + "\n") #writes save dict to save.txt

def read(): #reads from save.txt
    global save_dict
    global board
    global users
    global game_state
    global time_delay
    global heart_delay

    with open("save.txt","r", encoding='utf-8') as save:

        save_dict = eval(save.read()) #reads the file, sets contents to save_dict

        board = save_dict["board"] #sets all respective variables 
        users = save_dict["users"]
        game_state = save_dict["game_state"]
        time_delay = save_dict["time_delay"]
        heart_delay = save_dict["heart_delay"]

def reset(): #resets the game 
    global board
    global users
    global game_state

    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],]

    users = {}

    game_state = "null"

    save()

async def update_board_string(): #updates the board 
    global board_string
    global board_message

    board_string = ""

    for row in board:

        for element in row:  #loops through each cell in the board

            if element in users: #if it is a user id, set it as their emoji
                board_string += users[element]["emoji"]
            elif element == 0: #if it is 0, set it as fog
                board_string += ":fog:"
            elif element == 1: #if it is 1, set it as a heart
                board_string += ":heart:"
            else: #else, set as x (should never happen, just cautionary)
                board_string += ":x:"

        board_string += "\n"

    try:
        await board_message.edit(content=board_string) #edits message that holds the board (try statement because sometimes it lags and cant edit)
    except:
        pass


@client.event
async def on_ready():
    global board
    global channel
    global board_message
    global users
    global board_string

    

    channel = client.get_channel(channel_id)  #sets channel variable

    await channel.edit(slowmode_delay=3) #sets slowmode (3 seconds)

    await channel.send("Tank Bot is now online")

    try:
        read() #reads save, excepts if error 
    except:
        await channel.send("Error reading save")
        reset() #if error, reset

    if game_state == "started": #if the game was already in progress
            
        ap_event.change_interval(seconds=time_delay) #start the background loops
        ap_event.start()
        heart_event.change_interval(seconds=heart_delay)
        heart_event.start()

    board_message = await channel.send("Loading...", view=view_init()) #sends original board message, board message is the message that is edited to show the board
    await update_board_string()
    
@client.event
async def on_message(message):
    global channel
    global board_message

    if(message.author.bot): #if message is sent by a bot, return to avoid a loop of message sending from the bot
        return

    try:
        await board_message.delete() #makes it so that the value_message is always visible in the channel, deletes it and resends it
        board_message = await channel.send(board_string, view=view_init())
    except:
        pass

    if message.channel.id != channel_id and message.content.startswith("!"): #makes it so that the bot only works in desired channel
        await message.channel.send("Please use the Tank Tactics text channel for commands")
        return

    await client.process_commands(message) #makes it so that the bot can still process commands
        

@client.command()
async def start(ctx, amount: int = None, units = None, heart_multiplier: int = None):
    global game_state
    global time_delay
    global heart_delay
    
    if ctx.author.id != admin_id: #only admin can start
        await channel.send("You do not have permission to use that command")
        return

    if game_state == "null" and heart_multiplier == None: #makes sure all parameters are given
        await channel.send("Please enter the multiplier to determine the interval for the heart spawn")
        return

    if game_state == "null" and (amount == None or units == None): #makes sure all parameters are given
        await channel.send("Please enter an amount and units for the AP time delay")
        return
    elif game_state == "null" and (amount != None and units != None):

        if units == "seconds" or units == "second": #sets delays accordingly
            time_delay = amount
            heart_delay = heart_multiplier * time_delay
        elif units == "minutes" or units == "minute":
            time_delay = amount * 60
            heart_delay = heart_multiplier * time_delay
        elif units == "hours" or units == "hour":
            time_delay = amount * 3600
            heart_delay = heart_multiplier * time_delay
        else:
            await channel.send("Please enter a valid unit (seconds, minutes, hours)") #makes sure all parameters are given
            return



    if game_state == "null":
        game_state = "lobby"
        await channel.send("Lobby phase has been started, waiting for players to join...")
    elif game_state == "lobby":
        game_state = "started"
        await channel.send("Game has been started")
        #TODO: start game 
        ap_event.change_interval(seconds=time_delay)
        ap_event.start()

        heart_event.change_interval(seconds=heart_delay)
        heart_event.start()

    elif game_state == "started":
        await channel.send("Game has already been started")

    save()

@client.command()
async def end(ctx):

    if ctx.author.id != admin_id: #only admin can end
        await channel.send("You do not have permission to use that command")
        return

    ap_event.stop() #stops loops
    heart_event.stop()

    reset() #resets game
    await update_board_string()
    await channel.send("Game ended") #confirmation message

@client.command()
async def join(ctx, emoji : str = None): #joins game if in lobby phase
    global board
    global board_coords
    global users

    if ctx.author.id in users: #you can only join once
        await channel.send("You have already joined this game")
        return

    if game_state != "lobby": #only join in lobby phase
        await channel.send("You can only join when the game is in joining phase")
        return

    if emoji == None: #makes sure emoji parameter is given
        await channel.send("Please choose an emoji to play with")
        return

    if emoji == ":heart:": #cannot use heart because it spawns in the map
        await channel.send("You cannot use the heart emoji")
        return

    if emoji == ":fog:": #cannot use fog because that is the background
        await channel.send("You cannot use the fog emoji")
        return

    if emojis.count(emoji) == 1:
        emoji = list(emojis.get(emoji))[0] #removes everything but the emoji and sets it to the emoji variable

        for user in users: #cannot choose an emoji someone else chose
            if emoji == users[user]["emoji"]:
                await channel.send("Someone already chose that emoji")
                return
        
    else:
        await channel.send("Please send a valid emoji") #makes sure emoji parameter is given correctly
        return

    users[ctx.author.id] = copy.deepcopy(default_user_stats) #creates a copy of the default stats, adds it to the main users dictionary

    users[ctx.author.id]["emoji"] = emoji #sets the emoji of the user


    coordinates_tuple = board_coords.pop() #gets random unused position on the board
    users[ctx.author.id]["coords"]["y"] = coordinates_tuple[0] #sets x and y of player
    users[ctx.author.id]["coords"]["x"] = coordinates_tuple[1]



    board[users[ctx.author.id]["coords"]["y"]][users[ctx.author.id]["coords"]["x"]] = ctx.author.id #sets board position to id

    save() #saves and updates board
    await update_board_string()


@client.command() #see button_up for comments on functionality
async def up(ctx, amount: int = 1): #only thing different is that amount can be given as a parameter for precise movement
    print("hello")
    if ctx.author.id not in users:
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started":
        await channel.send("The game has not started yet")
        return
    if users[ctx.author.id]["ap"] < 1:
        await channel.send("You do not have enough AP to do that")
        return
    if amount > users[ctx.author.id]["speed"]:
        await channel.send("You cannot move farther than your speed")
        return
    if users[ctx.author.id]["coords"]["y"] - amount < 0:
        await channel.send("You cannot move out of bounds")
        return
    for user in users:
        if (users[ctx.author.id]["coords"]["y"] - amount, users[ctx.author.id]["coords"]["x"]) == (users[user]["coords"]["y"], users[user]["coords"]["x"]):
            await channel.send("You cannot move into another player's square")
            return
    
    if board[users[ctx.author.id]["coords"]["y"] - amount][users[ctx.author.id]["coords"]["x"]] == 1:
        await channel.send(f"**{ctx.author.name}** has collected a heart!")
        users[ctx.author.id]["hp"] += 1


    board[users[ctx.author.id]["coords"]["y"]][users[ctx.author.id]["coords"]["x"]] = 0
    users[ctx.author.id]["coords"]["y"] -= amount
    board[users[ctx.author.id]["coords"]["y"]][users[ctx.author.id]["coords"]["x"]] = ctx.author.id
    users[ctx.author.id]["ap"] -= 1

    save()
    await update_board_string()

@client.command() 
async def down(ctx, amount: int = 1): #see up() for comments on functionality
    if ctx.author.id not in users:
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started":
        await channel.send("The game has not started yet")
        return
    if users[ctx.author.id]["ap"] < 1:
        await channel.send("You do not have enough AP to do that")
        return
    if amount > users[ctx.author.id]["speed"]:
        await channel.send("You cannot move farther than your speed")
        return
    if users[ctx.author.id]["coords"]["y"] + amount > 12:
        await channel.send("You cannot move out of bounds")
        return
    for user in users:
        if (users[ctx.author.id]["coords"]["y"] + amount, users[ctx.author.id]["coords"]["x"]) == (users[user]["coords"]["y"], users[user]["coords"]["x"]):
            await channel.send("You cannot move into another player's square")
            return

    if board[users[ctx.author.id]["coords"]["y"] + amount][users[ctx.author.id]["coords"]["x"]] == 1:
        await channel.send(f"**{ctx.author.name}** has collected a heart!")
        users[ctx.author.id]["hp"] += 1


    board[users[ctx.author.id]["coords"]["y"]][users[ctx.author.id]["coords"]["x"]] = 0
    users[ctx.author.id]["coords"]["y"] += amount
    board[users[ctx.author.id]["coords"]["y"]][users[ctx.author.id]["coords"]["x"]] = ctx.author.id
    users[ctx.author.id]["ap"] -= 1

    save()
    await update_board_string()

@client.command()
async def left(ctx, amount: int = 1): #see up() for comments on functionality
    if ctx.author.id not in users:
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started":
        await channel.send("The game has not started yet")
        return
    if users[ctx.author.id]["ap"] < 1:
        await channel.send("You do not have enough AP to do that")
        return
    if amount > users[ctx.author.id]["speed"]:
        await channel.send("You cannot move farther than your speed")
        return
    if users[ctx.author.id]["coords"]["x"] - amount < 0:
        await channel.send("You cannot move out of bounds")
        return
    for user in users:
        if (users[ctx.author.id]["coords"]["y"], users[ctx.author.id]["coords"]["x"] - amount) == (users[user]["coords"]["y"], users[user]["coords"]["x"]):
            await channel.send("You cannot move into another player's square")
            return

    if board[users[ctx.author.id]["coords"]["y"]][users[ctx.author.id]["coords"]["x"] - amount] == 1:
        await channel.send(f"**{ctx.author.name}** has collected a heart!")
        users[ctx.author.id]["hp"] += 1


    board[users[ctx.author.id]["coords"]["y"]][users[ctx.author.id]["coords"]["x"]] = 0
    users[ctx.author.id]["coords"]["x"] -= amount
    board[users[ctx.author.id]["coords"]["y"]][users[ctx.author.id]["coords"]["x"]] = ctx.author.id
    users[ctx.author.id]["ap"] -= 1

    save()
    await update_board_string()

@client.command()
async def right(ctx, amount: int = 1): #see up() for comments on functionality
    if ctx.author.id not in users:
        await channel.send("You must join the game before you can do that")
        return
    if game_state != "started":
        await channel.send("The game has not started yet")
        return
    if users[ctx.author.id]["ap"] < 1:
        await channel.send("You do not have enough AP to do that")
        return
    if amount > users[ctx.author.id]["speed"]:
        await channel.send("You cannot move farther than your speed")
        return
    if users[ctx.author.id]["coords"]["x"] + amount > 12:
        await channel.send("You cannot move out of bounds")
        return
    for user in users:
        if (users[ctx.author.id]["coords"]["y"], users[ctx.author.id]["coords"]["x"] + amount) == (users[user]["coords"]["y"], users[user]["coords"]["x"]):
            await channel.send("You cannot move into another player's square")
            return

    if board[users[ctx.author.id]["coords"]["y"]][users[ctx.author.id]["coords"]["x"] + amount] == 1:
        await channel.send(f"**{ctx.author.name}** has collected a heart!")
        users[ctx.author.id]["hp"] += 1

    board[users[ctx.author.id]["coords"]["y"]][users[ctx.author.id]["coords"]["x"]] = 0
    users[ctx.author.id]["coords"]["x"] += amount
    board[users[ctx.author.id]["coords"]["y"]][users[ctx.author.id]["coords"]["x"]] = ctx.author.id
    users[ctx.author.id]["ap"] -= 1

    save()
    await update_board_string()

@client.command()
async def stats(ctx, user: discord.Member = None): #prints user stats

    if ctx.author.id not in users: #you can only check stats if user joined
        await channel.send("You must join the game before you can do that")
        return
    if game_state == "null": #only checkable if game is in lobby/started phase
        await channel.send("The game has not started yet")
        return

    if user == None: #sends own stats
        await channel.send(f"\n**{ctx.author.name}**:  Emoji: {users[ctx.author.id]['emoji']}  HP: {users[ctx.author.id]['hp']}  AP: {users[ctx.author.id]['ap']}  Range: {users[ctx.author.id]['range']}  Speed: {users[ctx.author.id]['speed']}")
    else: #if a parameter is given, send that players stats
        await channel.send(f"\n**{user.name}**:  Emoji: {users[user.id]['emoji']}  HP: {users[user.id]['hp']}  AP: {users[user.id]['ap']}  Range: {users[user.id]['range']}  Speed: {users[user.id]['speed']}")


@client.command() #see button_give for comments on functionality
async def give(ctx, amount: int, member: discord.Member): #only difference is that you can choose amount and target
    
    if game_state != "started":
        await channel.send("The game has not started yet")
        return

    if ctx.author.id not in users: 
        await channel.send("That person is not in the game")
        return

    if abs(users[ctx.author.id]["coords"]["x"] - users[member.id]["coords"]["x"]) > users[ctx.author.id]["range"] or abs(users[ctx.author.id]["coords"]["y"] - users[member.id]["coords"]["y"]) > users[ctx.author.id]["range"]:
        await channel.send("That person is out of range")
        return

    if amount < 0: 
        await channel.send("You cannot give a negative amount")
        return

    if ctx.author.id == member.id: 
        await channel.send("You cannot give to yourself.")
        return

    if users[ctx.author.id]["ap"] >= amount:
        users[ctx.author.id]["ap"] -= amount
        users[member.id]["ap"] += amount
        await channel.send(f":dizzy: **{ctx.author.name}** gave {amount} AP to **{member.name}**")
        save() #saves to save file
    else:
        await channel.send("You do not have enough AP to give that amount.")

@client.command() #see button_shoot for comments on functionality
async def shoot(ctx, member: discord.Member = None): #only difference is that you can choose target with a parameter
    
    if game_state != "started":
        await channel.send("The game has not started yet")
        return

    if ctx.author.id not in users: 
        await channel.send("You are not in the game")
        return
    if users[ctx.author.id]["ap"] < 1:
        await channel.send("You do not have enough AP to do that")
        return 


    if abs(users[ctx.author.id]["coords"]["x"] - users[member.id]["coords"]["x"]) > users[ctx.author.id]["range"] or abs(users[ctx.author.id]["coords"]["y"] - users[member.id]["coords"]["y"]) > users[ctx.author.id]["range"]:
        await channel.send("That person is out of range")
        return

    users[ctx.author.id]["ap"] -= 1
    users[member.id]["hp"] -= 1

    user_object = client.get_user(member.id)

    if users[member.id]["hp"] == 0:
        await channel.send(f":skull: **{ctx.author.name}** shot and killed **{user_object.name}**")

        board[users[member.id]["coords"]["y"]][users[member.id]["coords"]["x"]] = 0

        users[ctx.author.id]["ap"] += users[member.id]["ap"]

        del users[member.id]

        if len(users) == 1:
            await channel.send(f":trophy::trophy::trophy:  **{ctx.author.name} won!!!**  :trophy::trophy::trophy:")
            await update_board_string()
            
        await update_board_string()
        save()
        


    else:
        await channel.send(f":broken_heart: **{ctx.author.name}** shot **{user_object.name}**")

        await update_board_string()
        save()


@client.command()
async def commandlist(ctx):  #sends a list of commands
    command_string = "**Text Commands:**"
    command_string += "\n!start <amount> <units> <heart_respawn_multiplier> - starts the lobby phase, parameters control the time delay for AP and Heart spawns"
    command_string += "\n!start - starts the game from the lobby phase"
    command_string += "\n!join <emoji> - join the game when in lobby phase"
    command_string += "\n!stats <player> - shows player stats, defaults to self if no argument is given"
    command_string += "\n!up <amount> - move up a certain amount"
    command_string += "\n!down <amount> - move down a certain amount"
    command_string += "\n!left <amount> - move left a certain amount"
    command_string += "\n!right <amount> - move right a certain amount"
    command_string += "\n!shoot <player> - shoot a player within Range (cost 1 AP)"
    command_string += "\n!give <amount> <player> - give a player a certain amount of AP within Range"
    command_string += "\n**Button Commands:**"
    command_string += "\n:arrow_up: - move up by speed"
    command_string += "\n:arrow_down: - move down by speed"
    command_string += "\n:arrow_left: - move left by speed"
    command_string += "\n:arrow_right: - move right by speed"
    command_string += "\n:scroll: Leaderboard - shows all player stats"
    command_string += "\n:heart: - buy a heart for 3 AP, increasing HP by 1"
    command_string += "\n:arrow_double_up: Range - increase Range by 1, costing 3 AP"
    command_string += "\n:arrow_double_up: Speed - increase Speed by 1, costing 3 AP"
    command_string += "\n:dizzy: Give - give 1 AP to the closest player to you"
    command_string += "\n:dagger: Shoot - shoot the closest player to you, costing 1 AP"

    await channel.send(command_string)

@client.command()
async def rules(ctx): #sends rules
    await channel.send("https://docs.google.com/document/d/1lxSeXA_7QfV4SBzh311vfT8645aGC0BfIenh324gU5g/edit?usp=sharing")


@tasks.loop(seconds=10) #10 is placeholder amount, it gets changed
async def ap_event(): #gives everyone an ap
    for user in users:
        users[user]["ap"] += 1
    await channel.send(":white_check_mark: AP has been distributed")
    save()

@tasks.loop(seconds=10) #10 is placeholder amount, it gets changed
async def heart_event(): #spawns a heart at random location

    for row in board:
        for element in row:
            if element == 1: #if there is already a heart on the board, do nothing
                return


    while True: #chooses an open board position (i know this method sucks)
        x = rand.randint(0, 12)
        y = rand.randint(0, 12)

        if board[y][x] == 0:
            break

    board[y][x] = 1 #sets the position to a heart

    save() #saves and updates board
    await update_board_string()


@client.command()
async def addap(ctx): #debug command
    if ctx.author.id == admin_id:
        users[ctx.author.id]["ap"] += 100
    else:
        return

@client.command()
async def ping(ctx): #basic ping command (used for debug)
    await channel.send("pong")


client.run(token) #token