import discord
from discord.ext import commands
from discord import app_commands
from utils.config import load_config, save_config

class RoleManage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -------------------------
    # オーナー設定
    # -------------------------
    @app_commands.command(name="set-owner", description="オーナーロールを設定")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_owner(self, interaction: discord.Interaction, role: discord.Role):

        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            config[guild_id] = {}

        config[guild_id]["owner_role"] = role.id
        save_config(config)

        await interaction.response.send_message(
            f"👑 オーナーロールを {role.name} に設定！",
            ephemeral=True
        )

    # -------------------------
    # 運営設定
    # -------------------------
    @app_commands.command(name="set-admin", description="運営ロールを設定")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_admin(self, interaction: discord.Interaction, role: discord.Role):

        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            config[guild_id] = {}

        config[guild_id]["admin_role"] = role.id
        save_config(config)

        await interaction.response.send_message(
            f"🛠️ 運営ロールを {role.name} に設定！",
            ephemeral=True
        )

    # -------------------------
    # 権限確認
    # -------------------------
    @app_commands.command(name="role-check", description="自分の権限を確認")
    async def role_check(self, interaction: discord.Interaction):

        config = load_config()
        guild_id = str(interaction.guild.id)

        if guild_id not in config:
            await interaction.response.send_message("❌ 未設定", ephemeral=True)
            return

        data = config[guild_id]
        member = interaction.user

        owner_id = data.get("owner_role")
        admin_id = data.get("admin_role")

        if owner_id and discord.utils.get(member.roles, id=owner_id):
            result = "👑 オーナー"
        elif admin_id and discord.utils.get(member.roles, id=admin_id):
            result = "🛠️ 運営"
        else:
            result = "👤 一般メンバー"

        await interaction.response.send_message(
            f"あなたは：{result}です",
            ephemeral=True
        )

# -------------------------
# 必須（これないと読み込めない）
# -------------------------
async def setup(bot):
    await bot.add_cog(RoleManage(bot))
