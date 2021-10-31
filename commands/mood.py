import discord
import requests
from discord.ext import commands

api_root = "http://77.87.241.39:5000/"

class Mood(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def current(self, ctx):
        res = requests.get(api_root + "current/all")
        emoji = res.json()["emoji"]
        text = res.json()["text"]
        
        embed=discord.Embed(title="World's mood", description=f"The World's mood at the moment is \n**{emoji} {text}**", color=0x3db548)
        embed.set_thumbnail(url="https://kristn.tech/api/world-mood/image/banner-zoom-transparent.png")
        embed.set_footer(text=self.client.user.name, icon_url=self.client.user.avatar_url)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Mood(client))