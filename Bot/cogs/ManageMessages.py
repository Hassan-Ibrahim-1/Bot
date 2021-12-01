import discord

from typing import Optional
from discord import Embed, Member
from discord.ext.commands import Cog, Converter
from discord.ext.commands import CheckFailure, BadArgument
from discord.ext.commands import command, has_permissions, bot_has_permissions, Bot


from discord.ext import commands

class manage_messages(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @has_permissions(manage_messages=True)
    async def purge(self, ctx, amount : Optional[int]):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @has_permissions(manage_messages=True)
    async def clear(self, ctx, member : discord.Member, amount : Optional[int]):
        async for message in ctx.channel.history(limit=amount):
            if message.author == ctx.author:
                await message.delete()


def setup(client):
    client.add_cog(manage_messages(client))