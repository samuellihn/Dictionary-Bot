import os

import discord
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv
import asyncio
import re
from PyDictionary import PyDictionary
from datetime import datetime


load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

client = discord.Client()
prefix = "!d "
bot = Bot(command_prefix="!d ")

dictionary = PyDictionary()

words_file = "20k.txt"
with open(words_file) as words_list:
    common_words = words_list.read().splitlines()
commons = set(common_words)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.change_presence(status=discord.Status.online)


@bot.event
async def on_message(message: discord.Message):
    await bot.process_commands(message)
    message_words = re.split("\W+", message.content)

    role = discord.utils.get(message.guild.roles, name="Dictionary")
    if not role in message.author.roles: return
    to_send = False
    em = Embed(title="Difficult Words")

    for word in message_words:
        word = word.lower()
        if word not in commons:
            to_send = True
            definition = dictionary.meaning(word)
            try:
                text = ""
                for de in definition.items():
                    text += f"**{de[0]}:**\n"
                    for subdef in de[1]:
                        text += " - " + subdef.capitalize() + "\n"
                em.add_field(name=word.capitalize(), value=text)
            except AttributeError:
                pass
    if to_send:
        chan = message.channel
        await chan.send(embed=em)




@bot.command(name="add")
async def adduser(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Dictionary")
    if role is None:
        role = await ctx.guild.create_role(name="Dictionary")
    await user.add_roles(role)
    await ctx.send(f"{user.mention} has been added to the dictionary list")


bot.run(DISCORD_TOKEN)
