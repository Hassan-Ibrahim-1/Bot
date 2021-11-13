 
import discord

from discord.ext import commands

class OnCommandErrors(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
           await ctx.send("Command does not exist.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing a required argument.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention} You do not have required permissions to run this command.")
        if isinstance(error, commands.BotMissingPermissions):
            await ctx.send("I don't have sufficient permissions!")

def setup(client):
    client.add_cog(OnCommandErrors(client))