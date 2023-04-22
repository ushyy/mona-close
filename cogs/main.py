
import discord
from discord.ext import commands

class main(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):

        await self.client.change_presence(status = discord.Status.dnd,
                                          activity = discord.Activity(type = discord.ActivityType.watching, name = 'за Mona - /menu для информации'))

        print('\n------------------------------')
        print('ㅤ ㅤ connection in as:\nㅤ{0.user.name} : {0.user.id}'.format(self.client))
        print('------------------------------\n')
    
async def setup(client):
    await client.add_cog(main(client))