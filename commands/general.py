import discord
from discord.ext import commands

class FortyTwoBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Reconnect
    @commands.Cog.listener()
    async def on_resumed(self):
        print('Bot has reconnected!')
        await self.bot.change_presence(activity=discord.Game(name="with c"))
        
    # Error Handlers
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Unknown command
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(title = "⛔️ Command not found!", description = "**!friends** • Shows status of your friends\n**!addfriend <intra_id>** • Add a friend\n**!remfriend <intra_id>** • Remove a friend", color = 15158332)
            await ctx.send(embed=embed)

        # Bot does not have permission
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(':no_entry:Bot Permission Missing!')
        elif isinstance(error, commands.MissingAnyRole):
            await ctx.send(":no_entry: You don't have permission to use this command!")
          
async def setup(bot):
  await bot.add_cog(FortyTwoBot(bot))