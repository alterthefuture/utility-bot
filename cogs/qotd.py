import asyncio
from discord.ext import commands
from helper import *
import discord

class qotd(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def qotd(self,ctx):
        await ctx.send(embed=create_embed("Please enter a QOTD."))

        check = lambda m: m.author == ctx.author and m.channel == ctx.channel

        try:
            qotd_message = await self.bot.wait_for("message", check=check, timeout=120)

            embed=discord.Embed(title="Good Morning! It's time for your QOTD",description=f"{qotd_message.content}",color=discord.Color.green())

            await ctx.send(embed=create_embed("Perfect! Does this look correct?"))
            await ctx.send(embed=embed)

            for channel in list(ctx.guild.channels):
                if channel.name == 'qotd':
                    channel_id = channel.id
                    break

            try:
                for i in range(10):
                    correct = await self.bot.wait_for("message", check=check, timeout=15)

                    if correct.content == 'yes':
                        channel = self.bot.get_channel(channel_id)
                        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/552927506957729802.gif?v=1")
                        await channel.send(embed=embed)
                        break
                        
                    elif correct.content == 'no':
                        await ctx.send(embed=error_embed("Sorry, please restart the process."))
                        break
                    else:
                        await ctx.send(embed=error_embed("Please state either yes or no."))
                
            except asyncio.TimeoutError:
                await ctx.send(embed=error_embed("You weren't fast enough, please try again later."))
                return

        except asyncio.TimeoutError:
            await ctx.send(embed=error_embed("You weren't fast enough, please try again later."))
            return

def setup(bot):
    bot.add_cog(qotd(bot))