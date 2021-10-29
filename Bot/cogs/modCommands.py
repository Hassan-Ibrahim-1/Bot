import discord
import random
import os
import sys
import asyncio

from typing import Optional
from datetime import datetime, timedelta
from discord import Embed, Member, NotFound
from time import time
from platform import python_version
from discord.ext.commands import Cog, Greedy, Converter
from discord.ext.commands import CheckFailure, BadArgument
from discord.ext.commands import command, has_permissions, bot_has_permissions, Bot
from discord import Activity, ActivityType
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

class DurationConverter(Converter):
    async def convert(self, ctx, argument):
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm', 'h', 'd']:
            return (int(amount), unit)
        
        raise BadArgument(message='Not a vaild duration')

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
    async def ban(self, ctx, member : commands.MemberConverter, *, reason="No reason provided."):
        await member.ban(reason=reason)
        await ctx.channel.send(f'Banned {member.mention} for {reason}')
        return

class TempBanMembers(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def tempban(self, ctx, member : commands.MemberConverter, duration: DurationConverter, *, reason="No reason provided."):
        multiplier = {'s' : 1, 'm': 60, 'h': 3600, 'd': 86400}
        amount, unit = duration

        await member.ban(reason=reason)
        await ctx.send(f'{member} has been temporarily banned for {reason} for {amount}{unit}.')
        await asyncio.sleep(amount * multiplier[unit])
        await ctx.guild.unban(member)
    

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
    client.add_cog(TempBanMembers(client))