import os
import discord
from discord.ext import commands
from google import genai

class Companion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Initialize the official Google GenAI client (automatically grabs GEMINI_API_KEY from environment)
        self.client = genai.Client()
        
        # Persistent in-memory tracking per channel to maintain conversation history
        self.conversation_memory = {}

    @commands.command(name="chat", help="Chats with Yazoni's Right Hand using Gemini AI and persistent context memory.")
    async def chat(self, ctx, *, prompt: str):
        async with ctx.typing():
            try:
                channel_id = ctx.channel.id

                # Initialize history stack for this channel if it doesn't exist yet
                if channel_id not in self.conversation_memory:
                    self.conversation_memory[channel_id] = []

                # Append user prompt to memory
                self.conversation_memory[channel_id].append(f"User: {prompt}")

                # Keep history trimmed to the last 12 interactions to prevent token bloat
                if len(self.conversation_memory[channel_id]) > 12:
                    self.conversation_memory[channel_id] = self.conversation_memory[channel_id][-12:]

                # Compile conversation history context
                history_context = "\n".join(self.conversation_memory[channel_id])
                
                system_persona = (
                    "You are 'Yazoni's Right Hand', an elite, highly competent, sharp, and technical "
                    "AI companion. You have persistent memory of the ongoing conversation, assist with "
                    "development, and maintain a sharp, no-nonsense edge."
                )

                full_prompt = f"{system_persona}\n\nRecent Conversation:\n{history_context}\n\nAssistant:"

                # Generate response via google-genai SDK
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt
                )

                reply_text = response.text

                # Append assistant response back into memory
                self.conversation_memory[channel_id].append(f"Assistant: {reply_text}")

                # Handle Discord's 2000 character limit safely
                if len(reply_text) > 2000:
                    chunks = [reply_text[i:i+1900] for i in range(0, len(reply_text), 1900)]
                    for chunk in chunks:
                        await ctx.send(chunk)
                else:
                    await ctx.reply(reply_text)

            except Exception as e:
                await ctx.reply(f"Companion neural link error: `{e}`")

    @commands.command(name="clearmemory", help="Wipes the current channel's conversation memory.")
    async def clearmemory(self, ctx):
        channel_id = ctx.channel.id
        if channel_id in self.conversation_memory:
            del self.conversation_memory[channel_id]
            await ctx.reply("Memory wiped. Starting fresh.")
        else:
            await ctx.reply("No active memory found for this channel.")

async def setup(bot):
    await bot.add_cog(Companion(bot))
