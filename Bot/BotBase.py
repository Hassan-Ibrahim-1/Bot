import discord
import os
import sys
import json

from discord import Embed, Member, NotFound
from discord.ext.commands import command, has_permissions, bot_has_permissions, Bot
from discord.utils import find
from discord.ext import commands, tasks
from itertools import cycle


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = get_prefix, intents=intents, pm_help=True)

@client.event
async def on_ready():
    print("Bot is Online")
    await client.change_presence(activity=discord.Game(".help"))

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command()
@has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}')


@client.command()
@has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'loaded {extension}')

@client.command()
@has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'unloaded {extension}')

@client.command()
@has_permissions(administrator=True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'reloaded {extension}')

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



client.run('ODkwOTA3NzMzNDE3Njg1MDEy.YU2oew.iRtzeA7tCNi__UaXaaQvrQif73w')