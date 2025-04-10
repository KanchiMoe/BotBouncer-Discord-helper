import discord
from discord import app_commands
from src.discordbot import BOT

#/ping
@app_commands.command(name="ping", description="Ping")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message(":stopwatch: | pong!")