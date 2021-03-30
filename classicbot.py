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

def search(name: str, expansion: str="classic") -> str:
    result = requests.get(f'https://{expansion}.wowhead.com/search?q={name}#items')
    data = re.search(r'/item=(\d*)', result.text)
    if data is None:
        print(f"Could not find item for \"{name}\"")
    else:
        return data.group(1)


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
    data = re.findall(r'\[(.*?)\](\((c|t)\))?', message.content)
    if data is not None:
        for text in data:
            searchterm, _, expansion = text
            item = search(searchterm, expansion)
            if item is None:
                await message.channel.send(f'Could not find "{searchterm}"')
                continue
            expansion = "tbc" if expansion == "t" else "classic"
            try:
                await message.channel.send(f'<https://{expansion}.wowhead.com/item={item}>', file=discord.File(f'items/{expansion}/{item}.png'))
            except FileNotFoundError:
                await message.channel.send(f'Could not find image for "{item}" in {expansion}')


# Initialization of bot

BOT.run(CFG.get('token'))
