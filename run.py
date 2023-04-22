
import discord
from discord.ext import commands

import dotenv
from dotenv import load_dotenv
load_dotenv()

import os

import asyncio

client = commands.Bot(os.getenv('PREFIX'), intents = discord.Intents.all())

async def load_cogs():

    for cogs in os.listdir('cogs'):

        if cogs.endswith('.py'):
            await client.load_extension(f'cogs.{cogs[:-3]}')
    
async def run():

    async with client:
        await load_cogs()
        await client.start(os.getenv('API-TOKEN'))

asyncio.run(run())