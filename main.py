import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

#  import all of the cogs
from help import help
from music import music

bot = commands.Bot(command_prefix=">")

# remove the default help command so that we can write our own
bot.remove_command('help')

# register the class with the bot
bot.add_cog(help(bot))
bot.add_cog(music(bot))

# start the  bot with our token
bot.run(os.getenv("TOKEN"))
