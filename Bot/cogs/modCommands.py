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

class KickMembers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason="No reason provided."):
        await member.kick(reason=reason)
        await ctx.channel.send(f'Kicked {member.mention} for {reason}')
        return

class BanMembers(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason="No reason provided."):
        await member.ban(reason=reason)
        await ctx.channel.send(f'Banned {member.mention} for {reason}')
        return

class UnbanMembers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def unban(self, ctx, targets : Greedy[BannedUser], *, reason: Optional[str] = "No reason provided."):
        for target in targets:
            await ctx.guild.unban(target, reason=reason)
            await ctx.send(f'Unbanned {target.mention} for {reason}')

def setup(client):
    client.add_cog(KickMembers(client))
    client.add_cog(BanMembers(client))
    client.add_cog(UnbanMembers(client))