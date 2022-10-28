import discord
from discord.ext import commands
from utils import IntraAPI

intra_api = IntraAPI()

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx: commands.Context, intra_id: str):
      res = intra_api.request(f"/users/{intra_id}")
      data = res.json()
      rc = res.status_code
      if rc == 200:
        print(data)
        name = data["usual_full_name"]
        intra_url = data["url"]
        kind = data["kind"]
        image = data["image_url"]
        eval_points = data["correction_point"]
        piscine_month = data["pool_month"]
        piscine_year = data["pool_year"]
        country = data["campus"][0]["country"]
        city = data["campus"][0]["city"]
        
        if not data["location"]:
          location = "`🔴 Offline`"
        else:
          location = f"`🟢 [{location[0:7]}]`"

        color = discord.Colour.from_str("#12E2E6")
        embed = discord.Embed(title=f"{name} • {kind}", color=color)
        embed.add_field(name="Eval Points", value = eval_points)
        embed.add_field(name="Campus", value=f"{city}, {country}")
        embed.add_field(name="Piscine", value=f"{piscine_month}, {piscine_year}")
        embed.add_field(name="Location", value=f"{location}")
        embed.set_author(name="Intra Profile", url=intra_url, icon_url="https://42.fr/wp-content/uploads/2021/08/42.jpg")
        embed.set_thumbnail(url=image)

        await ctx.send(embed=embed)
        
async def setup(bot):
  await bot.add_cog(UserInfo(bot))