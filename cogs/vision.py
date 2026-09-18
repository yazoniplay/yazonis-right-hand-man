import os
from io import BytesIO
import discord
from discord.ext import commands
from google import genai
from google.genai import types

class Vision(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    @commands.command(name="image", aliases=["draw", "imagine"])
    async def image(self, ctx, *, prompt: str):
        """Generates an image using Gemini's image output modality."""
        async with ctx.typing():
            try:
                # Use gemini-2.5-flash-image with IMAGE response modality
                response = self.client.models.generate_content(
                    model='gemini-2.5-flash-image',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_modalities=["IMAGE"],
                        image_config=types.ImageConfig(
                            aspect_ratio="1:1",
                        ),
                    ),
                )
                
                image_found = False
                for part in response.parts:
                    if part.inline_data:
                        image_bytes = part.inline_data.data
                        file = discord.File(fp=BytesIO(image_bytes), filename="generated.jpg")
                        await ctx.send(f"🎨 **Generated for you:** `{prompt}`", file=file)
                        image_found = True
                        break
                
                if not image_found:
                    await ctx.send("❌ The model didn't return an image for that prompt.")
                    
            except Exception as e:
                await ctx.send(f"❌ Image generation error: `{e}`")

async def setup(bot):
    await bot.add_cog(Vision(bot))
