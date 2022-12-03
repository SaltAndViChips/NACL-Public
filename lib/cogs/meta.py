from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Activity, ActivityType
from apscheduler.triggers.cron import CronTrigger


class Meta(Cog):
    def __init__(self, bot):
        self.bot = bot
        self._message = "watching {users:,} users commit tax evasion  |  {bots:,} other bots"

        bot.scheduler.add_job(self.set, CronTrigger(second=30))


    @property
    def message(self):
        return self._message.format(users=len([x for x in self.bot.users if not x.bot]), guilds=len(self.bot.guilds), bots = len([x for x in self.bot.users if x.bot] ))

    @message.setter
    def message(self, value):
        if value.split(" ")[0] not in ("playing", "watching", "listening-to", "streaming"):
            raise ValueError("Invalid activity type!")

        self._message = value

    async def set(self):
        _type, _name = self.message.split(" ", maxsplit=1)

        await self.bot.change_presence(activity=Activity(
            name=_name, type=getattr(ActivityType, _type, ActivityType.playing)
        ))


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("meta")

    # @Cog.listener()


async def setup(bot):
    await bot.add_cog(Meta(bot))