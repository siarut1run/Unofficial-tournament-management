import discord
from discord.ext import commands
from discord import app_commands
from utils.config import load_config, save_config

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()

    async def create_room(self, guild, role, limit):
        if discord.utils.get(guild.categories, name=role.name):
            return False

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            role: discord.PermissionOverwrite(view_channel=True)
        }

        category = await guild.create_category(role.name, overwrites=overwrites)
        await guild.create_text_channel("チャット", category=category)

        if limit:
            await guild.create_voice_channel("通話", category=category, user_limit=limit)
        else:
            await guild.create_voice_channel("通話", category=category)

        return True

    @app_commands.command(name="setup", description="チーム設定")
    async def setup(self, interaction: discord.Interaction,
                    channel: discord.TextChannel,
                    team_name: str,
                    role: discord.Role,
                    limit: int = None):

        guild_id = str(interaction.guild.id)

        if guild_id not in self.config:
            self.config[guild_id] = {
                "channel_id": channel.id,
                "team_roles": {}
            }

        name = team_name.lower().replace(" ", "_")

        self.config[guild_id]["channel_id"] = channel.id
        self.config[guild_id]["team_roles"][name] = role.id

        save_config(self.config)

        created = await self.create_room(interaction.guild, role, limit)

        msg = f"✅ {team_name} 設定完了"
        msg += "\n📁 部屋作成" if created else "\n⚠️ 既に存在"

        await interaction.response.send_message(msg, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Setup(bot))