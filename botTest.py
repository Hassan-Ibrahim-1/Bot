import discord
import random
import os
import sys

from datetime import datetime, timedelta
from discord import Embed
from time import time
from platform import python_version
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Activity, ActivityType
from discord import __version__ as discord_version
from psutil import Process, virtual_memory
from guppy import hpy
from discord.ext import commands


client = commands.Bot(command_prefix=".")


# Tells you when the bot is online
@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def ping(ctx):
    await ctx.channel.send(f'{round(client.latency * 1000)}ms')

@client.command()
@commands.has_role('admin')
async def clear(ctx):
    await ctx.channel.purge()

@client.command(name="stats")
async def bot_stats(ctx):
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

@client.command()
@commands.has_role('admin')
async def kick(ctx, member : discord.Member, *, reason=None):

    await member.kick(reason=reason)
    await ctx.channel.send(f'Kicked {member.mention} for {reason}')
    return

@client.command()
@commands.has_role('admin')
async def ban(ctx, member : discord.Member, *, reason=None):

    await member.ban(reason=reason)
    await ctx.channel.send(f'Banned {member.mention} for {reason}')
    return

@client.command()
@commands.has_role('admin')
async def unban(ctx, *, member):

    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.send(f'Unbanned {member}')
            return

# Executes code when a message is sent
@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author.id == 759699257950994482 and message.content == 'test console' and message.channel.id == 891313671685435442:

        # if i(0) < 2, do this
        i = False
        while i == False:
            consoleMessage = input()
            await message.channel.send(consoleMessage)  # await message.channel.send() sends a message through the bot

            # If the value is _
            if consoleMessage == 'exit':
                await message.channel.send("Messages via console disabled")
                print('Messages via console disabled')
                i = True

    if message.author.id == 759699257950994482 and message.content == 'test console' and message.channel.id == 891373151924154418:

        # if i(0) < 2, do this
        i = False
        while i == False:
            consoleMessage = input()
            await message.channel.send(consoleMessage)  # await message.channel.send() sends a message through the bot

            # If the value is _
            if consoleMessage == 'exit':
                await message.channel.send("Messages via console disabled")
                print('Messages via console disabled')
                i = True
        



# Run the user with this token
client.run('ODkwOTA3NzMzNDE3Njg1MDEy.YU2oew.ONcjMB-MILH17_M08_Z34cjZgSw')
