#!/usr/bin/env python3
import requests
import re
from pyyamlconfig import load_config
import discord
import io
import aiohttp


BOT = discord.Client()
CFG = load_config('config.yaml')


# Helpers

def search(name: str) -> str:
    result = requests.get(f'https://classic.wowhead.com/search?q={name}#items')
    data = re.search(r'/item=(\d*)', result.text)
    if data is None:
        print(f"Could not find item for \"{name}\"")
    else:
        return data.group(1)


def image_link(item_id: str) -> str:
    return f"https://items.classicmaps.xyz/{item_id}.png"


# Events

@BOT.event
async def on_ready():
    """Print user information once logged in"""
    print('Logged in as')
    print(BOT.user.name)
    print(BOT.user.id)
    print('------')
    perms = discord.Permissions.none()
    perms.read_messages = True
    perms.send_messages = True
    print(
        discord.utils.oauth_url(CFG.get('clientid'),
                                permissions=perms),
    )


@BOT.event
async def on_message(message):
    """Handle on_message event"""
    data = re.findall(r'\[(.*?)\]', message.content)
    if data is not None:
        for text in data:
            async with aiohttp.ClientSession() as session:
                async with session.get(image_link(search(text))) as resp:
                    if resp.status == 200:
                        data = io.BytesIO(await resp.read())
                        await message.channel.send(file=discord.File(data, 'image.png'))


# Initialization of bot

BOT.run(CFG.get('token'))
