import discord
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ui import Button, View
from discord import embeds
from discord import Embed


class example(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="example")
    async def exampleCommand(self, ctx):
        Running = True
        await ctx.message.delete()

        while Running:
            exitButton = Button(label="Exit", style=discord.ButtonStyle.red)
            view = View()
            view.add_item(exitButton)

            async def exit_callback(interaction):
                nonlocal Running
                await interaction.response.send_message("Exiting Example Command!", ephemeral=True)
                Running = False

            exitButton.callback = exit_callback

            embed = Embed(
                title="Test",
                description="Test"
            )

            await ctx.send(embed=embed, view=view)

            await self.bot.wait_for('interaction')

            if Running:
                print ("I don\'t want this to print")

        print("exiting")



    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("example")


async def setup(bot):
    await bot.add_cog(example(bot))
