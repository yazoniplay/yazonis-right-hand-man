import os
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from discord.ext import commands

# 1. Render Port-Binding Dummy Server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Yazoni's Right Hand is online and active!")
    
    def log_message(self, format, *args):
        return  # Suppress console log spam

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Spin up the web server thread immediately
threading.Thread(target=run_dummy_server, daemon=True).start()

# 2. Discord Intents Setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("Yazoni's Right Hand is locked, loaded, and online!")

async def main():
    async with bot:
        # Load all cogs safely with error catching
        extensions = ["cogs.companion", "cogs.architect", "cogs.scout"]
        
        for ext in extensions:
            try:
                await bot.load_extension(ext)
                print(f"Successfully loaded extension: {ext}")
            except Exception as e:
                print(f"Failed to load extension {ext}: {e}")

        token = os.getenv("DISCORD_TOKEN")
        if not token:
            print("ERROR: DISCORD_TOKEN environment variable not found!")
            return
        
        await bot.start(token)

if __name__ == "__main__":
    asyncio.run(main())
