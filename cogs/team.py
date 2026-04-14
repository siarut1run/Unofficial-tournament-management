import discord
from discord.ext import commands
from utils.config import load_config

class Team(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        config = load_config()
        guild_id = str(message.guild.id)

        if guild_id not in config:
            return

        data = config[guild_id]

        if message.channel.id != data["channel_id"]:
            return

        team_name = message.content.lower().strip().replace(" ", "_")

        if team_name not in data["team_roles"]:
            await message.channel.send(f"{message.author.mention} ❌ チームなし")
            return

        role = message.guild.get_role(data["team_roles"][team_name])

        for r_id in data["team_roles"].values():
            r = message.guild.get_role(r_id)
            if r in message.author.roles:
                await message.author.remove_roles(r)

        await message.author.add_roles(role)

        await message.channel.send(
            f"{message.author.mention} ✅ {role.name}"
        )