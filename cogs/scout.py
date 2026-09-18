import aiohttp
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

class Scout(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="scout")
    async def scout(self, ctx, url: str):
        """Scrapes and extracts clean text content from a URL."""
        async with ctx.typing():
            try:
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers, timeout=10) as response:
                        if response.status != 200:
                            await ctx.send(f"❌ Scout failed to reach URL. Status code: `{response.status}`")
                            return
                        
                        html = await response.text()
                
                # Parse text using BeautifulSoup
                soup = BeautifulSoup(html, "html.parser")
                
                for script in soup(["script", "style", "nav", "footer"]):
                    script.extract()
                    
                text = soup.get_text(separator="\n")
                lines = [line.strip() for line in text.splitlines() if line.strip()]
                clean_text = "\n".join(lines)
                
                if len(clean_text) > 1900:
                    clean_text = clean_text[:1900] + "\n[Content truncated...]"

                await ctx.send(f"🔍 **Scouted URL successfully (`{url}`):**\n```text\n{clean_text}\n```")
                
            except Exception as e:
                await ctx.send(f"❌ Scout error: `{e}`")

async def setup(bot):
    await bot.add_cog(Scout(bot))
