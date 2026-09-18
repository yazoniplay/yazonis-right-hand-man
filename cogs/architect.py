import discord
from discord.ext import commands

class Architect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="buildserver")
    @commands.has_permissions(administrator=True)
    async def buildserver(self, ctx):
        """Quickly sets up standard categories, channels, and roles."""
        guild = ctx.guild
        await ctx.send("🏗️ **Architect Protocol Initialized:** Deploying server infrastructure...")

        try:
            # Create Core Roles
            admin_role = discord.utils.get(guild.roles, name="👑 Owner")
            if not admin_role:
                await guild.create_role(name="👑 Owner", color=discord.Color.red(), hoist=True)

            dev_role = discord.utils.get(guild.roles, name="💻 Developer")
            if not dev_role:
                await guild.create_role(name="💻 Developer", color=discord.Color.blue(), hoist=True)

            member_role = discord.utils.get(guild.roles, name="🛡️ Member")
            if not member_role:
                await guild.create_role(name="🛡️ Member", color=discord.Color.green(), hoist=True)

            # Create Categories and Channels
            info_cat = await guild.create_category("📊 INFORMATION")
            await guild.create_text_channel("rules", category=info_cat)
            await guild.create_text_channel("announcements", category=info_cat)

            chat_cat = await guild.create_category("💬 COMMUNITY")
            await guild.create_text_channel("general", category=chat_cat)
            await guild.create_text_channel("bot-commands", category=chat_cat)
            await guild.create_voice_channel("General Voice", category=chat_cat)

            await ctx.send("✅ **Server architecture successfully deployed!**")
        except Exception as e:
            await ctx.send(f"❌ Architect error: `{e}`")

    # --- CHANNEL MANAGEMENT ---
    @commands.command(name="mkchan")
    @commands.has_permissions(manage_channels=True)
    async def mkchan(self, ctx, channel_type: str, name: str):
        """Creates a channel. Usage: !mkchan text announcements OR !mkchan voice Lounge"""
        guild = ctx.guild
        if channel_type.lower() == "text":
            await guild.create_text_channel(name)
            await ctx.send(f"📁 Created text channel: `#{name}`")
        elif channel_type.lower() == "voice":
            await guild.create_voice_channel(name)
            await ctx.send(f"🔊 Created voice channel: `🔊 {name}`")
        else:
            await ctx.send("❌ Use `text` or `voice`. Example: `!mkchan text rules`")

    @commands.command(name="delchan")
    @commands.has_permissions(manage_channels=True)
    async def delchan(self, ctx, channel: discord.TextChannel = None):
        """Deletes a channel. Tag it or run it inside the channel: !delchan #channel"""
        target = channel or ctx.channel
        name = target.name
        await target.delete()
        await ctx.send(f"🗑️ Deleted channel: `#{name}`")

    # --- ROLE MANAGEMENT ---
    @commands.command(name="mkrole")
    @commands.has_permissions(manage_roles=True)
    async def mkrole(self, ctx, *, role_name: str):
        """Creates a new role. Usage: !mkrole VIP"""
        guild = ctx.guild
        role = await guild.create_role(name=role_name, hoist=True)
        await ctx.send(f"✨ Created role: **{role.name}**")

    @commands.command(name="delrole")
    @commands.has_permissions(manage_roles=True)
    async def delrole(self, ctx, *, role: discord.Role):
        """Deletes a role by name. Usage: !delrole VIP"""
        role_name = role.name
        await role.delete()
        await ctx.send(f"❌ Deleted role: **{role_name}**")

async def setup(bot):
    await bot.add_cog(Architect(bot))
