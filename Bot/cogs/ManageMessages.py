import discord
import random
import os
import sys

from typing import Optional
from datetime import datetime, timedelta
from discord import Embed, Member, NotFound
from time import time
from platform import python_version
from discord.ext.commands import Cog, Greedy, Converter
from discord.ext.commands import CheckFailure, BadArgument
from discord.ext.commands import command, has_permissions, bot_has_permissions, Bot
from discord import Activity, ActivityType
from discord import __version__ as discord_version
from psutil import Process, virtual_memory
from discord.utils import find
from discord.ext import commands

class manage_messages(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx):
        await ctx.channel.purge()

def setup(client):
    client.add_cog(manage_messages(client))