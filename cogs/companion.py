import os
import asyncio
import discord
from discord.ext import commands
from google import genai
from google.genai import types

class Companion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        # Updated to the current active model identifier
        self.model_name = "gemini-3.6-flash"
        self.chat_sessions = {}

    def get_or_create_chat(self, thread_id):
        if thread_id not in self.chat_sessions:
            self.chat_sessions[thread_id] = self.client.chats.create(
                model=self.model_name,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are Yazoni's Right Hand, a personalized, ultra-loyal 24/7 AI companion "
                        "and server manager built exclusively for Yazan. Talk naturally, keep it sharp, "
                        "and act like a true right-hand man who can see and analyze any images he sends you."
                    )
                )
            )
        return self.chat_sessions[thread_id]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.content.startswith("!"):
            return # Let standard commands like !buildserver work normally

        async with message.channel.typing():
            try:
                chat = self.get_or_create_chat(message.channel.id)
                
                contents = []
                if message.content:
                    contents.append(message.content)
                else:
                    contents.append("What do you see in this image?")

                for attachment in message.attachments:
                    if any(attachment.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.webp', '.gif']):
                        image_bytes = await attachment.read()
                        mime_type = attachment.content_type or "image/jpeg"
                        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=mime_type))

                # Retry loop to handle temporary high demand or rate limits gracefully
                response = None
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        response = chat.send_message(contents)
                        break
                    except Exception as api_err:
                        if ("503" in str(api_err) or "429" in str(api_err)) and attempt < max_retries - 1:
                            await asyncio.sleep(2 * (attempt + 1))
                            continue
                        raise api_err

                if response and response.text:
                    await message.reply(response.text)
                
            except Exception as e:
                await message.channel.send(f"❌ Companion error: `{e}`")

async def setup(bot):
    await bot.add_cog(Companion(bot))
