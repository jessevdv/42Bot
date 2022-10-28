import os
import asyncio
import discord
from discord.ext import commands



# Discord Bot Token
my_secret = os.environ['token']

class CodamBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents(messages=True, guilds=True, members=True, message_content=True)
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)

    async def on_ready(self):
      print(f'⚡️⚡️⚡️ Logged in as {self.user} (ID: {self.user.id})')
      print('------')

bot = CodamBot()

async def load():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await bot.load_extension(f'commands.{filename[: -3]}')
          
async def main():
  await load()
  await bot.start(my_secret, reconnect=True)

try:
  asyncio.run(main())
except:
  os.system('kill 1')
