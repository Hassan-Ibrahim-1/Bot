import discord

from discord import Embed, Member
from discord.ext.commands import Cog, CheckFailure, BadArgument, command, Bot
from discord.ext import commands 


class OnJoin_OnLeave(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    
    @commands.Cog.listener()
    async def on_member_join(self, member : commands.MemberConverter):
        
        role = member.guild.get_role(896343742544498718)
        channel = member.guild.get_channel(908977348353880095)
        await member.add_roles(role)
        await channel.send(f"{member.mention} joined the server")

    @commands.Cog.listener() 
    async def on_member_remove(self, member):
        channel = member.guild.get_channel(908977348353880095)
        await channel.send(f'{member} left the server')

def setup(client):
    client.add_cog(OnJoin_OnLeave(client))