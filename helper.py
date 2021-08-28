import discord

def create_embed(text):
    embed = discord.Embed(description=text,color=discord.Color.green())

    return embed

def error_embed(text):
    embed = discord.Embed(description=text,color=discord.Color.red())

    return embed