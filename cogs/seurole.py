import discord
from discord.ext import commands
from discord import app_commands
from utils.config import load_config, save_config

class SeuRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------
    # 設定コマンド
    # -------------------------
    @app_commands.command(name="seurole", description="文字でロール付与設定（チャンネル指定付き）")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        channel="反応させるチャンネル",
        name="入力する文字",
        role="付与するロール"
    )
    async def seurole(
        self,
        interaction: discord.Interaction,
        channel: discord.TextChannel,
        name: str,
        role: discord.Role
    ):
        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            config[guild_id] = {}

        if "seurole" not in config[guild_id]:
            config[guild_id]["seurole"] = {}

        key = name.lower().strip()

        config[guild_id]["seurole"][key] = {
            "channel_id": channel.id,
            "role_id": role.id
        }

        save_config(config)

        await interaction.response.send_message(
            f"✅ '{name}' → {role.name}（{channel.mention}限定）",
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

        if "seurole" not in data:
            return

        keyword = message.content.lower().strip()

        if keyword not in data["seurole"]:
            return

        setting = data["seurole"][keyword]

        # チャンネル制限
        if message.channel.id != setting["channel_id"]:
            return

        role = message.guild.get_role(setting["role_id"])

        if role is None:
            return

        await message.author.add_roles(role)

        await message.channel.send(
            f"{message.author.mention} ✅ {role.name} を付与！"
        )

# 必須
async def setup(bot):
    await bot.add_cog(SeuRole(bot))
