import discord

from discord.ext import commands
from discord.ext.commands import has_permissions


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    
    @commands.command()
    @has_permissions(administrator=True)
    async def poll(self, ctx, pollContent):
        await ctx.channel.purge(limit=1)
        message = await ctx.channel.send(f"Poll: {pollContent}")
        await message.add_reaction("✅")
        await message.add_reaction("❎")

    @commands.command()
    async def membercount(self, ctx):
        await ctx.send(f"This server has {ctx.guild.member_count} members")



def setup(client):
    client.add_cog(Misc(client))