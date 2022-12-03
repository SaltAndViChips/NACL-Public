from asyncio import run as run_async
from asyncio import sleep
from datetime import datetime
from glob import glob
from pathlib import PurePath, Path
from sys import platform

import tzlocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed
from discord import Intents
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, BotMissingPermissions, \
    MissingPermissions, BadColourArgument
from discord.errors import Forbidden
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
Server_Whitelist = [955631286263885835, 535693863696990208]

# Grab Cogs
COGPATH = Path('lib/cogs')
COGS = [path.stem.split(os.sep)[-1] for path in (COGPATH.glob('*.py'))]


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
        self.stdout = self.get_channel(600001330920292353) or self.get_channel(965478504038813796)
        self.guild = self.get_guild(535693863696990208) or self.get_guild(955631286263885835)
        pass


    def run(self, version, update):
        self.VERSION = version
        self.UPDATE = update


        print("Starting Up...")
        run_async(self.setup())
        try:
            with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
                self.TOKEN = tf.readlines(1)[0]
        except FileNotFoundError:
            self.TOKEN = os.getenv("DISCORD_TOKEN")
        super().run(self.TOKEN, reconnect=True)
        self.TOKEN = ""

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

#     async def on_guild_join(self, ctx):
#         self.update_db()
#         owner = ctx.owner
#         ownerembed = Embed(
#             title=f"NaCl Bot | Version: {self.VERSION}",
#             description=f"""Hello {owner.mention}!
# I'm NaCl | A poorly coded bot with terrible support
#
# I've just been added to your server: {ctx.name}
# {ctx.system_channel.mention}
#
#
# If you aren't [Salt](https://nicecock.tech/) then you probably shouldn't be seeing this message!""",
#
#         )
#         ownerembed.set_footer(text="SaltAndViChips#0001")
#         await owner.send(embed=ownerembed)

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
        elif isinstance(exc, Forbidden):
            await ctx.send(f"An Error has occurred:\n{exc}")
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
            self.stdout = self.stdout = self.get_channel(600001330920292353) or self.get_channel(965478504038813796)
            self.guild = self.get_guild(535693863696990208) or self.get_guild(955631286263885835)
            self.ready = True
            # self.guild = self.get_guild(535693863696990208) or self.get_guild(955631286263885835)

            embed = Embed(
                title=f"{bot.user.name} Online ***\♥***",
                # description="You didn't break me",
                color=0x00FA9A,
                timestamp=datetime.utcnow()
            )

            fields = [("Version", self.VERSION, True),
                      ("Newest Update", self.UPDATE, True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_footer(text="♥")
            embed.set_author(name="Salt And Vi Chips", icon_url=self.guild.icon.url)
            embed.set_thumbnail(url=self.guild.icon.url)
            embed.set_image(url=self.guild.icon.url)
            await self.stdout.send(embed=embed)






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
            if message.guild.id not in Server_Whitelist:
                if message.author.id in bot.owner_ids:
                    await self.process_commands(message)

            elif str(message.author.id) not in server_blacklist:
                    await self.process_commands(message)

    async def on_message_delete(self, message):
        if not message.author.bot:
            logchannel = self.get_channel(991906374537711676)

            embed = Embed(
                title="Message Deleted!",
                description = f"{message.author.mention} deleted a message in {message.channel.mention}\nMessage Content:\n\n{message.content}"
            )
            # await logchannel.send(f"Message: {message.content} was deleted by {message.author} in {message.channel.mention}")
            await logchannel.send(embed=embed)

bot = Bot()
