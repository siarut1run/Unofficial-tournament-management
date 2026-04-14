import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"起動完了: {bot.user}")

async def main():
    async with bot:
        await bot.load_extension("cogs.setup")
        await bot.load_extension("cogs.team")
        await bot.start(os.getenv("TOKEN"))

asyncio.run(main())