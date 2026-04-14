import discord
from discord.ext import commands
from discord import app_commands
from utils.config import load_config, save_config

class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------
    # 設定コマンド
    # -------------------------
    @app_commands.command(name="setrole", description="文字でロール付与設定")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        name="入力する文字",
        role="付与するロール"
    )
    async def setrole(
        self,
        interaction: discord.Interaction,
        name: str,
        role: discord.Role
    ):
        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            config[guild_id] = {}

        if "autorole" not in config[guild_id]:
            config[guild_id]["autorole"] = {}

        key = name.lower().strip()

        config[guild_id]["autorole"][key] = role.id
        save_config(config)

        await interaction.response.send_message(
            f"✅ '{name}' → {role.name}",
            ephemeral=True
        )

    # -------------------------
    # 自動付与
    # -------------------------
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return

        config = load_config()
        guild_id = str(message.guild.id)

        if guild_id not in config:
            return

        data = config[guild_id]

        if "autorole" not in data:
            return

        keyword = message.content.lower().strip()

        if keyword not in data["autorole"]:
            return

        role_id = data["autorole"][keyword]
        role = message.guild.get_role(role_id)

        if role is None:
            return

        await message.author.add_roles(role)

        await message.channel.send(
            f"{message.author.mention} ✅ {role.name} を付与！"
        )

# -------------------------
# 🔥 これ必須（ないと今回のエラー出る）
# -------------------------
async def setup(bot):
    await bot.add_cog(AutoRole(bot))
