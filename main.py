from Notetaker import notetaker as n
import constants as co
import emotes as e

import asyncio
import discord

pre = '"'
client = discord.Client()
UDB = {}

@client.event
async def on_message(msg):
    cmd = msg.content
    chan = msg.channel
    user = msg.author.id
    if cmd.startswith(pre) and chan.is_private:
        cmd = cmd[1:]
        if not user in UDB:
            UDB[user] = n(user, msg.author.name)
        NOTES = UDB[user]
        if cmd.split()[0] in ['new', 'open']:
            args = cmd.split()[1:]
            if 0 < len(args) < 2:
                client.send_message(chan, NOTES.open_context(args[0]))
            else:
                client.send_message(chan, '{}Invalid arguments'.format(e.ERROR))
        elif cmd.startswith('topic'):
            exit_code = NOTES.write_to_context(co.TOPIC, data=cmd[6:])
            if exit_code == 0:
                client.add_reaction(msg, ':white_check_mark:')
            else:
                client.send_message(chan, exit_code)
        elif cmd.startswith('close'):
            client.send_message(chan, NOTES.close_context())
        elif cmd.startswith('delete'):
            args = cmd.split()[1:]
            if 0 < len(args) < 2:
                client.send_message(chan, NOTES.delete(args[0]))
            else:
                client.send_message(chan, '{}Invalid arguments'.format(e.ERROR))
        elif cmd.startswith('status'):
            current = NOTES.context
            if current is None:
                current = '{}No file is open'.format(e.INFO)
            else:
                current = current.split(sep='/')[-1]
            client.send_message(chan, current)
        elif cmd.startswith('ls'):
            client.send_message(chan, NOTES.ls())
        elif cmd.startswith('undo'):
            client.send_message(chan, NOTES.undo())

try:
    with open('API.key', 'r') as key_file:
        API_KEY = str(key_file.read().replace('\n', ''))
    print('API Key loaded')
except:
    print('Failed to load API key')
    exit(1)

client.run(API_KEY)
