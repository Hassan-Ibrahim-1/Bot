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

onJoinRole = 896343742544498718

class OnJoin_OnLeave(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, person):
        print(f"{person} has joined")
        await person.add_roles(person.guild.get_role(onJoinRole))

    @commands.Cog.listener() 
    async def on_member_remove(self, member):
        print(f"{member} has left")

def setup(client):
    client.add_cog(OnJoin_OnLeave(client))