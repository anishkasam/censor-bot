import discord
import os
import requests
import random
from replit import db
from run import keep_running

client = discord.Client()

censoredwords = ["fuck", "bitch", "shit", "ass", "nigga"]
censoring = True

def update_censoredwords(word):
  if word in censoredwords:
    return
  else:
    censoredwords.append(word)

def delete_censoredword(word):
  if word in censoredwords:
    censoredwords.remove(word)
  else:
    return

@client.event
async def on_ready():
  print("Logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  global censoring
  global censoredwords
  if message.author == client.user:
    return

  msg = message.content.lower()

  if msg.startswith("-") == False and censoring is True:
    if any(word in msg for word in censoredwords):
      await message.delete()
  
  if msg.startswith("-hello") or msg.startswith("-hi"):
    await message.channel.send("Hello! Type -help to see all the available commands.")

  if msg.startswith("-add"):
    word = msg.split("-add ", 1)[1]
    update_censoredwords(word)
    await message.channel.send("Word was added to list of censored words.")

  if msg.startswith("-remove"):
    word = msg.split("-remove ", 1)[1]
    delete_censoredword(word)
    await message.channel.send("Word was removed from list of censored words.")

  if msg.startswith("-list"):
    await message.channel.send(censoredwords)

  if msg.startswith("-toggle"):
    if censoring == True:
      censoring = False
      await message.channel.send("Censor Bot has stopped censoring.")
    elif censoring == False:
      censoring = True
      await message.channel.send("Censor Bot has started censoring.")

  if msg.startswith("-clear"):
    censoredwords = []
    await message.channel.send("All words were removed from the list of censored words.")

  if msg.startswith("-help"):
    await message.channel.send("-add: you can add a word to the list of censored words \n-remove: you can remove a word from the list of censored words \n-toggle: you can toggle whether or not the bot is censoring \n-list: lists all the words that are currently being censored \n-clear: clear all words from the list of censored words")

keep_running()  
client.run(os.getenv("TOKEN"))
