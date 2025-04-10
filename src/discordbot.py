import discord
from discord.ext import commands
import logging


intents = discord.Intents.default() # default intents
intents.guilds          = True
intents.message_content = True # Enable message content intent
intents.members         = True # Enable server member intent (for member join/leave events)
intents.presences       = True # Enable presence intent (for status changes like online/offline)
intents.messages        = True
BOT = commands.Bot(command_prefix="/", intents=intents, help_command=None)

async def bot_add_slashcommands(bot_instance: commands.Bot):
    from src.misc_commands import ping_slash
    from src.main import banbot

    bot = bot_instance
    bot.tree.add_command(ping_slash)
    bot.tree.add_command(banbot)


async def tree_sync():
    await BOT.tree.sync()
    logging.info("Slash commands synced")

@BOT.event
async def on_connect():
    await bot_add_slashcommands(BOT)

@BOT.event
async def on_ready():
    logging.info(f"Logged in as {BOT.user} ({BOT.user.id})")
    await tree_sync()
    logging.info("Bot ready.")
