import discord
import requests
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow, wait_for_component, ComponentContext
from discord_slash.utils.manage_commands import create_choice, create_option

api_root = "https://world-mood-333716.appspot.com"

mood_prompt = create_actionrow(
    create_select(
        options=[
            create_select_option("Happy", value="happy", emoji="😊"),
            create_select_option("Angry", value="angry", emoji="👺"),
            create_select_option("Sad", value="sad", emoji="😔")
        ],
        placeholder="Choose your option",
        min_values=1,
        max_values=1,
    )
)

class SubmitMood(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["add-mood", "redirect", "add"])
    async def submit(self, ctx, mood: str = None):
        if mood is not None:
            res = requests.get(f"{api_root}/mood/is-valid?mood={mood.lower()}")
            if res.status_code == 200:
                
                submit_url = f"{api_root}/mood-bot?mood={mood.lower()}"

                res_embed = discord.Embed(title="Submit your mood", description=f"Click the following link to submit your mood:\n{submit_url}", color=0x00ff00)
                await ctx.send(embed=res_embed)

            else:
                await ctx.send("You have entered invalid mood. Please try again.")

        else:
            prompt_embed = discord.Embed(title="Submit your mood", description="Here, you can select your mood and submit it quickly, please select your mood from the selection below", color=0x00ff00)
            prompt_embed.set_footer(icon_url=self.client.user.avatar_url, text=f"{self.client.user.name}#{self.client.user.discriminator}")
            await ctx.send(embed=prompt_embed, components=[mood_prompt])

            button_ctx: ComponentContext = await wait_for_component(self.client, components=mood_prompt, timeout=30)
            selected_mood = button_ctx.values[0]

            submit_url = f"{api_root}/mood-bot?mood={selected_mood}"
                
            res_embed = discord.Embed(title="Submit your mood", description=f"Click the following link to submit your mood:\n{submit_url}", color=0x00ff00)
            await button_ctx.edit_origin(embed=res_embed, components=[])

    @cog_ext.cog_slash( name="Submit", 
                        description="Submit your mood!", 
                        guild_ids=[901125693113524295],
                        options=[
                            create_option(
                                name="mood",
                                description="Submit your mood",
                                option_type=3,
                                required=False,
                                choices=[
                                    create_choice(
                                        name="Happy",
                                        value="happy"
                                    ),
                                    create_choice(
                                        name="Angry",
                                        value="angry"
                                    ),
                                    create_choice(
                                        name="Sad",
                                        value="sad"
                                    )
                                ]
                            )
                        ]
                    )



    async def _submit(self, ctx: SlashContext, mood: str = None):
        await self.submit(ctx, mood)

def setup(client):
    client.add_cog(SubmitMood(client))