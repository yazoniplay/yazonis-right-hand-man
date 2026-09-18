import discord
from discord.ext import commands

class Architect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="buildserver")
    @commands.has_permissions(administrator=True)
    async def buildserver(self, ctx):
        """Automatically builds a clean, organized category and channel structure."""
        guild = ctx.guild
        await ctx.send("🏗️ **Architect Protocol Initialized:** Deploying server infrastructure...")

        try:
            # Create Core Roles
            admin_role = discord.utils.get(guild.roles, name="👑 Owner")
            if not admin_role:
                admin_role = await guild.create_role(name="👑 Owner", color=discord.Color.red(), hoist=True)

            dev_role = discord.utils.get(guild.roles, name="💻 Developer")
            if not dev_role:
                dev_role = await guild.create_role(name="💻 Developer", color=discord.Color.blue(), hoist=True)

            member_role = discord.utils.get(guild.roles, name="🛡️ Member")
            if not member_role:
                member_role = await guild.create_role(name="🛡️ Member", color=discord.Color.green(), hoist=True)

            # Create Categories and Channels
            info_cat = await guild.create_category("📊 INFORMATION")
            await guild.create_text_channel("rules", category=info_cat)
            await guild.create_text_channel("announcements", category=info_cat)
            await guild.create_text_channel("welcome", category=info_cat)

            chat_cat = await guild.create_category("💬 COMMUNITY")
            await guild.create_text_channel("general", category=chat_cat)
            await guild.create_text_channel("bot-commands", category=chat_cat)
            await guild.create_voice_channel("General Voice", category=chat_cat)

            dev_cat = await guild.create_category("⚙️ DEVELOPMENT")
            await guild.create_text_channel("server-dev", category=dev_cat)
            await guild.create_text_channel("code-snippets", category=dev_cat)
            await guild.create_voice_channel("Dev Room", category=dev_cat)

            await ctx.send("✅ **Server architecture successfully deployed!** Roles and channels are locked and loaded.")
        except Exception as e:
            await ctx.send(f"❌ Architect error: `{e}` (Make sure I have Administrator permissions!)")

async def setup(bot):
    await bot.add_cog(Architect(bot))
