import os
import discord
from discord.ext import commands
from google import genai
from google.genai import types

class Research(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    @commands.command(name="research", aliases=["search", "google"])
    async def research(self, ctx, *, query: str):
        """Searches the live internet autonomously using Google Search grounding."""
        async with ctx.typing():
            try:
                # Ask Gemini with Google Search tool enabled
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=query,
                    config=types.GenerateContentConfig(
                        tools=[types.Tool(google_search=types.GoogleSearch())],
                        system_instruction="You are a deep research assistant. Find accurate, up-to-date info from the web and present it clearly."
                    ),
                )
                
                answer = response.text
                if len(answer) > 1900:
                    answer = answer[:1900] + "\n[Content truncated...]"

                await ctx.send(f"🌐 **Research Results for:** `{query}`\n\n{answer}")
                
            except Exception as e:
                await ctx.send(f"❌ Research error: `{e}`")

async def setup(bot):
    await bot.add_cog(Research(bot))
