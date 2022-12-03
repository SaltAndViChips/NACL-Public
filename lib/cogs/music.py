from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
from discord.utils import get


class music(Cog):
    def __init__(self, bot):
        self.bot = bot









    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("music")

async def setup(bot):
    await bot.add_cog(music(bot))