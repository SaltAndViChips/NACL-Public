import discord
from discord import Embed, Member
# from discord_components import DiscordComponents, Select, SelectOption, Button, ButtonStyle
from typing import Optional
from discord.utils import get
from ..db import db
from ..imports import search
import asyncio

async def moodmenu(self):
    """Sends a message with our dropdown containing colours"""
    channel = 956342454720802907
    moodview = MoodDropDownView()
    roleview = RoleDropDownView()
    # Sending a message containing our view
    if ctx.message != None:
        await ctx.message.delete()
    async with ctx.channel.typing():
        deleted = await ctx.channel.purge(limit=100)
    await ctx.send("How are you feeling princess?", view=moodview)
    await ctx.send("Just picking a role?", view=roleview)