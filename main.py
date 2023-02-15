import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from python_aternos import Client, atwss

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ATERNOS_USER = os.getenv('ATERNOS_USER')
ATERNOS_PASS = os.getenv('ATERNOS_PASS')
channel_id = '1074756389009883327'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='=', intents=intents)

aternos = Client.from_credentials(ATERNOS_USER, ATERNOS_PASS)
server = aternos.list_servers()[0]

@bot.command(name='ping')
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(name='status')
async def status(ctx):
    server.fetch()
    embed = discord.Embed(title = f"Estado: {server.status}")
    embed.set_author(name="Udsito Mods Server status", icon_url="https://media.discordapp.net/attachments/1024192333597655120/1074776049822470266/udsitogamer.png")
    if server.status == "offline":
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1074756389009883327/1075185880882487316/apagado.png")
    else:
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/1074756389009883327/1075185902030176298/boton-de-encendido.png")
    embed.add_field(name="IP", value=f"`{server.address}`", inline=False)
    embed.add_field(name="Jugadores actuales", value=f"{server.players_count}/20", inline=True)
    embed.add_field(name="Versión", value=server.version)
    embed.set_footer(text="Si el servidor esa apagado puedes usar =iniciar para encenderlo.")

    await ctx.send(embed=embed)

@bot.command(name='iniciar')
async def iniciar(ctx):
    server.fetch()
    try:
        if server.status != "online":
            server.start()
            embed = discord.Embed(title = "Se esta iniciando el server...", description="Por favor esperar entre 30 a 60 segundos para que encienda. Para revisar si ya esta activo puedes usar ´=status´.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title = "Servidor activo", description="El servidor esta funcional y corriendo.")
            await ctx.send(embed=embed)
    except:
        await ctx.send("No se puede conectar a Aternos.")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)