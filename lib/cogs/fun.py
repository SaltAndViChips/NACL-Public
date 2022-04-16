import asyncio
from random import choice, randint
from typing import Optional
from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import NotOwner as devonly
from discord import Embed


class fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="rpc", aliases=["rock","paper","scissors"])
    async def rpc(self, ctx):
        gamewindow = Embed(
                title="Rock Paper Scissors",
                description="Let's play\nRock Paper Scissors!",
                color=0x00FA9A,
            )
        gamewindow.set_footer(text="♥")
        buttons = ["🪨", "📜", "✂", "❌"]
        BotChoice = randint(0, 2)
        msg = await ctx.send(embed=gamewindow)
        Enabled=True
        for button in buttons:
            await msg.add_reaction(button)
        async def closegame():
            await asyncio.sleep(10)
            await msg.delete()
        def gamestate(UserChoice, BotChoice):
            Tie = "You have Tied!"
            Win = "You Won! Congratulations!"
            Lose = "You Lost! Better luck next time!"
            Choices = ["Rock", "Paper", "Scissors"]
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
                description=f"You Chose: {Choices[UserChoice]}\n\nI chose: {Choices[BotChoice]}\n\n{Outcome}\n\nGood Game!",
                color=0x00FA9A,
            )
            gameboard.set_footer(text="♥")
            return gameboard

        while Enabled==True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                await closegame()


            else:
                UserChoice = None

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
                    await asyncio.sleep(5)

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if UserChoice != None:
                    await msg.edit(embed=gamestate(UserChoice, BotChoice))
                    Enabled=False
                    await closegame()




    @command(name="hello", aliases=["hi"])
    async def say_hello(self, ctx):
        await ctx.send(f"{choice(('Hello','Howdy','Sup','Bonjour',))} {ctx.author.mention}!")

    @command(name="parrot", aliases=["polly", "echo"])
    async def poly_parrot(self, ctx, *, phrase: Optional[str] = "**Silence Falls Over The Room**"):
        await ctx.send(phrase)

    @command(name="dice", aliases=["r", "roll"])
    async def roll_dice(self, ctx, die_string: str):
        dice, value = (int(term) for term in die_string.split("d"))
        rolls = [randint(1, value) for i in range(dice)]

        await ctx.send(" + ".join([str(r) for r in rolls]) + f" = {sum(rolls)}")

    @command(name="slap")
    async def slap_member(self, ctx, member: Optional [Member], *, reason: Optional[str] = "No Reason Given"):
        if member == None:
            embed=Embed(
                title="Invalid Entry",
                description="You need to pick someone to slap silly"
            )
            await ctx.send(embed=embed)
        else:
            embed = Embed(
                author="NaCl Bot | Fun Commands",
                title=f"You've Been Slapped",
                description=f"{ctx.author.mention} slapped {member.mention} | Reason: {reason}",
                color=0x00FA9A,

            )
            await ctx.send(embed=embed)

    @command(name="rivens", aliases=["rivs", "riv", "riven"], hidden=False)

    async def rivenlist(self, ctx):
        rivens = []
        with open("./lib/items/rivens.txt", "r", encoding="utf-8") as rl:
            items = []
            for line in rl:
                stripped_line = line.strip()
                line_split = stripped_line.split("|")
                items.append(line_split)
            for riven in range(len(items)):
                tempembed = Embed(
                    title="Salts Rivens",
                    description=items[riven][1],
                    color=0x00FA9A
                )
                tempembed.set_image(url=items[riven][0])
                new_var = (f"r{riven}")
                exec(new_var + " = tempembed")
                rivens.append(eval(f"r{riven}"))

        buttons = [u"\u23EA", u"\u25C0", u"\u25B6", "⏩"]
        current = 0
        msg = await ctx.send(embed=rivens[current])

        for button in buttons:
            await msg.add_reaction(button)
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                embed = rivens[current]
                embed.set_footer(text="Timed Out")
                await msg.edit(embed=rivens[current])
                await msg.clear_reactions()

            else:
                previous_page = current

                if reaction.emoji == "\u23EA":
                    current = 0

                elif reaction.emoji == "\u25C0":
                    if current > 0:
                        current -= 1

                elif reaction.emoji == "\u25B6":
                    if current < len(rivens)-1:
                        current += 1
                elif reaction.emoji == "\u23E9":
                    current = len(rivens)-1

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(embed=rivens[current])



    # @command(name="command", aliases=["cmd", "c"], hidden=True)
    # async def command(self, ctx):
    #     pass


    # @command(name="paris")
    # @devonly
    # async def who_was_in_paris(self, ctx):
    #




    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")

    # @Cog.listener()

async def setup(bot):
    await bot.add_cog(fun(bot))
