import os
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

# 1. Dummy HTTP Server to satisfy Render's Web Service port-binding requirement
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Yazoni's Right Hand is online and active!")
    
    # Suppress server log spam in the console
    def log_message(self, format, *args):
        return

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Start the dummy web server in the background before the bot initializes
threading.Thread(target=run_dummy_server, daemon=True).start()

# 2. Setup Discord Bot Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("Yazoni's Right Hand is locked, loaded, and online!")

async def main():
    async with bot:
        # Load cogs
        await bot.load_extension("cogs.companion")
        
        # Uncomment these once you create architect.py and scout.py
        # await bot.load_extension("cogs.architect")
        # await bot.load_extension("cogs.scout")
        
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            print("ERROR: DISCORD_TOKEN environment variable not found!")
            return
        
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
