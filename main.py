from Notetaker import notetaker as n
import constants as co
import emotes as e

import asyncio
import discord
import discord
from discord.utils import get

pre = '%'
client = discord.Client()
UDB = {}

@client.event
async def on_message(msg):
    cmd = msg.content
    chan = msg.channel
    user = msg.author.id
    if cmd.startswith(pre):
        cmd = cmd[1:]
        if not user in UDB:
            UDB[user] = n(user, msg.author.name)
        NOTES = UDB[user]
        if cmd.split()[0] in ['new', 'open']:
            args = cmd.split()[1:]
            if 0 < len(args) < 2:
                await client.send_message(chan, NOTES.open_context(args[0]))
            else:
                await client.send_message(chan, '{}Invalid arguments'.format(e.ERROR))
        elif cmd.startswith('topic'):
            exit_code = NOTES.write_to_context(co.TOPIC, data=cmd[6:])
            if exit_code == 0:
                await client.add_reaction(msg, '✅')
            else:
                await client.send_message(chan, exit_code)
        elif cmd.startswith('close'):
            await client.send_message(chan, NOTES.close_context())
        elif cmd.startswith('read'):
            await client.send_message(chan, NOTES.read_context(cmd.split()[1:]))
        elif cmd.startswith('delete'):
            args = cmd.split()[1:]
            if 0 < len(args) < 2:
                await client.send_message(chan, NOTES.delete(args[0]))
            else:
                await client.send_message(chan, '{}Invalid arguments'.format(e.ERROR))
        elif cmd.startswith('status'):
            current = NOTES.context
            if current is None:
                current = '{}No file is open'.format(e.INFO)
            else:
                current = 'Document: {}'.format(current.split(sep='/')[-1])
            await client.send_message(chan, current)
        elif cmd.startswith('ls'):
            await client.send_message(chan, NOTES.ls())
        elif cmd.startswith('undo'):
            await client.send_message(chan, NOTES.undo())
    elif chan.is_private and user in UDB:
        if cmd == '\\n':
            cmd = '\n'
        out = UDB[user].write_to_context(co.TXT, data=cmd)
        if out == 0:
            await client.add_reaction(msg, '✅')
        else:
            await client.send_message(chan, out)

try:
    with open('API.key', 'r') as key_file:
        API_KEY = str(key_file.read().replace('\n', ''))
    print('API Key loaded')
except:
    print('Failed to load API key')
    exit(1)

client.run(API_KEY)
