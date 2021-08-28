from discord.ext import commands
import discord
import os

intents=discord.Intents.all()
bot = commands.Bot(command_prefix="!",intents=intents)   

@bot.event
async def on_ready():
    print("> Bot is online!")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run("token-here")

