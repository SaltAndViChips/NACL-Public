import discord
from discord import Embed, Member
from discord.ext.commands import Cog
from discord.ext.commands import command, has_permissions
from discord.ext.commands import is_owner as devonly
from typing import Optional
from discord.utils import get
from discord.ui import Button, View
from contextlib import suppress

from ..db import db
from ..imports import search
import asyncio


class MoodRolesMenu(discord.ui.Select):


    def __init__(self, bot):
        self.bot = bot
        self.saferoles = [957529066632794222, 960000648785588254]
        GGServer = bot.get_guild(955631286263885835).roles
        roleList = []
        for role in GGServer:
            if role.id == 957128314055716894:
                RoleCap = role.position
            elif role.id == 957128447065477130:
                MoodCap = role.position
            elif role.id == 955635233548541982:
                BotPosition = role.position
        for role in GGServer:
            if role.position < BotPosition and RoleCap < role.position < MoodCap and role.id not in self.saferoles:
                roleList.append(role.name)
        # roleList = [('Bratty'), ('Happy', '😊'), ('Needy', '🥰'), ('Non-Verbal', '😶'),
        #             ('Neutral', '😑'), ('Upset', '😓'), ('Sad', '😭'), ('Vibin\'', '🔊'),
        #             ('Not Vibin\'', '🔈'), ('Tired', '😴')]
        options = []
        for Role in sorted(roleList):
            options.append(
                discord.SelectOption(label=f'{Role}', description=f'I am {Role}'))

        # Set the options that will be presented inside the dropdown
        # options = [
        #     discord.SelectOption(label='Bratty', description='I am Bratty',
        #                          emoji='😤'),
        #     discord.SelectOption(label='Happy', description='I am Happy',
        #                          emoji='😊'),
        #     discord.SelectOption(label='Needy', description='I am Needy',
        #                          emoji='🥰'),
        #     discord.SelectOption(label='Non-Verbal', description='I am Non-Verbal',
        #                          emoji='😶'),
        #     discord.SelectOption(label='Neutral', description='I am Neutral',
        #                          emoji='😑'),
        #     discord.SelectOption(label='Upset', description='I am Upset',
        #                          emoji='😓'),
        #     discord.SelectOption(label='Sad', description='I am Sad',
        #                          emoji='😭'),
        #     discord.SelectOption(label='Vibin\'', description='I am Vibin\'',
        #                          emoji='🔊'),
        #     discord.SelectOption(label='Not Vibin\'', description='I am not Vibin\'',
        #                          emoji='🔈')
        # ]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder='How are you feeling?', min_values=1, max_values=1,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        # await interaction.response.send_message(embed=embed)
        AllRoles = []

        KeptMood = db.field("SELECT FirstMood from moods WHERE UserID = ?", interaction.user.id) or "Neutral"
        db.execute("UPDATE moods SET SecondMood = ? WHERE UserID = ?", KeptMood, interaction.user.id)
        for role in interaction.guild.roles:
            AllRoles.append(role)
        userRoleList = []
        for role in interaction.user.roles:
            userRoleList.append(role)
        botposition = get(interaction.guild.roles, id=955635233548541982).position
        roleCap = get(interaction.guild.roles, id=957128314055716894).position
        moodCap = get(interaction.guild.roles, id=957128447065477130).position
        for role in AllRoles:

            if role.position < botposition and moodCap > role.position > roleCap and role.id not in self.saferoles and role.name != KeptMood:
                if role in userRoleList:
                    await interaction.user.remove_roles(role)

        newRole = None
        for role in AllRoles:
            if self.values[0] == role.name:
                newRole = role
        if newRole not in AllRoles:
            newRole = await interaction.guild.create_role(name=self.values[0], color=0x00FA9A)
        await newRole.edit(position=moodCap-1)

        if newRole is not None:
            await interaction.user.add_roles(newRole)
            embed = Embed(
                title="Changing Mood...",
                description=f"You're feeling {newRole.mention}",
                color=newRole.color
            )
            Salt = await self.bot.fetch_user(92276895185387520)
            dmEmbed = Embed(
                title="Mood Changed!",
                description=f"{interaction.user.mention} has changed their mood to {newRole.name}",
                color=newRole.color
            )
            # await Salt.send(embed=dmEmbed)
            LogChannel = await self.bot.fetch_channel(959626235229667438)
            dmEmbed = Embed(
                title="Mood Changed!",
                description=f"{interaction.user.mention} has changed their mood to {newRole.mention}",
                color=newRole.color
            )
            db.execute("UPDATE moods SET FirstMood = ? WHERE UserID = ?", newRole.name,
                       interaction.user.id)
            await LogChannel.send(embed=dmEmbed)
            await interaction.response.send_message(embed=embed, ephemeral=True)


class RolesMenu(discord.ui.Select):
    def __init__(self, bot):
        self.saferoles = [957529066632794222, 960000648785588254]
        self.bot = bot

        GGServer = bot.get_guild(955631286263885835).roles
        roleList = []
        for role in GGServer:
            if role.id == 957128314055716894:
                RoleCap = role.position
            elif role.id == 955635233548541982:
                BotPosition = role.position
        for role in GGServer:
            if role.position < BotPosition and RoleCap > role.position > 0 and role.id not in self.saferoles:
                roleList.append(role.name)

        options = []
        for Role in sorted(roleList):
            options.append(discord.SelectOption(label=f'{Role}', description=f'I\'m (a) {Role}'))

        super().__init__(placeholder='What role would you like princess?', min_values=1,
                         max_values=1,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        # await interaction.response.send_message(embed=embed)
        AllRoles = []
        KeptMood = db.field("SELECT FirstRole from moods WHERE UserID = ?",
                            interaction.user.id) or "Neutral"
        db.execute("UPDATE moods SET SecondRole = ? WHERE UserID = ?", KeptMood,
                   interaction.user.id)

        for role in interaction.guild.roles:
            AllRoles.append(role)
        userRoleList = []
        for role in interaction.user.roles:
            userRoleList.append(role)
        botPosition = get(interaction.guild.roles, id=955635233548541982).position
        roleCap = get(interaction.guild.roles, id=957128314055716894).position
        for role in AllRoles:
            if role.position < botPosition and roleCap > role.position > 0 and role.id not in self.saferoles and role.name != KeptMood:
                if role in userRoleList:
                    await interaction.user.remove_roles(role)

        NewRole = None
        for role in AllRoles:
            if self.values[0] == role.name:
                NewRole = role
        if NewRole != None:
            await interaction.user.add_roles(NewRole)
            embed = Embed(
                title="Changing Role...",
                description=f"Your new role is {NewRole.mention}",
                color=NewRole.color
            )
            Salt = await self.bot.fetch_user(92276895185387520)
            dmEmbed = Embed(
                title="Role Changed!",
                description=f"{interaction.user.mention} has changed their Role to {NewRole.mention}",
                color=NewRole.color
            )
            # await Salt.send(embed=dmEmbed)
            db.execute("UPDATE moods SET FirstRole = ? WHERE UserID = ?", NewRole.name,
                       interaction.user.id)
            LogChannel = await self.bot.fetch_channel(959626235229667438)
            await LogChannel.send(embed=dmEmbed)
            await interaction.response.send_message(embed=embed, ephemeral=True)


# class Confirm(View):
#     def __init__(self, bot):
#         super().__init__()
#         self.value = None
#
#     @Button(emoji="✔", style=discord.ButtonStyle.green)
#     async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
#         self.value = True
#
#     @Button(emoji="❌", style=discord.ButtonStyle.grey)
#     async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
#         self.value = False
#         await self.stop()

class MoodDropDownView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(MoodRolesMenu(self.bot))


class RoleDropDownView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()

        self.add_item(RolesMenu(self.bot))


# class requestRole(discord.ui.Button):
#     def __init__(self):
#         Button=discord.ui.Button
#         AcceptButton = Button(emoji="👍", style=discord.ButtonStyle.green)
#         DeclineButton = Button(emoji="👎", style=discord.ButtonStyle.red)
#         self
#     async def callback(self,  interaction: discord.Interaction):
#
#
# class requestRoleView(discord.ui.view):
#     def __init__(self, bot):
#         self.bot=bot
#         super().__init__()
#
#         self.add_item(requestRole(self.bot))


class misc(Cog):
    def __init__(self, bot):
        self.bot = bot

    # @command(name="rolerequest", aliases=["rr", "request"])
    # async def rolerequest(self, ctx):
    #     fields = []
    #     Running = True
    #     await ctx.message.delete()
    #     def add_fields(fields, embed):
    #         for field in fields:
    #             embed.add_field(name=field[0], value=field[1])
    #
    #
    #     def MakeEmbed(TempDescription, color=0x00FA9A):
    #         embed = Embed(
    #             title="Role Request!",
    #             description=TempDescription,
    #             color=color
    #         )
    #         return embed
    #
    #     fields = []
    #     global RoleType
    #     RoleType = ""
    #     global roleAccepted
    #     roleAccepted = None
    #
    #     embed = MakeEmbed(f"Hello {ctx.author.mention}\n"
    #                       f"What is the name of the role you would like to request?")
    #     AcceptButton = Button(emoji="👍", style=discord.ButtonStyle.green)
    #     DeclineButton = Button(emoji="👎", style=discord.ButtonStyle.red)
    #     MoodButton = Button(label="Mood", style=discord.ButtonStyle.green)
    #     RoleButton = Button(label="Role", style=discord.ButtonStyle.red)
    #
    #     async def accept_callback(interaction):
    #         global roleAccepted
    #         roleAccepted = True
    #         response = await interaction.response.send_message(f"{RoleName} Accepted", ephemeral=True)
    #
    #     async def decline_callback(interaction):
    #         global roleAccepted
    #         roleAccepted = False
    #         response = await interaction.response.send_message(f"{RoleName} Denied", ephemeral=True)
    #
    #     async def mood_callback(interaction):
    #         global RoleType
    #         RoleType = "Mood"
    #         embed = MakeEmbed(f"Requesting Mood {RoleName}!\n\n"
    #                           f"Role Color #{RoleColorContent}!\n", RoleColor)
    #         await interaction.response.send_message(embed=embed, ephemeral=True)
    #
    #     async def role_callback(interaction):
    #         global RoleType
    #         RoleType = "Role"
    #         embed = MakeEmbed(f"Requesting Role {RoleName}!\n\n"
    #                           f"Role Color #{RoleColorContent}!\n", RoleColor)
    #         await interaction.response.send_message(embed=embed, ephemeral=True)
    #     view = View()
    #
    #     msg = await ctx.send(embed=embed)
    #
    #     MoodButton.callback = mood_callback
    #
    #     RoleButton.callback = role_callback
    #
    #     AcceptButton.callback = accept_callback
    #
    #     DeclineButton.callback = decline_callback
    #
    #     await msg.edit(view=view)
    #
    #     def check(message):
    #         return message.channel.id == ctx.channel.id
    #
    #     RoleNameMsg = await self.bot.wait_for('message', check=check)
    #     RoleName = RoleNameMsg.content
    #     fields.append(("Role Name", f"{RoleName}"))
    #     await RoleNameMsg.delete()
    #
    #     embed = MakeEmbed(f"Good Job!\n"
    #                       f"What is the Color of the role you would like to request?\n\n"
    #                       f"Please use a valid Hex ID (Example: 00FA9A)")
    #     add_fields(fields, embed)
    #     await msg.edit(embed=embed)
    #     RoleColorMsg = await self.bot.wait_for('message', check=check)
    #     RoleColorContent = RoleColorMsg.content
    #     try:
    #         RoleColor = eval(f"0x{RoleColorMsg.content}")
    #         RoleColorContent = RoleColorMsg.content
    #     except SyntaxError:
    #         RoleColor = 0x00FA9A
    #         RoleColorContent = "00FA9A"
    #         await ctx.send("You entered an Invalid Color Code, color set to default!",
    #                        delete_after=5)
    #
    #     await RoleColorMsg.delete()
    #
    #     embed = MakeEmbed(f"Very Good Girl!\n\n"
    #                       f"Last thing:\n\n"
    #                       f"Is this a Mood, or a Role?", RoleColor)
    #     add_fields(fields, embed)
    #     view.add_item(MoodButton)
    #     view.add_item(RoleButton)
    #     await msg.edit(embed=embed, view=view)
    #     await self.bot.wait_for('interaction', check=check)
    #     await msg.delete()
    #     requestEmbed = Embed(
    #         title="New Role Requested!",
    #         description=f"{ctx.author.mention} has requested a {RoleType} called {RoleName}\n",
    #         color=RoleColor
    #
    #     )
    #     requestview = View()
    #     requestview.add_item(AcceptButton)
    #     requestview.add_item(DeclineButton)
    #     requestchannel = self.bot.get_channel(963237913888423946)
    #     requestmsg = await requestchannel.send(embed=requestEmbed, view=requestview)
    #
    #     async def check2(interaction):
    #         return interaction.author.id == 92276895185387520 and interaction.message.id == requestmsg.id
    #
    #     await self.bot.wait_for('interaction', check=check2)
    #     roleCap = get(ctx.guild.roles, id=957128314055716894).position
    #     moodCap = get(ctx.guild.roles, id=957128447065477130).position
    #     requestview.clear_items()
    #     if roleAccepted == True:
    #         requestEmbed.add_field(name="Status", value="Accepted!")
    #         await requestmsg.edit(embed=requestEmbed, view=requestview)
    #         newRole = await ctx.guild.create_role(name=RoleName, color=RoleColor)
    #         if RoleType == "Mood":
    #             await newRole.edit(position=moodCap-1)
    #         else:
    #             await newRole.edit(position=roleCap-1)
    #         PMEmbed = Embed(
    #             title="Role Request",
    #             description=f"Your {RoleType}: {RoleName} has been Accepted!\nYay!",
    #             color=RoleColor
    #         )
    #         await ctx.author.send(embed=PMEmbed)
    #
    #
    #
    #
    #     else:
    #         requestEmbed.add_field(name="Status", value="Denied!")
    #         await requestmsg.edit(embed=requestEmbed, view=requestview)
    #         PMEmbed = Embed(
    #             title="Role Request",
    #             description=f"Your {RoleType}: {RoleName} has been denied!",
    #             color=RoleColor
    #         )
    #         await ctx.author.send(embed=PMEmbed)

        # requestEmbed = Embed(
        #     title="New Role Requested!",
        #     description=f"{interaction.user.mention} has requested a new role!"
        # )
        # requestEmbed.add_field(name="Role Name", value=f"{}")

    @command(name="moodmenu", aliases=["mm", "mood", "rm", "rolemenu"])
    async def moodmenu(self, ctx):
        """Sends a message with our dropdown containing colours"""
        if ctx.channel.id == 956342454720802907:
            moodview = MoodDropDownView(self.bot)
            roleview = RoleDropDownView(self.bot)
            # Sending a message containing our view
            if ctx.message != None:
                await ctx.message.delete()
            async with ctx.channel.typing():
                deleted = await ctx.channel.purge(limit=100)
            await ctx.send("How are you feeling princess?", view=moodview)
            await ctx.send("Just picking a role?", view=roleview)

    @command(name="prefix")
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        if new == "current":
            currentprefix = db.field("SELECT Prefix from guilds WHERE GuildID = ?", ctx.guild.id)
            await ctx.send(currentprefix)
        elif len(new) > 3:
            await ctx.send(
                f"The prefix {new} cannot be accepted. Please make a prefix with 3 or less characters!")
        else:
            db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
            db.commit()

            embed = Embed(
                title="Successfully Updated Prefix!",
                description=f"The Prefix has been updated to \"**{new}**\"",
                color=0x00FA9A,
            )
            await ctx.send(embed=embed)

    # @command(name="moodmenu")
    # async def moodmenu(self,ctx):
    #     await ctx.send("Welcome to the mood Menu!",
    #                    components=
    #                    [Select(placeholder="How are you feeling Princess?",
    #                        options=[
    #                            SelectOption(
    #                            label="Happy!",
    #                            value="956104410046529546",
    #                            description="I am feeling Happy!",
    #                            emoji="😊"
    #                         ),
    #                         SelectOption(
    #                            label="Bratty!",
    #                            value="956104326026264577",
    #                            description="I am feeling Bratty!",
    #                            emoji="😤"
    #                         ),
    #                         SelectOption(
    #                            label="Neutral!",
    #                            value="956106547820371989",
    #                            description="I am feeling Neutral!",
    #                            emoji="😑"
    #                         ),
    #                         SelectOption(
    #                            label="Upset!",
    #                            value="956105526645780490",
    #                            description="I am feeling Upset!",
    #                            emoji="😓"
    #                         ),
    #                         SelectOption(
    #                            label="Sad!",
    #                            value="956106199269531658",
    #                            description="I am feeling Sad!",
    #                            emoji="😭"
    #                         ),
    #                         SelectOption(
    #                            label="Needy!",
    #                            value="956105126337191936",
    #                            description="I am feeling Needy!",
    #                            emoji="🥰"
    #                         ),
    #                         SelectOption(
    #                            label="Non-Verbal!",
    #                            value="956108017219297340",
    #                            description="I am feeling Non-Verbal!",
    #                            emoji="😶"
    #                         ),
    #
    #                        ])])
    #     while True:
    #         try:
    #             event = await self.bot.wait_for("select_option", check=None)
    #
    #             label = event.component[0].label
    #
    #             roleid=int(label.value)
    #             await ctx.send(roleid)
    #
    #             newrole=get(ctx.guild.roles, id=roleid)
    #             response=Embed(
    #                 title="Changed mood",
    #                 description=f"Your mood has been updated to {newrole.name}"
    #             )
    #             await event.respond(
    #                 type=4,
    #                 ephemeral=True,
    #                 embed=response
    #             )
    #         except discord.NotFound:
    #             print("Error")

    @command(name="guilds")
    @devonly()
    async def guildlist(self, ctx):
        list_of_guilds = []
        for guild in self.bot.guilds:
            list_of_guilds.append(f"{guild.name}\nID: {guild.id}\n")
        embed = Embed(
            color=0x694201,
            title="What Guilds am I in?",
            description="\n".join(list_of_guilds)
        )
        await ctx.send(embed=embed)
        # db.multiexec("SELECT GuildID from guilds",((guild.id,) for guild in self.guilds)

    @command(name="invite")
    async def invite(self, ctx):
        embed = Embed(
            title="You want to invite me?",
            description="Click [here](https://discord.com/api/oauth2/authorize?client_id=837121872171630602&permissions=0&scope=bot)"
        )
        await ctx.send(embed=embed)

    @command(name="join")
    async def join_channel(self, ctx):
        channel = ctx.author.voice.channel
        await channel.connect()

    @command(name="leave")
    async def leave_channel(self, ctx):
        await ctx.voice_client.disconnect()

    @command(name="leaveguild", aliases=["lg", "leave"])
    @devonly()
    async def leave_guild_command(self, ctx, *, guild_name):
        list_of_guilds = []
        list_of_guild_ids = []
        for guilds in self.bot.guilds:
            list_of_guilds.append(f"{guilds.name}")
            list_of_guild_ids.append(f"{guilds.id}")
        if guild_name in list_of_guilds or guild_name in list_of_guild_ids:
            if guild_name in list_of_guilds:
                guild = get(self.bot.guilds, name=guild_name)
            elif guild_name.isnumeric() == True:
                guild = get(self.bot.guilds, id=int(guild_name))
            else:
                guild = get(self.bot.guilds, name=guild_name)
            embed = Embed(
                title="Leaving Server...",
                description=f"Server Left Successfully!\n\n\n I have left {guild.name}\n\n (Server ID:{guild.id})",
                color=0x420691
            )
            embed.set_thumbnail(url=f"{guild.icon_url}")
            await ctx.send(embed=embed)
            await guild.leave()
        else:
            if guild_name.isnumeric() == True:
                embed = Embed(
                    title="An Error has occured!",
                    description=f"I am not in a guild with the ID:\n{guild_name}",
                    color=0x00FA9A
                )
                await ctx.send(embed=embed)
            else:
                embed = Embed(
                    title="An Error has occured!",
                    description=f"I am not in a guild named:\n{guild_name}",
                    color=0x00FA9A
                )
                await ctx.send(embed=embed)

    @command(name="leaveguildid", aliases=("lgid", "leaveid"))
    async def leave_guild_command(self, ctx, *, guild_name):
        list_of_guild_ids = []
        for guilds in self.bot.guilds:

            list_of_guild_ids.append(f"{guilds.id}")
            if guild_name in list_of_guild_ids:
                guild = get(self.bot.guilds, id=int(guild_name))
                embed = Embed(
                    title="Leaving Server...",
                    description=f"Server Left Successfully!\n\n\n I have left {guild.name}\n\n (Server ID:{guild.id})",
                    color=0x420691
                )
                embed.set_thumbnail(url=f"{guild.icon_url}")
                await ctx.send(embed=embed)
                await guild.leave()

            else:
                embed = Embed(
                    title="An Error has occured!",
                    description=f"I am not in a guild with the ID:\n{guild_name}",
                    color=0x00FA9A
                )
                await ctx.send(embed=embed)

    @command(name="snipe")
    async def get_last_message(self, ctx, target: Optional[Member]):

        LastDeleted = db.field("SELECT LastSnipe from misc WHERE GuildID = ?", ctx.guild.id)

        LastSnipe = Object()

        if LastDeleted == None:
            pass
        else:
            LastSnipe.id = LastDeleted[0]
            target = target or LastSnipe
            lastmessage = db.field("SELECT Message from snipes WHERE UserID = ?", target.id)
            messageurl = search.FindUrl(lastmessage)
            await ctx.send(lastmessage)

            # If the users message is ONLY an image.
            # if search.is_url_image(messageurl[0]) == True and messageurl[0] == lastmessage:
            #     embed = Embed(
            #         title="Sniped!",
            #         # description="lastmessage",
            #         image=messageurl[0]
            #     )
            #     await ctx.send(embed=embed)
            # #if the users message CONTAINED an IMAGE and TEXT!
            # elif search.is_url_image(messageurl[0]) == True and messageurl[0] != lastmessage:
            #     #Remove URL From User Message
            #     updatedmessage=lastmessage.replace(messageurl[0], "")
            #     embed = Embed(
            #         title="Sniped!",
            #         description=updatedmessage,
            #         image=messageurl[0]
            #     )
            # #Check if we have a last message value
            # elif lastmessage != None:
            #     embed = Embed(
            #         title="Sniped!",
            #         description = (lastmessage)
            #     )
            #     await ctx.send (embed=embed)
            # else:
            #     await ctx.send ("I could not retrieve the last message for that user, sorry!")

    @command(name="dev")
    async def devlist(self, ctx):
        embed = Embed(
            title="Developers!"
        )
        for dev in self.bot.owner_ids:
            devinfo = await self.bot.fetch_user(dev)
            embed.add_field(name=f"{devinfo.name}", value=f"{dev}", inline=True)
        await ctx.send(embed=embed)

    @command(name="rolecolor", aliases=["rc"])
    async def testrole(self, ctx, color: discord.Color):
        if ctx.author.id == 475379866775322636 or ctx.author.id == 92276895185387520:
            role = get(ctx.guild.roles, id=956102449649831936)
            rolecap = get(ctx.guild.roles, id=955635233548541982)
            await role.edit(color=color)
            embed = Embed(
                title="I have switched your color!",
                description=f"Test Color has been changed to {color}",
                color=(role.color)
            )
            if role.position != rolecap.position-1:
                await role.edit(position=rolecap.position-1)
                embed = Embed(
                    title="I have switched your color!",
                    description=f"Test Color has been changed to {color}",
                    color=(role.color)
                )

            await ctx.send(embed=embed)

    # @command(name="subswitch", aliases=["ss", "switch", "mood"])
    # async def moverole(self, ctx, role: discord.Role):
    #     if ctx.author.id == 475379866775322636 or ctx.author.id == 92276895185387520:
    #         rolecap = get(ctx.guild.roles, id=955635233548541982)
    #         if role.position != rolecap.position - 1:
    #             await role.edit(position=rolecap.position - 1)
    #             embed = Embed(
    #                 title="I have switched your Mood!",
    #                 description=f"Your Mood has been switched to {role.mention}",
    #                 color=(role.color)
    #             )
    #             await ctx.send(embed=embed)
    #         else:
    #             embed = Embed(
    #                 title="You are already in that mood!",
    #                 description=f"Your Mood is already set to {role.mention}",
    #                 color=(role.color)
    #             )
    #             await ctx.send(embed=embed)

    # if role.position is 2:
    #     await role.edit(position=3)
    # else:
    #     await role.edit(position=2)

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            self.bot.cached_messages

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("misc")


async def setup(bot):
    await bot.add_cog(misc(bot))
