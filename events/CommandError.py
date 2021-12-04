import discord
import difflib
from discord.ext import commands

class Ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def suggestCommand(self, user_input):
        available_commands = []
        for command in self.client.commands:
            available_commands.append(command.name)

        try:
            return f"Did you mean `!{difflib.get_close_matches(user_input, available_commands)[0]}`?"
        except:
            return f"You can do `!help` to see all the available commands"

    async def get_error_embed(self, title: str, description: str):
        embed = discord.Embed(title=title, description=description, color=0xFF0000)
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        return embed

    async def handle_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(embed=await self.get_error_embed("Command not found", "The command you tried to use was not found.\n" + await self.suggestCommand(ctx.message.content.split(" ")[0][1:])))
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=await self.get_error_embed("Missing argument", "The command you tried to use is missing an argument.\n\n"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self.handle_error(ctx, error)

def setup(client):
    client.add_cog(Ready(client))