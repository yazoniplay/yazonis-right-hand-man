import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load local .env if it exists (for local testing), otherwise OS environment variables take over
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"-----------------------------------")
    print(f"Logged in as: {bot.user.name} (ID: {bot.user.id})")
    print(f"Status: Online and ready for commands.")
    print(f"-----------------------------------")

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"cogs.{cog_name}")
                print(f"[Loaded Cog]: {cog_name}")
            except Exception as e:
                print(f"[Failed to load cog {cog_name}]: {e}")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
