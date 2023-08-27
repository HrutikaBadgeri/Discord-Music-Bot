import discord
from discord.ext import commands
import datetime as dt


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_message = """
 General Commands:
 • prefix used - >
 • >help/h - displays all the available commands
 • >join/j - the bot will join the respective voice channel 
 • >play <keyword>/p - finds the songs on youtube and plays it in your current channel. 
 • >queue/q - displays the current music queue
 • >skip/s - skips the current song being played
 • >clear/c - stops the music and clears the queue
 • >stop/st - stops the bot from playing music
 • >disconnect/dc/leave/d - disconnect the bot from the voice channel
 • >pause/ps - pauses the current song being played
 • >resume/r - resume playing the current song
 • >lyrics - gets the lyrics of the song currently playing 
 • >remove/rem - removes a song from the queue according to the position specified 
 • >loop/l - loops the current song 
 • >loop_off/lo - turns off the loop 
 • >current/curr - returns the current song that is playing  
  """

    @commands.command(name="help", aliases=["h"], help="Displays all the available commands")
    async def help(self, ctx):
        embed = discord.Embed(
            title="Help Commands",
            description="Displays all the available commands for the bot" + self.help_message,
            color=ctx.author.color,
            timestamp=dt.datetime.utcnow()
        )
        embed.set_author(name=ctx.author)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(help(bot))
