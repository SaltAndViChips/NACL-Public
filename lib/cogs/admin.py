from random import choice, randint
from typing import Optional
from discord import Member
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import has_permissions, bot_has_permissions, is_owner
from discord import Embed
import socket
from ..db import db


class admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="warn", hidden=False)
    @has_permissions(administrator=True)
    async def warn(self, ctx, target: Optional[Member], *, reason: Optional[str] = "No Reason Provided"):
        if target == None:
            await ctx.send("This command Warns users!")
        else:
            db.execute("UPDATE warns SET NumWarn = NumWarn+1 WHERE UserID = ?", target.id)
            db.execute("UPDATE warns SET ActiveWarns = ActiveWarns+1 WHERE UserID = ?", target.id)
            db.execute("UPDATE users SET LastWarn = CURRENT_TIMESTAMP WHERE UserID = ?", target.id)
            if db.field("SELECT WarnReason FROM warns WHERE USERID = ?", target.id) == None:
                db.execute("UPDATE warns SET WarnReason = ? WHERE UserID = ?", reason, target.id)
            else:
                db.execute("UPDATE warns SET WarnReason = WarnReason || \"|-| \" || ?  WHERE UserID = ?", reason,
                           target.id)

            if db.field("SELECT StaffID FROM warns WHERE USERID = ?", target.id) == None:
                db.execute("UPDATE warns SET StaffID = ? WHERE UserID = ?", ctx.author.id, target.id)
            else:
                db.execute("UPDATE warns SET StaffID = StaffID || \"|-| \" || ? WHERE UserID = ?", ctx.author.id,
                           target.id)

            db.commit()
            embed = Embed(
                title="User Has Been Warned",
                description=f"""{target.mention} Has Been Warned! 
                            
                            Reason: {reason}"""
            )
            await ctx.send(embed=embed)

    @command(name="history", aliases=["userhistory", "uh"], hidden=False)
    @has_permissions(administrator=True)
    async def userhistory(self, ctx, target: Optional[Member]):
        embed = Embed(
            title=f"User History",
            color=0x00FA9A,
        )
        target = target or ctx.author

        ID, Kicks, Bans, LastWarn, LastKick, LastBan = db.record(
            "SELECT UserID, NumKick, NumBan, LastWarn, LastKick, LastBan FROM users WHERE UserID = ?", target.id) or (
                                                       None, None)
        Warns, WarnReason, StaffID, ActiveWarns = db.record(
            "SELECT NumWarn, WarnReason, StaffID, ActiveWarns FROM warns WHERE UserID = ?", target.id) or (None, None)

        LastWarningReason = WarnReason.split("|-|")
        LastAdmin = StaffID.split("|-|")
        LastAdminName = await self.bot.fetch_user(LastAdmin[-1])
        fields = [("Display Name", target.display_name, True),
                  ("ID", ID, True),
                  ("Rank", target.top_role, True),
                  ("Total Warns", Warns, True),
                  ("Kicks", Kicks, True),
                  ("Bans", Bans, True),
                  ("Last Warn", LastWarn, True),
                  ("Last Kick", LastKick, True),
                  ("Last Ban", LastBan, True),
                  ("Active Warns", ActiveWarns, True),
                  ("Last Warned For", LastWarningReason[-1], True),
                  ("Last Warned By", f"<@{LastAdminName.id}>", True)]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_author(name="NaCl Bot | Staff")
        embed.set_footer(text="♥")
        await ctx.send(embed=embed)


    @command(name="blacklist", aliases=["bl"])
    @has_permissions(administrator=True)
    async def blacklist(self,ctx, target: Optional [Member], *, id: Optional[int]):
        guildDB = (f"\"{ctx.guild.id}\"")
        ServerBlacklist = db.column(f"SELECT Blacklist FROM {guildDB}")
        if target == None:
            await ctx.send("This command Blacklists users from using commands")
        elif target.id == 92276895185387520:

            if ServerBlacklist == None:
                await ctx.send("Nobody is blacklisted in this server!")
            else:
                ServerBlacklistAsMention = []
                for member in ServerBlacklist:
                    mention = (f"<@!{member}>")
                    ServerBlacklistAsMention.append(mention)
                embed = Embed(
                    title = f"Users Blacklisted in {ctx.guild.name}",
                    description = "\n".join(ServerBlacklistAsMention),
                    color = 0x00fA9A
                )
                await ctx.send(embed=embed)
        else:
            target = target or await self.bot.fetch_user(id)
            if target.id in ServerBlacklist:
                embed=Embed(
                    title="Blacklisting user...",
                    description=f"{target.mention} is already blacklisted in {ctx.guild.name}",
                    color=0x00FA9A
                )
                await ctx.send(embed=embed)

            else:
                embed = Embed(
                    title="Blacklisting user...",
                    description=f"{target.mention} has been blacklisted in {ctx.guild.name}",
                    color=0x00FA9A
                )
                await ctx.send(embed=embed)
                ServerBlacklist.append(target.id)
                db.execute(f"INSERT OR IGNORE INTO {guildDB} (Blacklist) VALUES ({target.id})")

    @command()
    @is_owner()
    async def stop_bot(self, ctx):
        stopchannel = self.bot.get_channel(965478504038813796)
        await stopchannel.send(socket.gethostname())
        exit()

    @command(name="unblacklist", aliases=["ubl"])
    @has_permissions(administrator=True)
    async def unblacklist(self, ctx, target: Optional[Member], *, id: Optional[int]):
        guildDB = (f"\"{ctx.guild.id}\"")
        ServerBlacklist = db.column(f"SELECT Blacklist FROM {guildDB}")
        if target == None:
            await ctx.send("This command Removes users from the Blacklist")
        elif target.id == 92276895185387520:
            if ServerBlacklist == None:
                await ctx.send("Nobody is blacklisted in this server!")
            else:
                ServerBlacklistAsMention = []
                for member in ServerBlacklist:
                    mention = (f"<@!{member}>")
                    ServerBlacklistAsMention.append(mention)
                embed = Embed(
                    title=f"Users Blacklisted in {ctx.guild.name}",
                    description="\n".join(ServerBlacklistAsMention),
                    color=0x00fA9A
                )
                await ctx.send(embed=embed)
        else:
            target = target or await self.bot.fetch_user(id)
            if target.id not in ServerBlacklist:
                embed = Embed(
                    title="Un-Blacklisting user...",
                    description=f"{target.mention} is not blacklisted in {ctx.guild.name}",
                    color=0x00FA9A
                )
                await ctx.send(embed=embed)
            else:
                embed = Embed(
                    title="Un-Blacklisting user...",
                    description=f"{target.mention} has been un-blacklisted in {ctx.guild.name}",
                    color=0x00FA9A
                )
                await ctx.send(embed=embed)
                db.execute(f"DELETE FROM {guildDB} WHERE blacklist = {target.id}")



                #
            # if db.field("SELECT StaffID FROM warns WHERE USERID = ?", target.id) == None:
            #     db.execute("UPDATE warns SET StaffID = ? WHERE UserID = ?", ctx.author.id, target.id)
            # else:
            #     db.execute("UPDATE warns SET StaffID = StaffID || \"|-| \" || ? WHERE UserID = ?", ctx.author.id,
            #                target.id)

    @command(name="clear", aliases=["purge"])
    @bot_has_permissions(manage_messages=True)
    @has_permissions (manage_messages=True)
    async def clear_messages(self, ctx, limit: Optional[int] = 10):
        if 0 < limit <= 100:
            async with ctx.channel.typing():
                await ctx.message.delete()
                deleted = await ctx.channel.purge(limit=limit)

                await ctx.send(f"Deleted {len(deleted):,} messages!", delete_after=5)

     # make sure no one else uses it



    # @command(name="command", aliases=["cmd", "c"], hidden=True)
    # async def command(self, ctx):
    #     pass
    # @command(name="DB", aliases=["RDB"], hidden = True)
    # async def RebuildDB(self,ctx):
    #     if ctx.author.id == 92276895185387520:
    #         db.execute("ALTER TABLE users DROP ActiveWarns")
    #
    #         db.execute("ALTER TABLE warns ADD COLUMN ActiveWarns integer DEFAULT 0")
    #         # db.commit()
    #         print("DB Updated")

    # else:
    #     await ctx.send("Sorry! This Command is only for Developers!")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("admin")


    # @Cog.listener()


async def setup(bot):
    await bot.add_cog(admin(bot))
