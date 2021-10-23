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


PREFIX = "."
intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = PREFIX, intents=intents)


@client.command()
@has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
@has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
@has_permissions(administrator=True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')


@client.command()
@has_permissions(administrator=True)
async def console(ctx):
    await ctx.channel.send("Messages via console are enabled")
    i = True
    while i == True:
        consoleMessage = input()
        await ctx.channel.send(consoleMessage)

        if consoleMessage == 'exit':
            await ctx.channel.send("Messages via console are disabled")
            print('Messages via console are disabled')
            i = False
            return


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')



client.run('Token)
