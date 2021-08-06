import discord

from discord import client
from discord.ext import commands
import os
import random
from discord.ext.commands.bot import Bot
from discord_slash.utils.manage_commands import create_choice, create_option

from dotenv import load_dotenv
from discord_slash import SlashCommand



client = commands.Bot(command_prefix = '/')
guildID=*GuildIDS*
load_dotenv()
slash = SlashCommand(client, sync_commands=True)
helloList = ['Howdy!', ':/', 'Hello!', 'What do you want >:(', "What's up!", "Greetings!", "Hey!", "Yo yo yo!", '¿Qué tal?', 'Hola!', 'Bonjour!', '今日は', '你好', '안녕하세요', 'Hallo!', 'Ciao!', 'नमस्ते', 'γεια σας', 'Salve', 'مرحبا', 'Kamusta', 'Olá', 'Xin chào', 'Привет']


DESCRIPTION = {
    'hello': 'Use /hello in the chat to greet mahthieuBot.',
    'ping': 'Use /ping to check mahthieuBot\'s latency.',
    'rps': 'Command to start a game of Rock Paper Scissors against mahthieuBot!\n\nHow to Play:\n\nType "/rps <rock/paper/scissors>" and then mahthieuBot will also make a selection. Rock beats scissors, scissors beats paper, and paper beats rock. If you and mahthieuBot make the same selection then the game will draw.',
    'tttstart': 'Use /tttstart to start a Tic Tac Toe Game!\n\nRules:\nThe Tic Tac Toe board is a 3x3 board which we will number like so:\n\n1|2|3\n------\n4|5|6\n------\n7|8|9\n\nWhen command entered, the bot will randomly select who be X\'s and O\'s at the start of the game and randomly select who will start.\n\nFirst to get three in a row wins. \n\nExample of a win:\n\nX|O|X\n------\nO|X|O\n------\nO|X|X\n\nExample of a draw:\n\nO|X|O\n------\nX|X|O\n------\nX|O|X\n\n',
    'tttplace': 'Use /tttplace to place your piece during a Tic Tac Toe Game.\n\nThe Tic Tac Toe board is a 3x3 board which we will number like so:\n\n1|2|3\n------\n4|5|6\n------\n7|8|9\n\nA game must be in progress in order to run this command.'}


rpsChoices = [
    'Rock',
    'Paper',
    'Scissors',
]

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    status = discord.Game('/help')
    await client.change_presence(activity=status)

@slash.slash(
    name="help",
    description="Find help for any command with '/help <command>'",
    guild_ids=guildID,
    options=[
        create_option(name="commands",
        description="Which command do you need help with?",
        option_type=3,
        required=True,
        choices=[
            create_choice(
                name='hello',
                value='hello'
            ),
            create_choice(
                name='ping',
                value='ping'
            ),
            create_choice(
                name="rps",
                value="rps"
            ),
            create_choice(
                name="tttstart",
                value='tttstart'
            ),
            create_choice(
                name="tttplace",
                value='tttplace'
            ),

        ])
        
    ]
)
async def help(ctx, commands):
    embed = discord.Embed(
        title = "HELP",
        description = "Welcome to mahthieuBot! Use '/help <command>' for more info.",
    )
    embed.add_field(name="\u200b\nCommands", value = "hello | ping | rps | tttstart | tttplace", inline=False),

    embed.add_field(name="\u200b\n" + commands, value=DESCRIPTION[commands], inline=False)
    await ctx.send(embed=embed)



@slash.slash(
    name="ping",
    description="Shows mahthieuBot latency",
    guild_ids=guildID
)
async def ping(ctx):
    embed = discord.Embed(
        title = "mahthieuBot Ping",
        description=f'Bot Speed - {round(client.latency *1000)}ms'
    )
    await ctx.send(embed=embed)

@slash.slash(
    name="hello",
    description="Come and greet mahthieuBot!",
    guild_ids=guildID,

)
async def hello(ctx):
    await ctx.send(random.choice(helloList))

@slash.slash(
    name="tttstart",
    description="Start a Tic Tac Toe game!",
    guild_ids=guildID,
    )
async def tttstart(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Please finish the game before starting a new one.")

@slash.slash(
    name="tttplace",
    description="Place during your TTT Game",
    guild_ids=guildID,
    )
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose a number between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the tttstart command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tttstart.error
async def tttstart_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter a number.")


@slash.slash(
    name="rps",
    description="Rock Paper Scissors Game!",
    guild_ids=guildID,
    options=[
        create_option(
        name="choices",
        description="Your choices for the Rock Paper Scissors game.",
        option_type=3,
        required=True,
        choices=[
            create_choice(
                name="Rock",
                value="Rock"
            ),
            create_choice(
                name="Paper",
                value="Paper"
            ),
            create_choice(
                name="Scissors",
                value="Scissors"
            )
        ]
    )
    ]

)
async def rps(ctx, choices):
    embed = discord.Embed(
        title = "Rock Paper Scissors Game"
    )
    player_choice = choices
    bot_choice = random.choice(rpsChoices)
    result = ""
    result_title = ""
    if player_choice == "Rock" and bot_choice == "Rock":
        result = "Draw"
        result_title = "No Winner :/"
    elif player_choice == "Paper" and bot_choice == "Paper":
        result = "Draw"
        result_title = "No Winner :/" 
    elif player_choice == "Scissors" and bot_choice == "Scissors":
        result = "Draw"
        result_title = "No Winner :/"   
    elif player_choice == "Paper" and bot_choice == "Rock":
        result = "You win!"
        result_title = "Result!"   
    elif player_choice == "Paper" and bot_choice == "Scissors":
        result = "You lose :("
        result_title = "Result!"
    elif player_choice == "Scissors" and bot_choice == "Rock":
        result = "You lose :("
        result_title = "Result!"   
    elif player_choice == "Scissors" and bot_choice == "Paper":
        result = "You win!"
        result_title = "Result!"   
    elif player_choice == "Rock" and bot_choice == "Paper":
        result = "You lose :("
        result_title = "Result!"   
    elif player_choice == "Rock" and bot_choice == "Scissors":
        result = "You win!"
        result_title = "Result!"   

    embed.add_field(name="\u200b\nYour choice", value=player_choice, inline=False)
    embed.add_field(name="\u200b\nmahthieuBot's choice", value=bot_choice, inline=False)
    embed.add_field(name="\u200b\n" + result_title,value=result, inline=False)
    await ctx.send(embed = embed)



client.run(os.getenv('TOKEN'))