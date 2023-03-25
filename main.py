import discord
import os
import requests
from io import BytesIO
import pytesseract
from PIL import Image

# Set up the IDs for the Discord server, role, and channel, and the YouTube channel
discord_server_id = 1087640802446032968 # Replace with the ID of your Discord server
verified_role_id = 1087640834196910123 # Replace with the ID of your verified role
discord_channel_id = 1088082273880002581 # Replace with the ID of your Discord channel
youtube_channel_name = "Dungeon Playz" # Replace with the name of your YouTube channel
youtube_api_key = "AIzaSyBgWSH0atAopEb69V23RjTbTey" # Replace with your YouTube API key

intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    channel = client.get_channel(discord_channel_id)
    await channel.send("I am there to verify you people! Just subscribe to Dungeon Playz Channel and send screenshot and get verified.")
    activity = discord.Activity(type=discord.ActivityType.watching, name="Dungeon Playz")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Bot is ready.")

@client.event
async def on_message(message):
    if message.channel.id == discord_channel_id:
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.endswith(".png") or attachment.filename.endswith(".jpg") or attachment.filename.endswith(".jpeg"):
                    image_url = attachment.url
                    response = requests.get(image_url)
                    img = Image.open(BytesIO(response.content))
                    text = pytesseract.image_to_string(img)
                    if youtube_channel_name.lower() in text.lower():
                        role = message.guild.get_role(verified_role_id)
                        await message.author.add_roles(role)
                        await message.add_reaction("✅")
                        await message.channel.send(f"{message.author.mention}, you have been verified!")
                    else:
                        await message.add_reaction("❌")
                        await message.channel.send(f"{message.author.mention}, verification failed. Please ensure that the screenshot includes your subscription to the YouTube channel.")
                    break

client.run("MTA4ODQyNDE1MDQ3NDk1MjcxNQ.GT8OUO.")
