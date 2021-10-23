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

class BotInfo(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.channel.send(f'{round(client.latency * 1000)}ms')

    @commands.command()
    async def stats(self, ctx):
        embed = Embed(title="Bot stats", color=ctx.author.colour, thumbnail=client.user.avatar_url, timestamp=datetime.utcnow())
        proc = Process()
        with proc.oneshot():
            uptime = timedelta(seconds=time()-proc.create_time())
            cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
            mem_total = virtual_memory().total / (1024**2)
            mem_of_total = proc.memory_percent()
            mem_usage = mem_total * (mem_of_total / 100)

        fields = [("Python version", python_version(), True), ("discord.py version", discord_version, True), ("Uptime", uptime, True), ("Cpu time", cpu_time, True), ("Memory usage", f"{mem_usage:,.3f} / {mem_total:,.0f}", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)
        return

def setup(client):
    client.add_cog(BotInfo(client))
