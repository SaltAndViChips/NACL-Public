from random import choice, randint
from typing import Optional
from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed

class social(Cog):
    def __init__(self, bot):
        self.bot = bot

    # @command(name="command", aliases=["cmd", "c"], hidden=True)
    # async def command(self, ctx):
    #     pass
    @command(name="spotify", aliases=("music", "tunes", "goodshit"), hidden=False)
    async def spotify(self, ctx):
        embed = Embed(
            title="Check Out My Spotify!",
            color=0x00FA9A,
            url="https://open.spotify.com/user/225ebhn2g7tnut36eyooatbwy?si=50d721897bb0435d"
        )
        embed.set_image(url="https://platform-lookaside.fbsbx.com/platform/profilepic/?asid=10207417777755236&height=300&width=300&ext=1623745640&hash=AeQrQZf7UP3OVOl_Ra0")
        embed.set_author(name="NaCl Bot | Socials")
        embed.set_footer(text="♥")
        await ctx.send(embed=embed)


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("social")

    # @Cog.listener()


async def setup(bot):
    await bot.add_cog(social(bot))
