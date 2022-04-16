from asyncio import run as run_async
from asyncio import sleep
from datetime import datetime
from glob import glob
from pathlib import Path

import tzlocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed
from discord import Intents
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, BotMissingPermissions, \
    MissingPermissions, BadColourArgument
from discord.ext.commands import MemberNotFound
from discord.ext.commands import NotOwner
from discord.ext.commands import when_mentioned_or
import os

from ..db import db


def get_prefix(Bot, message):
    prefix = db.field("SELECT Prefix FROM guilds Where GuildID = ?", message.guild.id)
    return when_mentioned_or(prefix)(Bot, message)


# Timezone scheduler
# timezone = pytz.timezone("Canada/Eastern")
# dt = datetime.now(tz=timezone)

# Dev Account IDs

SaltID = 92276895185387520

OWNER_IDS = [SaltID]

# Grab Cogs
COGPATH = Path("./lib/cogs/*.py")
COGS = [path.split("\\" or "/")[-1][:-3] for path in glob(COGPATH)]


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} Initialized".capitalize())

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])

class BreakExcept(Exception):
    pass


class Bot(BotBase):
    TOKEN: str
    UPDATE: str
    VERSION: str

    def __init__(self):
        self.guild = None
        self.stdout = None
        self.ready = False
        self.cogs_ready = Ready()
        # self.guild = None
        self.scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))
        self.dt = datetime.now(tz=self.scheduler.timezone)

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=get_prefix,
            owner_ids=OWNER_IDS,
            intents=Intents.all(),
        )

    async def setup(self):
        for cog in COGS:
            await self.load_extension(f"lib.cogs.{cog}")

    def update_db(self):
        db.multiexec("INSERT OR IGNORE INTO guilds (GuildID) VALUES (?)",
                     ((guild.id,) for guild in self.guilds))
        db.multiexec("INSERT OR IGNORE INTO users (UserID) VALUES (?)",
                     ((member.id,) for guild in self.guilds for member in guild.members))
        db.multiexec("INSERT OR IGNORE INTO moods (UserID) VALUES (?)",
                     ((member.id,) for guild in self.guilds for member in guild.members))
        db.multiexec("INSERT OR IGNORE INTO warns (UserID) VALUES (?)",
                     ((member.id,) for guild in self.guilds for member in guild.members))
        for guild in self.guilds:
            db.execute(
                f"CREATE TABLE IF NOT EXISTS \"{str(guild.id)}\" (UserID integer PRIMARY KEY, "
                f"Blacklist integer, Banlist integer)")

        # print ("Updating DB!")
        db.commit()

    async def print_message(self):
        self.stdout = self.get_channel(600001330920292353)
        self.guild = self.get_guild(535693863696990208)
        pass


    def run(self, version, update):
        self.VERSION = version
        self.UPDATE = update


        print("Starting Up...")
        run_async(self.setup())

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = os.getenv("DISCORD_TOKEN") or tf.read()
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print(
            f"""
Bot Connected:
As {bot.user.name} | {bot.user.id}
{self.dt.hour}:{self.dt.minute:02d}:{self.dt.second:02d}
Date: {self.dt.day:02d}/{self.dt.month:02d}/{self.dt.year}
""")

    async def on_reconnect(self):
        print(
            f"""Bot Reconnected:
{self.dt.hour}:{self.dt.minute:02d}:{self.dt.second:02d}
Date: {self.dt.day:02d}/{self.dt.month:02d}/{self.dt.year}
""")

    async def on_guild_join(self, ctx):
        self.update_db()
        owner = ctx.owner
        ownerembed = Embed(
            title=f"NaCl Bot | Version: {self.VERSION}",
            description=f"""Hello {owner.mention}!
I'm NaCl | A poorly coded bot with terrible support

I've just been added to your server: {ctx.name}
{ctx.system_channel.mention}


If you aren't [Salt](https://nicecock.tech/) then you probably shouldn't be seeing this message!""",

        )
        ownerembed.set_footer(text="SaltAndViChips#0001")
        await owner.send(embed=ownerembed)

    async def on_disconnect(self):

        print(
            f"""
Bot disconnected:
{self.dt.hour}:{self.dt.minute:02d}:{self.dt.second:02d}
Date: {self.dt.day:02d}/{self.dt.month:02d}/{self.dt.year}""")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            embed = Embed(
                title="Huh that's odd...",
                description="It appears an error has occurred. Sorry for any trouble!"
            )
            error_message = await args[0].send(embed=embed)
            await sleep(5)
            await error_message.delete()

        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif isinstance(exc, NotOwner):
            await ctx.send("That command is for developers only!", delete_after=8)
        elif isinstance(exc, MemberNotFound):
            await ctx.send("That user is not in this server, Command could not be completed.",
                           delete_after=8)
        elif isinstance(exc, MissingRequiredArgument):
            await ctx.send(f"You are missing a required input!\n{exc}", delete_after=8)
        elif isinstance(exc, BreakExcept):
            pass
        elif isinstance(exc, MissingPermissions):
            embed = Embed(
                title="You are missing permissions to run this command!",
                description=f"{exc}"
            )
            await ctx.send(embed=embed, delete_after=8)

        elif isinstance(exc, BotMissingPermissions):
            embed = Embed(
                title="Command Failed.",
                description=f"{exc}",
                color=0x00FA9A
            )
            await ctx.send(embed=embed, delete_after=8)
        elif isinstance(exc, BadColourArgument):
            embed = Embed(
                title="Color Input Incorrect.",
                description=f"{exc}"
            )
            embed.add_field(name="Example", value="#00FA9A")
            await ctx.send(embed=embed)
        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.scheduler.add_job(self.update_db, CronTrigger(second="0,30"))
            self.scheduler.start()
            # Example Embed

            self.update_db()
            print("Cog Setup Starting...")
            while not self.cogs_ready.all_ready():
                await sleep(0.5)
            print("\nCog Setup Complete")

            self.ready = True

            embed = Embed(
                title="NaCl Online ***\♥***",
                # description="You didn't break me",
                color=0x00FA9A,
                timestamp=datetime.utcnow()
            )

            fields = [("Version", self.VERSION, True),
                      ("Newest Update", self.UPDATE, True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_footer(text="♥")
            # embed.set_author(name="Salt And Vi Chips", icon_url=self.guild.icon)
            # embed.set_thumbnail(url=self.guild.icon_url)
            # embed.set_image(url=self.guild.icon_url)
            # await self.stdout.send(embed=embed)

            # meta = self.get_cog("Meta")
            # await meta.set()
            # await self.process_commands("moodmenu")
            # mmlocation = self.get_channel(956342454720802907)
            # mmcontext = self.get_context(mmlocation)
            # await mmcontext.invoke(mm)





        else:
            print("Bot Reconnected")

    async def on_message(self, message):
        # if self.moodsetup == False and message.channel.id==self.moodmenulocation and \
        #         message.author.bot:
        #     self.moodsetup = True
        #     await self.process_commands(message)

        if not message.author.bot:
            guild_db = f"\"{message.guild.id}\""
            server_blacklist = db.column(f"SELECT Blacklist FROM {guild_db}")
            if str(message.author.id) not in server_blacklist:
                await self.process_commands(message)


bot = Bot()
