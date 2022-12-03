from random import choice, randint
from typing import Optional
from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed
import asyncio

class help(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="helpembed", aliases=["newhelp"])
    async def newhelp(self,ctx):
        buttons = [u"\u23EA", u"\u25C0", u"\u25B6", "⏩"]
        current = 0
        help_page1 = Embed(
            title="Help | Page 1",
            description="Basic Commands",
            color=0x00Fa9a
        )
        fields = [("History", "Shows Users Punishment History", True),
                  ("Slap", "Slaps The User (For Fun!)", True)]
        for name, value, inline in fields:
            help_page1.add_field(name=name, value=value, inline=False)
        help_page_admin = Embed(
            title="Help | Admin Commands",
            color=0x00Fa9a
        )
        fields = [("Blacklist", "Blacklist a user from using this bot", False),
                  ("Clear", "Deletes up to 100 messages in the current channel", False),
                  ("History", "Show User Moderation History", True),
                  ("quit", "Restarts the bot (Dev Only, Sorry!)", True),
                  ("rolekick", "Kicks all users with a given role (Use the roles ID)", True),
                  ("unblacklist", "Unblacklists a user from using this bot", True),
                  ("warn", "Warns the user!", True)
                  ]
        for name, value, inline in fields:
            help_page_admin.add_field(name=name, value=value, inline=False)
        # help_page_admin.set_footer(text="Page #2")
        help_pages = [help_page1, help_page_admin]

        msg = await ctx.send(embed=help_pages[current])

        for button in buttons:
            await msg.add_reaction(button)
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout=60.0)

            except asyncio.TimeoutError:
                embed = help_pages[current]
                embed.set_footer(text="Timed Out")
                await msg.edit(embed=help_pages[current])
                await msg.clear_reactions()

            else:
                previous_page = current

                if reaction.emoji == "\u23EA":
                    current = 0

                elif reaction.emoji == "\u25C0":
                    if current > 0:
                        current -= 1

                elif reaction.emoji == "\u25B6":
                    if current < len(help_pages) - 1:
                        current += 1
                elif reaction.emoji == "\u23E9":
                    current = len(help_pages) - 1

                for button in buttons:
                    await msg.remove_reaction(button, ctx.author)

                if current != previous_page:
                    await msg.edit(embed=help_pages[current])


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")

    # @Cog.listener()


async def setup(bot):
    await bot.add_cog(help(bot))