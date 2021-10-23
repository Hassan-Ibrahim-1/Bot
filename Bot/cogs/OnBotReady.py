import discord

from discord.ext import commands

class OnBotReady(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener() #Events
    async def on_ready(self):
        print('Bot is Online')


def setup(client):
    client.add_cog(OnBotReady(client))
