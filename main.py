import os
from discord.ext import commands
from dotenv import load_dotenv
import discord
import asyncio
load_dotenv()

bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())

# remove the default help command so that we can write our own
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Success: Bot is connected to discord')


# load all cogs
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


# start the  bot with our token
async def main():
    async with bot:
        await load()
        await bot.start(os.getenv("TOKEN"))
asyncio.run(main())