'''
programa: spotted_do_tt
linguagem: python v3.8
autor: @Bruno_Miguelez_
versão: v2.0
destaque: equipe de moderação
'''
import tweepy
import time
import os
from keep_alive import keep_alive
import discord
from discord import Webhook, RequestsWebhookAdapter
import requests
from dhooks import Webhook
from datetime import datetime
from pytz import timezone
from discord.ext import tasks, commands

data_e_hora_atuais = datetime.now()
fuso_horario = timezone('America/Sao_Paulo')
data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime('%d/%m/%Y %H:%M')

print(data_e_hora_sao_paulo_em_texto)


auth = tweepy.OAuthHandler((os.getenv('consumer_key')),
                           (os.getenv('consumer_secret')))
auth.set_access_token((os.getenv('access_token')),
                      (os.getenv('access_token_secret')))
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
client = discord.Client()
hook = Webhook((os.getenv('webhook_url')))


keep_alive()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  atualização_spotted.start()

@client.event
async def on_message(message):
  msg = message.content

  if message.author.bot == True:
    if message.channel == client.get_channel(794467326660968459):
      if msg.startswith('spotted:'):
        await message.add_reaction("✔️")
        await message.add_reaction("🗣️")
        await message.add_reaction("❌")

  if message.author.bot == True:
    if message.channel == client.get_channel(794644643278487633):
      if msg.startswith('spotted:'):
        print("bot- foi pra discussão")
        await message.add_reaction("❌")
        await message.add_reaction("✔️")

    

@client.event
async def on_reaction_add(reaction, user):
  if user.bot == True:
    return
  else:
    messages = api.list_direct_messages()
    channel = reaction.message.channel
    content = reaction.message.content
    cemiterio_channel = client.get_channel(795441819902410842)
    discussão_channel = client.get_channel(794644643278487633)
    #for message in messages:
    if reaction.emoji == '❌':
        print("❌")
        await channel.send("{} cancelou o envio do {}".format(user.name, reaction.message.content))
        print(content)
        await cemiterio_channel.send("spotted cancelado por {}, em {} \n {}".format(user.name, data_e_hora_sao_paulo_em_texto, reaction.message.content))
        print(content)
        await reaction.message.clear_reactions()
      
    if reaction.emoji == '✔️':
        print("✔️")     
        await channel.send("{} aprovou o envio do {}".format(user.name, reaction.message.content))
        api.update_status(reaction.message.content)
        print(content)
        await reaction.message.clear_reactions()

    elif reaction.emoji == '🗣️':
        print("🗣️")
        await channel.send("{} chamou reunião a respeito do {}".format(user.name, reaction.message.content))
        await discussão_channel.send("<@&794462660803821569>, {} acha melhor discutirmos esse {} \n \n votem quando chegarem num consenso".format(user.name, reaction.message.content))
        await discussão_channel.send("{}".format(reaction.message.content))
        await reaction.message.clear_reactions()
        print(content)
    
@tasks.loop(seconds=100)
async def atualização_spotted():
    messages = api.list_direct_messages()
    desenvolvimento_channel = client.get_channel(794801047901831169)
    for message in messages:
        try:
            print(message.message_create['message_data']['text'])
            text = message.message_create["message_data"]["text"]  
            data = (f'spotted: {text}')
            hook.send(data)
            api.destroy_direct_message(message.id)
            print("deletado")
        except tweepy.TweepError as e:
            print(e.reason)
            await desenvolvimento_channel.send("error: ".format(e.reason))
    else:
        print("nada bro")

client.run(os.getenv('token'))
