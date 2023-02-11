import discord
from discord import *
from discord.ui import *
from discord.ext import commands, tasks



bot = commands.Bot(command_prefix="-", help_command=None, intents=discord.Intents.all())

config = {
    "token":"MTA3MzkxMzgxMTUwNzA5MzU2Ng.GXJHc7.g2sZ3W0-s7xVBE7Ewa_9kkIiqzsVlAvSmZ4Ngw",
}


@bot.command()
async def setup(ctx, channel:int = None):
    if channel == None:
        button = Button(
            style=ButtonStyle.link,
            label="Verify",
            url="https://discord.com/api/oauth2/authorize?client_id=1073913811507093566&redirect_uri=http://localhost:8080/callback&response_type=code&scope=identify%20guilds%20email%20guilds.join"
        )
        async def res(interaction):
                await interaction.response.send_message("a")
        guild = ctx.message.guild
        a = await guild.create_text_channel("Verify")
        await button.callback( res)
        vie = View()
        vie.add_item(button)
        await a.send(embed=Embed(title="Verify", description="Click the button below to verify in this server!"), view=vie)
    else:
        
        button = Button(
            style=ButtonStyle.link,
            label="Verify",
            url="https://discord.com/api/oauth2/authorize?client_id=1073913811507093566&redirect_uri=http://localhost:8080/callback&response_type=code&scope=identify%20guilds%20email%20guilds.join"
        )
        

        vie = View()
        vie.add_item(button)
        await a.send(embed=Embed(title="Verify", description="Click the button below to verify in this server!"), view=vie)

bot.run(config['token'])