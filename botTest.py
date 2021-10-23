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
from discord.ext.commands import command, has_permissions, bot_has_permissions
from discord import Activity, ActivityType
from discord import __version__ as discord_version
from psutil import Process, virtual_memory
from discord.utils import find
from discord.ext import commands


intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = '.', intents=intents)

onJoinRole = 896343742544498718

class BannedUser(Converter):
	async def convert(self, ctx, arg):
		if ctx.guild.me.guild_permissions.ban_members:
			if arg.isdigit():
				try:
					return (await ctx.guild.fetch_ban(Object(id=int(arg)))).user
				except NotFound:
					raise BadArgument

		banned = [e.user for e in await ctx.guild.bans()]
		if banned:
			if (user := find(lambda u: str(u) == arg, banned)) is not None:
				return user
			else:
				raise BadArgument


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Missing a required argument.")
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have required permissions to run this command.")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("I don't have sufficient permissions!")

@client.event
async def on_member_join(person):
    print(f"{person} has joined")
    await person.add_roles(person.guild.get_role(onJoinRole))

@client.event 
async def on_member_remove(member):
    print(f"{member} has left")

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def ping(ctx):
    await ctx.channel.send(f'{round(client.latency * 1000)}ms')

@client.command()
@bot_has_permissions(ban_members=True)
@has_permissions(ban_members=True)
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
@bot_has_permissions(ban_members=True)
@has_permissions(ban_members=True)
async def kick(ctx, member : discord.Member, *, reason="No reason provided."):
    await member.kick(reason=reason)
    await ctx.channel.send(f'Kicked {member.mention} for {reason}')
    return

@client.command()
@bot_has_permissions(ban_members=True)
@has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason="No reason provided."):
    await member.ban(reason=reason)
    await ctx.channel.send(f'Banned {member.mention} for {reason}')
    return

@client.command()
@bot_has_permissions(ban_members=True)
@has_permissions(ban_members=True)
async def unban(ctx, targets : Greedy[BannedUser], *, reason: Optional[str] = "No reason provided."):
    for target in targets:
        await ctx.guild.unban(target, reason=reason)
        await ctx.send(f'Unbanned {target.mention} for {reason}')


@client.command()
@bot_has_permissions(ban_members=True)
@has_permissions(ban_members=True)
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


client.run('Token')
