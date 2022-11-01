import discord
import uuid
from utils import connectMongo

users = connectMongo("Users")

class DeleteData(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.user_id = None

    @discord.ui.button(label='Delete', style=discord.ButtonStyle.red, custom_id=str(uuid.uuid1()))
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
      if self.user_id == str(interaction.user.id):
        try:
          users.delete_one({"_id": self.user_id})
          await interaction.response.send_message("✅ Your data has been **removed** from the database succesfully!")
        except:
          await interaction.response.send_message("⚠️ Something went wrong here, make sure you even have data stored and try again!")
        self.stop()
        
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.green, custom_id=str(uuid.uuid1()))
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
      if self.user_id == str(interaction.user.id):
        await interaction.response.send_message("Glad that you stayed!")
        self.stop()

async def setup(bot):
  bot.add_view(DeleteData())