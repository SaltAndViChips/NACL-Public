from discord import Embed
from random import *
import asyncio

async def rockpaperscissors(self, ctx):
    gamewindow = Embed(
                    title="Rock Paper Scissors",
                    description="Let's play\nRock Paper Scissors!",
                    color=0x00FA9A,
                )
    gamewindow.set_footer(text="♥")
    gamewindow.set_author(name="Salt And Vi Chips", icon_url=self.guild.icon_url)
    buttons = [u"\1FAA8", u"\1F4F0", u"\2702", "\274C"]
    UserChoice = None
    BotChoice = randint(0,2)
    msg = await ctx.send(embed=embed)
    for button in buttons:
        await msg.add_reaction(button)
    while True:
        try:
            reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

        except asyncio.TimeoutError:
            TempEmbed = gamewindow
            TempEmbed.set_footer(text="Timed Out")
            await msg.edit(embed=TempEmbed)
            await msg.clear_reactions()

        else:
            previous_page = current

            if reaction.emoji == buttons[0]:
                 UserChoice = 0

            elif reaction.emoji == buttons[1]:
                UserChoice = 1

            elif reaction.emoji == buttons[2]:
                UserChoice = 2
            elif reaction.emoji == buttons[3]:
                TempEmbed = gamewindow
                TempEmbed.set_footer(text="You have quit!")
                await msg.edit(embed=TempEmbed)
                await msg.clear_reactions()


            for button in buttons:
                await msg.remove_reaction(button, ctx.author)

            if UserChoice != None:
                await msg.edit(embed=gamestate(UserChoice,BotChoice))
                await msg.clear_reactions()

def gamestate(UserChoice, BotChoice):
    Tie = "You have Tied!"
    Win = "You Won! Congratulations!"
    Lose = "You Lost! Better luck next time!"
    Choices=["Rock","Paper","Scissors"]
    if UserChoice == BotChoice:
        Outcome = Tie
    elif UserChoice == 0 & BotChoice == 2:
        Outcome = Win
    elif UserChoice == 1 & BotChoice == 0:
        Outcome = Win
    elif UserChoice == 2 & BotChoice == 1:
        Outcome = Win
    else:
        Outcome = Lose
    gameboard = Embed(
        title="Rock Paper Scissors",
        description=f"You Chose: {Choices[UserChoice]}\nI chose: {Choices[BotChoice]}\n{Outcome}\nGood Game!",
        color=0x00FA9A,
    )
    gameboard.set_footer(text="♥")
    gameboard.set_author(name="Salt And Vi Chips", icon_url=self.guild.icon_url)
    return gameboard
