import discord.ext.commands.errors
from discord.ext.commands import Cog
from random import choice
from typing import Optional
from discord.ext.commands import command, group
from discord import Member
from discord import Embed
from validators import url as urlcheck
from discord.ext.commands import is_owner as devonly
from discord.ext.commands import has_permissions, bot_has_permissions
from pathlib import Path
import os

class harassment(Cog):
    def __init__(self, bot):
        self.bot = bot


    @command (name="avatar", aliases=["Avatar","pfp","PFP","DA"])
    async def pfp(self, ctx, *, member: Member = None):
        if not member:
            member = ctx.author
        memberpfp = member.default_avatar.url
        await ctx.send(f"{memberpfp}")

    @command (name="serveravatar", aliases=["ServerAvatar","spfp","SPFP","SA"])
    async def displaypfp(self, ctx, *, member: Member = None):
        if not member:
            member = ctx.author
        memberpfp = member.display_avatar.url
        await ctx.send(f"{memberpfp}")


    @command(name="angel", aliases=["angle", "retard", "dumbass"])
    async def angle(self, ctx):
        user = await self.bot.fetch_user(689989339698036762)
        embed = Embed(
            title=f"Identifying Idiocy...",
            description=f"Peak Idiocy Detected\n ID: <@{user.id}>",

            color=0x00FA9A,
        )
        await ctx.send(embed=embed)

    @command(name="allie", aliases=["loser", "Allie"], hidden=True)
    async def say_allie(self, ctx):
        embed = Embed(
            title=f"Allie is a loser",
            description=f"<@163119630368374785> is a loser.\nand she smells.",
            color=0x00FA9A,
        )
        await ctx.send(embed=embed)

    @command(name="bruh")
    async def bruh(self, ctx):
        await ctx.send('bruh')

    # @command(name="daddy", hidden=True)
    # async def daddy(self, ctx):
    #     embed = Embed(
    #         title="Who's a Good Boy?",
    #         description=f"{ctx.author.mention} is a good boy!"
    #     )
    #
    #     embed.set_thumbnail(url=f"{ctx.author.avatar_url}")
    #     await ctx.send(embed=embed)

    # @command(name="addtobreed", aliases=["addbreed", "ab", "atb", "a2b"], hidden=True)
    # @devonly()
    # async def addtobreed(self, ctx, userimage):
    #     if urlcheck(userimage) == True:
    #         with open("./lib/items/breeding.txt", "a+", encoding="utf-8") as rl:
    #             rl.seek(0)
    #             data = rl.read(100)
    #             if len(data) > 0:
    #                 rl.write("\n")
    #             rl.write(f"{userimage}")
    #         embed = Embed(
    #             title="Adding new image!",
    #             description=f"I have added {userimage} to my list of pictures!"
    #         )
    #         embed.set_image(url=f"{userimage}")
    #         await ctx.send(embed=embed)
    #     else:
    #         await ctx.send("Please use a valid URL!")
    #
    # @command(name="addtospank", aliases=["addspank", "as", "ats", "a2s"], hidden=True)
    # @devonly()
    # async def addtospank(self, ctx, userimage):
    #     if urlcheck(userimage) == True:
    #         with open("./lib/items/spanking.txt", "a+", encoding="utf-8") as rl:
    #             rl.seek(0)
    #             data = rl.read(100)
    #             if len(data) > 0:
    #                 rl.write("\n")
    #             rl.write(f"{userimage}")
    #         embed = Embed(
    #             title="Adding new image!",
    #             description=f"I have added {userimage} to my list of pictures!"
    #         )
    #         embed.set_image(url=f"{userimage}")
    #         await ctx.send(embed=embed)
    #     else:
    #         await ctx.send("Please use a valid URL!")
    #
    # @command(name="addtochoke", aliases=["addchoke", "ac", "atc", "a2c"], hidden=True)
    # @devonly()
    # async def addtochoke(self, ctx, userimage):
    #     if urlcheck(userimage) == True:
    #         with open("./lib/items/choking.txt", "a+", encoding="utf-8") as rl:
    #             rl.seek(0)
    #             data = rl.read(100)
    #             if len(data) > 0:
    #                 rl.write("\n")
    #             rl.write(f"{userimage}")
    #         embed = Embed(
    #             title="Adding new image!",
    #             description=f"I have added {userimage} to my list of pictures!"
    #         )
    #         embed.set_image(url=f"{userimage}")
    #         await ctx.send(embed=embed)
    #     else:
    #         await ctx.send("Please use a valid URL!")
    @group(passcontext=True)
    async def sir(self, ctx, member: Optional[Member], amount: Optional[int]):
        if ctx.invoked_subcommand is None:
            await ctx.send("You need to select an action!")

    async def sirembed(self, ctx, action, images, member: Optional[Member], amount: Optional[int], title):


        if member is None:
            if action == "spit":
                embed = Embed(
                    title=f"{title}",
                    description=f"Someone {action} on {ctx.author.mention}",
                    color=0xFF5682
                )
            else:
                embed = Embed(
                    title=f"{title}",
                    description=f"Someone {action} {ctx.author.mention}",
                    color=0xFF5682
                )
            randomimage = choice(images)
            print("Sending " + randomimage)
            embed.set_image(url=f"{randomimage}")
            embed.set_footer(text="♥")
        elif member is not None:
            if amount is None:

                if action == "spit" and member.id == 92276895185387520:
                    embed = Embed(
                        title=f"{title}",
                        description=f"{member.mention} {action}s on {ctx.author.mention}",
                        color=0xFF5682
                    )

                elif action == "spit":
                    embed = Embed(
                        title=f"{title}",
                        description=f"{ctx.author.mention} {action}s on {member.mention}",
                        color=0xFF5682
                    )

                elif member.id == 92276895185387520:
                    embed = Embed(
                        title=f"{title}",
                        description=f"{member.mention} {action}s {ctx.author.mention}",
                        color=0xFF5682
                    )
                else:
                    embed = Embed(
                        title=f"{title}",
                        description=f"{ctx.author.mention} {action}s {member.mention}",
                        color=0xFF5682
                    )
            if amount is not None:
                if action == "spit" and member.id == 92276895185387520:
                    embed = Embed(
                        title=f"{title}",
                        description=f"{member.mention} {action}s on {ctx.author.mention} {amount} times!",
                        color=0xFF5682
                    )

                elif action == "spit":
                    embed = Embed(
                        title=f"{title}",
                        description=f"{ctx.author.mention} {action}s on {ctx.author.mention} {amount} times!",
                        color=0xFF5682
                    )

                elif member.id == 92276895185387520:
                    embed = Embed(
                        title=f"{title}",
                        description=f"{member.mention} {action}s {ctx.author.mention} {amount} times!",
                        color=0xFF5682
                    )
                else:
                    embed = Embed(
                        title=f"{title}",
                        description=f"{ctx.author.mention} {action}s {member.mention} {amount} times!",
                        color=0xFF5682
                    )

            randomimage = choice(images)
            embed.set_image(url=f"{randomimage}")
            embed.set_footer(text="♥")
        return embed, randomimage


    @sir.command(name="breed", aliases=["breedme", "breedpls", "breedplz", "breedmenow", "plingz1"], hidden=True)
    async def breed(self, ctx, member: Optional[Member], amount: Optional[int]):
        with open("./lib/items/breeding.txt", "r", encoding="utf-8") as rl:
            images = []
            for line in rl:
                images.append(line)
                # ctx, action, images, member: Optional[Member], amount: Optional[int], title
        action = "breed"
        title = "Breeding Time!"
        embed = await self.sirembed(ctx, action, images, member, amount, title)
        randomimage = embed[1]
        embed=embed[0]
        if embed is None:
            pass
        else:
            msg = await ctx.send(embed=embed)
            # await ctx.send("just testing")
        # if member is None:
        #     embed = Embed(
        #         title="Say Please",
        #         description=f"{ctx.author.mention} Wants to be bred",
        #         color=0xFF5682
        #     )
        #     randomimage = choice(breedimages)
        #     print("Sending " + randomimage)
        #     embed.set_image(url=f"{randomimage}")
        #     embed.set_footer(text="♥")
        #     await ctx.send(embed=embed)
        # elif member is not None:
        #     if member.id == 92276895185387520:
        #         embed = Embed(
        #             title="Say Please",
        #             description=f"{member.mention} breeds {ctx.author.mention}",
        #             color=0xFF5682
        #         )
        #     else:
        #         embed = Embed(
        #             title="Say Please",
        #             description=f"{ctx.author.mention} breeds {member.mention}",
        #             color=0xFF5682
        #         )
        #     randomimage = choice(breedimages)
        #     print("Sending " + randomimage)
        #     embed.set_image(url=f"{randomimage}")
        #     embed.set_footer(text="♥")
        #     await ctx.send(embed=embed)

    @sir.command(name="spank", aliases=["spankme", "spankpls", "spankplz", "spankmenow", "plingz2"], hidden=True)
    async def spank(self, ctx, member: Optional[Member], amount: Optional[int]):
        with open("./lib/items/spanking.txt", "r", encoding="utf-8") as rl:
            images = []
            for line in rl:
                images.append(line)
                # ctx, action, images, member: Optional[Member], amount: Optional[int], title
        action = "spank"
        title = "You've been Naughty!"
        embed = await self.sirembed(ctx, action, images, member, amount, title)
        randomimage = embed[1]
        embed = embed[0]
        if embed is None:

            pass
        else:
            await ctx.send(embed=embed)

    @sir.command(name="add", hidden=True)
    @has_permissions(administrator=True)
    async def addimage(self, ctx, file: Optional[str], *, NewLine: Optional[str]):
        ImagePath = Path('lib/items')
        Files = [path.stem.split(os.sep)[-1] for path in (ImagePath.glob('*.txt'))]
        if file == None:
            embed = Embed(
                title = "Files!",
                description = "You can add to the following files!"
            )
            WritableFiles = []
            for tempfile in Files:
                if tempfile.endswith("ing"):
                    WritableFiles.append(tempfile)
            embed.add_field(name="Files", value="\n".join(WritableFiles))
            msg = await ctx.send(embed=embed)
            if any ([hasattr(embed.image, "url") for embed in msg.embeds]):
                for embed in msg.embeds:
                    if embed.image.url != None:
                        print (embed.image.url)

        elif file in Files:
            filepath = Path(f'lib/items/{file}.txt')
            if NewLine is None:
                if len(ctx.message.attachments) > 0:
                    if any ([hasattr(attachment, "width") for attachment in ctx.message.attachments]):
                        for attachment in ctx.message.attachments:
                            if hasattr(attachment, "width"):
                                if NewLine is None:
                                    NewLine = attachment.url
                                else:
                                    NewLine += f"\n{attachment.url}"
                        with open(filepath, "a+", encoding="utf-8") as tf:
                            tf.seek(0)
                            data = tf.read(100)
                            if len(data) > 0:
                                tf.write("\n")
                            tf.write(NewLine)
                        await ctx.send(f"Added New Line:\n\n{NewLine}\n\nto the file!")
                    else:
                        await ctx.send("You must attach a valid Image file!", delete_after=5)

                else:
                    with open(filepath, "rb") as filetosend:
                        await ctx.send(file=discord.File(filetosend, f"{file}.txt"))
            else:
                with open(filepath, "a+", encoding="utf-8") as tf:
                    tf.seek(0)
                    data = tf.read(100)
                    if len(data) > 0:
                        tf.write("\n")
                    tf.write(NewLine)
                await ctx.send(f"Added New Line:\n\n{NewLine}\n\nto the file!")

        else:
            await ctx.send("Invalid File Name!")
        await ctx.message.delete()

    @sir.command(name="choke", aliases=["chokeme", "chokepls", "chokeplz", "chokemenow", "plingz3"], hidden=True)
    async def choke(self, ctx, member: Optional[Member], amount: Optional[int]):
        with open("./lib/items/choking.txt", "r", encoding="utf-8") as rl:
            images = []
            for line in rl:
                images.append(line)
                # ctx, action, images, member: Optional[Member], amount: Optional[int], title
        action = "choke"
        title = "Naughty Naughty"
        embed = await self.sirembed(ctx, action, images, member, amount, title)
        randomimage = embed[1]
        embed = embed[0]
        if embed is None:
            pass
        else:
            await ctx.send(embed=embed)

    @sir.command(name="kiss", aliases=["kissme", "kisspls", "kissplz", "kissmenow"],
                 hidden=True)
    async def kiss(self, ctx, member: Optional[Member], amount: Optional[int]):
        with open("./lib/items/kissing.txt", "r", encoding="utf-8") as rl:
            images = []
            for line in rl:
                images.append(line)
                # ctx, action, images, member: Optional[Member], amount: Optional[int], title
        action = "kiss"
        title = "Good Girl"
        embed = await self.sirembed(ctx, action, images, member, amount, title)
        randomimage = embed[1]
        embed = embed[0]
        if embed is None:
            pass
        else:
            msg = await ctx.send(embed=embed)
            if any ([hasattr(embed.image, "url") for embed in msg.embeds]):
                for embed in msg.embeds:
                    if embed.image.url == None:
                        print (randomimage)

    @sir.command(name="hug", aliases=["hugme", "hugpls", "hugplz", "hugmenow", "plingz"], hidden=False)
    async def hug(self, ctx, member: Optional[Member], amount: Optional[int]):
        with open("./lib/items/hugging.txt", "r", encoding="utf-8") as rl:
            images = []
            for line in rl:
                images.append(line)
                # ctx, action, images, member: Optional[Member], amount: Optional[int], title
        action = "hug"
        title = "♥ ♥ ♥ ♥ ♥"
        embed = await self.sirembed(ctx, action, images, member, amount, title)
        if embed is None:
            pass
        else:
            await ctx.send(embed=embed)

    @sir.command(name="pet", aliases=["petme", "petpls", "petplz", "petmenow", "plingz5", "patme", "patpls", "patplz", "patmenow", "pat"], hidden=False)
    async def pet(self, ctx, member: Optional[Member], amount: Optional[int]):
        with open("./lib/items/petting.txt", "r", encoding="utf-8") as rl:
            images = []
            for line in rl:
                images.append(line)
                # ctx, action, images, member: Optional[Member], amount: Optional[int], title
        action = "pet"
        title = "Good Pet!"
        embed = await self.sirembed(ctx, action, images, member, amount, title)
        if embed == None:
            pass
        else:
            await ctx.send(embed=embed)

    @sir.command(name="cuddle", aliases=["cuddleme", "cuddlepls", "cuddleplz", "cuddlemenow", "plingz6"], hidden=False)
    async def cuddle(self, ctx, member: Optional[Member], amount: Optional[int]):
        with open("./lib/items/cuddling.txt", "r", encoding="utf-8") as rl:
            images = []
            for line in rl:
                images.append(line)
                # ctx, action, images, member: Optional[Member], amount: Optional[int], title
        action = "cuddle"
        title = "Snuggle up!"
        embed = await self.sirembed(ctx, action, images, member, amount, title)
        if embed is None:
            pass
        else:
            await ctx.send(embed=embed)

    @sir.command(name="spit", aliases=["spitme", "spitpls", "spitplz", "spitmenow", "plingz7"], hidden=True)
    async def spit(self, ctx, member: Optional[Member], amount: Optional[int]):
        with open("./lib/items/spitting.txt", "r", encoding="utf-8") as rl:
            images = []
            for line in rl:
                images.append(line)
                # ctx, action, images, member: Optional[Member], amount: Optional[int], title
        action = "spit"
        title = "Time for a reward!"
        embed = await self.sirembed(ctx, action, images, member, amount, title)
        if embed is None:
            pass
        else:
            await ctx.send(embed=embed)

    @command(name="meth", hidden=True)
    async def meth(self, ctx):
        embed=Embed(
            title="No.",
            description="Not even a little.",
            color = 0x00fA9A
        )
        methage = await ctx.send(embed=embed)
        await ctx.message.delete(delay=5)
        await methage.delete(delay=5)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("harassment")

async def setup(bot):
    await bot.add_cog(harassment(bot))