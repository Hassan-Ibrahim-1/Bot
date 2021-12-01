import discord
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

        if amount.isdigit() and unit in ['s', 'm', 'h', 'd', 'y']:
            return (int(amount), unit)
        
        raise BadArgument(message='Not a vaild duration')

class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @bot_has_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason="No reason provided."):
        await member.send(f"{member.mention} you have been kicked from the server {member.guild.name} for {reason}")
        await member.kick(reason=reason)
        await ctx.channel.send(f'Kicked {member.mention} for {reason}')
        
    
    @commands.command()
    @has_permissions(ban_members=True)
    @bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member : commands.MemberConverter, duration : Optional[DurationConverter] = 0, *, reason="No reason provided"):
        if duration == 0:
            await member.send(f"{member.mention} you have been banned from the server {member.guild.name} for {reason}")
            await member.ban(reason=reason)
            await ctx.channel.send(f'Banned {member.mention} for {reason}.')
            

        if duration != 0:
            multiplier = {'s' : 1, 'm': 60, 'h': 3600, 'd': 86400, 'y': 31536000}
            amount, unit = duration
            await member.send(f"{member.mention} you have been temporarily banned from the server {member.guild.name} for {amount}{unit} for {reason}")
            await member.ban(reason=reason)
            await ctx.send(f'{member.mention} has been temporarily banned for {amount}{unit} for {reason}')

            await asyncio.sleep(amount * multiplier[unit])
            await ctx.guild.unban(member)
            

    @commands.command()
    @bot_has_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    async def unban(self, ctx, targets : Greedy[BannedUser], *, reason: Optional[str] = "No reason provided."):
        for target in targets:
            await ctx.guild.unban(target, reason=reason)
            await ctx.send(f'Unbanned {target.mention} for {reason}')


    @commands.command(aliases=["ar,", "role"])
    @bot_has_permissions(administrator=True)
    @has_permissions(administrator=True)
    async def addrole(self, ctx, member : discord.Member, role : discord.Role):
        await member.add_roles(role)
        await ctx.send(f'Added the role {role.mention} to {member.mention}.')


    @commands.command(aliases=["rr"])
    @bot_has_permissions(administrator=True)
    @has_permissions(administrator=True)
    async def removerole(self, ctx, member : discord.Member, role : discord.Role):
        await member.remove_roles(role)
        await ctx.send(f'Removed the role {role.mention} from {member.mention}.')


    @commands.command(aliases=['message', 'sendmessage'])
    @has_permissions(administrator=True)
    async def dm(self, ctx, member : discord.Member, *, message="test"):
        await member.send(message)
        await ctx.send(f"Message sent to {member.mention}")


    @commands.command(aliases=['invite'])
    @has_permissions(administrator=True)
    async def createinvite(self, ctx, uses : Optional = 50, time_in_seconds : Optional = 1000):
        link = await discord.abc.GuildChannel.create_invite(ctx.message.channel, max_uses=uses, max_age=time_in_seconds)
        await ctx.channel.send(link)


    @commands.command(aliases=["nick"])
    @has_permissions(administrator=True)
    async def changenick(self, ctx, member : discord.Member, *, newNick):
        await member.edit(nick=newNick)
        await ctx.send(f"Changed the nick of {member.mention} to {newNick}.")

    @commands.command(aliases=["nickremove"])
    @has_permissions(administrator=True)
    async def removenick(self, ctx, member : discord.Member):
        await member.edit(nick=None)
        await ctx.send(f"Removed the nick of {member.mention}")

    
    @commands.command()
    @has_permissions(administrator=True)
    async def mute(self, ctx, member : discord.Member, duration : Optional[DurationConverter] = 0, *, reason : Optional[str] = "No reason provided"):
        if duration == 0:
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages = False), reason=reason)

            for channel in ctx.guild.voice_channels:
                await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)
            await ctx.send(f"Muted {member.mention} for {reason}")

        if duration != 0:
            multiplier = {'s' : 1, 'm': 60, 'h': 3600, 'd': 86400, 'y': 31536000}
            amount, unit = duration
            for channel in ctx.guild.text_channels:
                await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(send_messages=False), reason=reason)
            await ctx.channel.send(f"Muted {member.mention} for {amount}{unit} for {reason}")

            for channel in ctx.guild.voice_channels:
                await channel.set_permissions(member, overwrite=discord.PermissionOverwrite(speak=False), reason=reason)

            await asyncio.sleep(amount * multiplier[unit])
            for channel in ctx.guild.channels:
                await channel.set_permissions(member, overwrite=None, reason=reason)


    @commands.command()
    @has_permissions(administrator=True)
    async def unmute(self, ctx, member : discord.Member, reason : Optional[str] = "No reason provided"):
        for channel in ctx.guild.channels:
            await channel.set_permissions(member, overwrite=None, reason=reason)
        await ctx.send(f"Unmuted {member.mention} for {reason}")
        

    @commands.command(aliases=["sl", "slow"])
    @has_permissions(administrator=True)
    async def slowmode(self, ctx, duration : Optional[int] = 5):
        await ctx.channel.edit(slowmode_delay=duration)
        await ctx.send(f"Set the slowmode delay in this channel to {duration} seconds")
    
    @commands.command(aliases=["rsl"])
    @has_permissions(administrator=True)
    async def removeslowmode(self, ctx):
        await ctx.channel.edit(slowmode_delay=None)
        await ctx.send("Removed the slowmode delay in this channel")




def setup(client):
    client.add_cog(Mod(client))