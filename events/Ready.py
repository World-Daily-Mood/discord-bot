import discord
from discord.ext import commands

class Ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="How the World is feeling"))

        print("Bot is ready")

def setup(client):
    client.add_cog(Ready(client))