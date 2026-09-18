import os
import discord
from discord.ext import commands
from google import genai
from google.genai import types

class Companion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Initialize the Google GenAI client using the active SDK
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        # Using gemini-3.5-flash-lite as configured
        self.model_name = "gemini-3.5-flash-lite"
        
        # Store chat sessions per channel/user for memory
        self.chat_sessions = {}

    def get_or_create_chat(self, thread_id):
        if thread_id not in self.chat_sessions:
            self.chat_sessions[thread_id] = self.client.chats.create(
                model=self.model_name,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are Yazoni's Right Hand, a personalized, ultra-loyal 24/7 AI companion "
                        "and server manager built exclusively for Yazan. Talk naturally, keep it sharp, "
                        "and act like a true right-hand man."
                    )
                )
            )
        return self.chat_sessions[thread_id]

    # Change from a command to an event listener that triggers on every message
    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore messages sent by the bot itself
        if message.author == self.bot.user:
            return

        # Optional: Restrict this to only reply to you (using your username or user ID if you want)
        # For now, it will respond to any message that doesn't start with command prefixes like '!'
        if message.content.startswith("!"):
            return # Let standard commands like !buildserver or !scout work normally

        # Automatically show typing status while generating response
        async with message.channel.typing():
            try:
                chat = self.get_or_create_chat(message.channel.id)
                response = chat.send_message(message.content)
                await message.reply(response.text)
            except Exception as e:
                await message.channel.send(f"❌ Companion error: `{e}`")

async def setup(bot):
    await bot.add_cog(Companion(bot))
