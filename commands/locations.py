from utils import IntraAPI
from discord.ext import commands

intra_api = IntraAPI()

class locations(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command()
  async def locations(self, ctx: commands.Context):
    map = "-------------------------\n"
    for j in range(12):
      map += "| "
      for i in range(6):
        if i == 3:
          map += "    "
        if j == 1 and i == 1:
          map += "•"
        else:
          map += "◦"
      map += " |\n"
    map += "--------------"
    await ctx.send(f"""```{map}```""")

async def setup(bot):
  await bot.add_cog(locations(bot))