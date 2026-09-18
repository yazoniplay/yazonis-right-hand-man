import os
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
        """Generates an image based on a text prompt."""
        async with ctx.typing():
            try:
                # Using Imagen 3 or the appropriate image generation model via GenAI SDK
                result = self.client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        output_mime_type="image/jpeg",
                        aspect_ratio="1:1"
                    )
                )
                
                for generated_image in result.generated_images:
                    image_bytes = generated_image.image.image_bytes
                    # Send the image file back to Discord
                    file = discord.File(fp=BytesIO(image_bytes), filename="generated.jpg")
                    await ctx.send(f"🎨 **Generated for you:** `{prompt}`", file=file)
                    
            except Exception as e:
                await ctx.send(f"❌ Image generation error: `{e}`")

async def setup(bot):
    await bot.add_cog(Vision(bot))
