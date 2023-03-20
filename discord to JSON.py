import discord
import json
import sys
import os
import re

client = discord.Client()

### CONFIG ###
token=""
channelid = 0
### END CONFIG ###
if channelid == 0:
    channelid = int(input("input id>>>"))
@client.event
async def on_ready():
    isGroup = False
    selectedchannel = None
    recipientname = ''
    groupname = ''
    for recent in client.private_channels:
        if str(type(recent)) == "<class 'discord.channel.DMChannel'>":
            if recent.recipient.id == channelid:
                selectedchannel = recent
                print(f"Found DM channel with id {channelid} and name {recent.recipient.name}")
                recipientname = recent.recipient.name

        elif str(type(recent)) == "<class 'discord.channel.GroupChannel'>":
            if recent.id == channelid:    
                selectedchannel = recent
                isGroup = True
                print(f"Found Group channel with id {channelid}")
                if recent.name:
                    print(f"and the name: {recent.name}")
                    groupname = recent.name
    if selectedchannel:
        data = {"users": {}, "messages":[]}
        async for message in selectedchannel.history(limit=None):
            messagedata = {"content": message.content, "user":{"id": message.author.id, "name": message.author.name, "discriminator": message.author.discriminator}}
            if message.author.id not in data["users"]:
                data["users"][str(message.author.id)] = {"name": message.author.name, "discriminator": message.author.discriminator}
                if message.author.avatar_url:
                    data["users"][str(message.author.id)]["avatar_url"] = str(message.author.avatar_url)
            if message.author.avatar_url:
                messagedata["user"]["avatar_url"] = str(message.author.avatar_url)
            attachment_urls = []
            if len(message.attachments):
                for attachment in message.attachments:
                    attachment_urls.append(attachment.url)
            messagedata["attachment_urls"] = attachment_urls
            if message.reference:
                messagedata["reply_id"] = message.reference.message_id
            if message.edited_at:
                messagedata["edited_at"] = message.edited_at.timestamp()
            if message.pinned:
                messagedata["pinned"] = True
            messagedata["created_at"] = message.created_at.timestamp()
            data["messages"].append(messagedata)
        if isGroup and groupname:
            if check_string(groupname):
                filename = os.path.dirname(__file__) + "\\" + groupname + ".json"
            else:
                filename = os.path.dirname(__file__) + "\\" + str(channelid) + ".json"
        elif not isGroup and recipientname:
            if check_string(recipientname):
                filename = os.path.dirname(__file__) + "\\" + recipientname + ".json"
            else:
                print(recipientname)
                filename = os.path.dirname(__file__) + "\\" + str(channelid) + ".json"
        else:
            filename = os.path.dirname(__file__) + "\\" + str(channelid) + ".json"
        data["messages"] = data["messages"][::-1]
        open(filename, "w+").write(json.dumps(data))
        print(f"FIle has been saved to: {filename}, shutting down")
    os.system(f"taskkill /pid {os.getpid()} /f")
                
def check_string(filename):
    if not filename:
        return False
    invalid_chars = re.compile(r'[\\/:*?"<>|]')
    if invalid_chars.search(filename):
        return False
    if filename.startswith('.') or filename.endswith('.'):
        return False
    return True
client.run(token, bot=False)