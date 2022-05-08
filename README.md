Classic Items Discord bot
=========================

A bot for linking items from Classic World of Warcraft in Discord.

Any message with "[item name]" will be searched in wowhead, the first item will be added as an image. To specify classic era, use "[item name](c)". If no suffix is used, the current expansion data is assumed.

Images are originally from the zip file found at https://items.classicmaps.xyz/

TBC images are generated by me.


Installation
============
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

Run
===
Get a token and client id by registering a bot at https://discord.com/developers/applications
Add them to config.yaml
venv/bin/python3 classicbot.py
