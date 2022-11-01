import discord
from discord.ext import commands
import time

from utils import IntraAPI, connectMongo
from commands.views import DeleteData

intra_api = IntraAPI()
users = connectMongo("Users")

class friends(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  ## SHOWS LIST OF ONLINE FRIENDS ##
  @commands.command()
  async def friends(self, ctx: commands.Context):
    user_id = str(ctx.author.id)
    color = discord.Colour.from_str("#FCEC03")
    color_err = discord.Colour.from_str("#FC0303")

    ## LOADING/ERROR EMBED ##
    loading_embed = discord.Embed(title = "**Searching for friends...**", color=color)
    error_embed = discord.Embed(title = "**An error occured!**", color=color_err)
    message = await ctx.reply(embed=loading_embed)

    ## GET USER FROM DB##
    user = users.find_one({"_id": user_id})
    
    if user is not None:
      friendlist = user["friends"]
      if len(friendlist) > 0:
        try:
          embed = discord.Embed(title=f"**⚡️ My Friends** • `({len(friendlist)}/25)`", color = color)
          ## GET ONLINE FRIENDS ##
          for friend in friendlist:
            res = intra_api.request(f"users/{friend}")
            data = res.json()
            if res.status_code == 429:
              await message.delete()
              await ctx.reply(f"Rate limit exceeded - Please wait {res.headers['Retry-After']}s")
            location = data["location"]
            name = data["first_name"]
            if not location:
              location = "`🔴 Offline`"
            else:
              location = f"`🟢 [{location[0:7]}]`"
            embed.add_field(name=name, value=location)      

          embed.set_footer(text=f"{ctx.author}'s friends")
          await message.edit(embed=embed)
        except:
          await message.edit(embed = error_embed)
      else:
        embed = discord.Embed(title="🥲 **You don't have any friends...**", description="Add one with the command **!addfriend <intra_id>**", color=color_err)
        await message.edit(embed=embed)
    else:
      embed = discord.Embed(title="🥲 **You don't have any friends...**", description="Add one with the command **!addfriend <intra_id>**", color=color_err)
      await message.edit(embed=embed)
      
  @commands.command()
  async def addfriend(self, ctx: commands.Context, friend: str):  
    user_id = str(ctx.author.id)
    user = users.find_one({"_id": user_id})
    message = await ctx.reply("`⏳` Loading...")
    
    res = intra_api.request(f"users/{friend}")
    if res.status_code == 200:
      if friend is None:
        await message.edit(content="⚠️ Please specify which friend you want to add!")
      else:
        if user is None:
          users.insert_one({"_id" : user_id, "friends" : [], "timestamp":time.time()})
          users.update_one({"_id" : user_id}, {"$push": {"friends": friend}})
          await message.edit(content=f"✅Welcome {ctx.author}! Your first friend has been **added** succesfully!")
        if len(user["friends"]) < 25:
          if friend not in user["friends"]:
            users.update_one({"_id" : user_id}, {"$push": {"friends": friend}})
            await message.edit(content="✅ Friend **added** succesfully!")
          else:
            await message.edit(content="⚠️ You can't be friends twice with the same person!")
        else:
          await message.edit(content="⚠️ Friend limit reached, you have to many friends (max 25).")
    else:
      await message.edit(content="⚠️ Thats not a valid intra_id please try again!")

  @commands.command()
  async def remfriend(self, ctx: commands.Context, friend: str):  
    user_id = str(ctx.author.id)
    user = users.find_one({"_id": user_id})

    message = await ctx.reply("`⏳` Loading...")
    
    if friend is None:
      await message.edit(content="⚠️ Please specify which friend you want to remove!")
    else:        
      if user is None:
        await message.edit(content="⚠️ How can you remove a friend if you don't have any to begin with? Add one with Add one with the command **!addfriend <intra_id>**")
      if friend in user["friends"]:
        users.update_one({"_id" : user_id}, {"$pull": {"friends": friend}})
        await message.edit(content="✅ Friend **removed** succesfully!")
      else:
        await message.edit(content="⚠️ You can't remove a friend who is not your friend!")

  @commands.command()
  async def delete(self, ctx: commands.Context):
    deleteview = DeleteData()
    color_err = discord.Colour.from_str("#FC0303")
    embed = discord.Embed(description="You are about to delete your data from the database, press **Delete** if you wish to proceed.", color=color_err)
    deleteview.user_id = str(ctx.author.id)
    await ctx.send(embed=embed, view=deleteview)
    
  @commands.command()
  async def friendmap(self, ctx: commands.Context):  
    print()
      
async def setup(bot):
  await bot.add_cog(friends(bot))