import discord
from discord.ext import commands
import os
import asyncio

# -------------------------
# intents
# -------------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# -------------------------
# 起動時
# -------------------------
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"起動完了: {bot.user}")

# -------------------------
# Cog読み込み
# -------------------------
async def main():
    async with bot:
        await bot.load_extension("cogs.setup")
        await bot.load_extension("cogs.team")
        await bot.load_extension("cogs.rolemanage")
        await bot.load_extension("cogs.autorole")

        await bot.start(os.getenv("TOKEN"))

# -------------------------
# 実行
# -------------------------
asyncio.run(main())
