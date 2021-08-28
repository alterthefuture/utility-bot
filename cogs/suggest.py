from discord.ext import commands
import discord
from helper import *
import asyncio

class suggest(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def suggest(self,ctx):
        check = lambda m: m.author == ctx.author and m.guild is None

        try:
            await ctx.author.send(embed=create_embed("Please write the suggestion title."))
            await ctx.send(embed=create_embed("Please check your direct messages."))
        except:
            return await ctx.send(embed=error_embed("Please enable direct messages and try again."))

        try:
            for i in range(10):
                suggest_title = await self.bot.wait_for("message", check=check, timeout=120)

                await ctx.author.send(embed=create_embed("Finally, what would you like to suggest(in detail)?"))

                try:
                    suggest_desc = await self.bot.wait_for("message", check=check, timeout=180)

                    await ctx.author.send(embed=create_embed("Perfect! Would you like to send it?"))
                    
                    try:
                        for i in range(10):
                            correct = await self.bot.wait_for("message", check=check, timeout=30)

                            if correct.content == "yes":
                                for channel in list(ctx.guild.channels):
                                    if channel.name == "suggestions":
                                        break

                                embed=discord.Embed(title=suggest_title.content,description=suggest_desc.content,color=discord.Color.green())
                                embed.set_footer(text=f"Requested by {ctx.author}")

                                msg = await channel.send(embed=embed)
                                await msg.add_reaction("✅")

                                await ctx.author.send(embed=create_embed("Your suggestion has been sent, please be patient."))
                                break
                            elif correct.content == "no":
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
        
        except asyncio.TimeoutError:
            await ctx.send(embed=error_embed("You weren't fast enough, please try again later."))
            return

    @suggest.error
    async def suggest_error(ctx,error):
        if isinstance(error,commands.CommandOnCooldown):
            await ctx.send(embed=error_embed(f"Please wait **{error.retry_after:.2f}** seconds before running this command again."))

def setup(bot):
    bot.add_cog(suggest(bot))