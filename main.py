import os
from discord.ext import commands
from discord_slash import SlashCommand
from utils import config

client = commands.Bot(command_prefix="!", case_insensitive=True)
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)

cog_folders = ["events", "commands"]

for cog in cog_folders:
    for filename in os.listdir(f"./{cog}"):
        if filename.endswith(".py"):
            client.load_extension(f"{cog}.{filename[:-3]}")

client.run(config.get_token())