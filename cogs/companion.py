import os
import discord
from discord.ext import commands
from google import genai

class Companion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Initialize the official Google GenAI SDK client
        # It automatically looks for GEMINI_API_KEY in environment variables
        self.client = genai.Client()
        
        # Simple in-memory conversation log per channel/session
        self.conversation_memory = []

    @commands.command(name="chat")
    async def chat(self, ctx, *, prompt: str):
        """Talks to Yazoni's Right Hand using memory-backed chat."""
        # Show typing indicator while talking to Gemini
        async with ctx.typing():
            try:
                # Append user message to history
                self.conversation_memory.append(f"User: {prompt}")
                
                # Keep history trimmed to avoid token bloat (last 10 interactions)
                if len(self.conversation_memory) > 20:
                    self.conversation_memory = self.conversation_memory[-20:]
                
                # Build context block
                full_prompt = (
                    "You are Yazoni's Right Hand, a 24/7 AI-powered Discord companion "
                    "helping with server architecture, coding, and general tasks.\n\n"
                    "Conversation History:\n" + "\n".join(self.conversation_memory) + "\nAI:"
                )

                # Generate response via google-genai SDK using gemini-3.5-flash-lite
                response = self.client.models.generate_content(
                    model='gemini-3.5-flash-lite',
                    contents=full_prompt
                )
                
                reply_text = response.text.strip()
                
                # Append AI response to history
                self.conversation_memory.append(f"AI: {reply_text}")

                # Discord has a 2000 character limit per message; split if needed
                if len(reply_text) > 2000:
                    for i in range(0, len(reply_text), 2000):
                        await ctx.send(reply_text[i:i+2000])
                else:
                    await ctx.send(reply_text)

            except Exception as e:
                await ctx.send(f"Companion neural link error: `{e}`")

async def setup(bot):
    await bot.add_cog(Companion(bot))
