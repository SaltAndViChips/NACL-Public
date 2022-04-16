from random import choice, randint
from typing import Optional
from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import has_permissions
from discord import Embed
from ..db import db

class events(Cog):
    def __init__(self, bot):
        self.bot = bot


    # @Cog.listener()
    # async def on_member_join(self, member):
    #     db.execute("INSERT INTO users (UserID) VALUES ?", member.id)



    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("events")

    # @Cog.listener()


async def setup(bot):
    await bot.add_cog(events(bot))