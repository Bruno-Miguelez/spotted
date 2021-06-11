<!DOCTYPE html>
<html lang="pt">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<h1 align="center">
    <a href="https://twitter.com/Spotted_do_tt">spotted</a>
</h1>
<p align="center">portal oficial do fogo no cu</p>

[![](https://img.shields.io/discord/794297088246153246?color=7289da&label=Discord&logo=Discord&style=for-the-badge)](https://discord.gg/fHaMSAKsg7)
[![](https://img.shields.io/github/license/apatacadof/spotted?logo=&style=for-the-badge)](https://raw.githubusercontent.com/apatacadof/spotted/7a1142bd2d2aef7e32b69a8038080377b415d953/LICENSE)
[![](https://img.shields.io/static/v1?label=pyhon&message=3.9&logo=python&color=informational&style=for-the-badge)](https://www.python.org/)
[![](https://img.shields.io/uptimerobot/status/m786806468-a734c9b76f9e14caac6270ec??label=bot%20status&style=for-the-badge)]()
[![](https://img.shields.io/uptimerobot/ratio/7/m786806468-a734c9b76f9e14caac6270ec??label=uptime%20last%207%20days&style=for-the-badge)]()
[![](https://img.shields.io/uptimerobot/ratio/m786806468-a734c9b76f9e14caac6270ec?label=uptime%20last%2030%20days&style=for-the-badge)]()


### CÓDIGO SPOTTED COMENTADO V2.1
```
'''
programa: spotted_do_tt v2.1 - estável
linguagem: python v3.8
autor: @Bruno_Miguelez_
versão: v2.1
'''
#IMPORTAR BIBILHOTECAS
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

#INFORMAÇÕES DE HORARIO
timeinfo_sp = datetime.now().astimezone(timezone('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M')
print(timeinfo_sp)

#AUTENTICAÇÃO DO BOT (TWITTER)
auth = tweepy.OAuthHandler((os.getenv('consumer_key')),(os.getenv('consumer_secret')))
auth.set_access_token((os.getenv('access_token')),(os.getenv('access_token_secret')))
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
client = discord.Client()

keep_alive()

#BOT DISCORD

@client.event #FUNÇÃO - QUANDO O BOT SE AUTENTICA
async def on_ready():
  print('We have logged in as {0.user}'.format(client)) #FALA SE DEU TUDO CERTO, INICIA A FUNÇÃO DO TWITTER, A PARTIR DA LINHA 111
  atualização_spotted.start()

@client.event
async def on_message(message): #QUANDO TEM ALGUMA MENSAGEM NO DISCORD
  msg = message.content

  if message.author.bot == True:
    if message.channel == client.get_channel(794467326660968459):
      if msg.startswith('spotted:'): #SE ESSA MENSAGEM FOR DO BOT(DO DISCORD), SE FOR NO CANAL DE SPOTTEDS, SE COMEÇAR COM "SPOTTED:" ELE ADICIONA AS OPÇÕES 
        await message.add_reaction("✔️")
        await message.add_reaction("🗣️")
        await message.add_reaction("❌")

  if message.author.bot == True:
    if message.channel == client.get_channel(794644643278487633): #MESMA COISA DA PARTE SUPERIOR, SÓ QUE PARA O CANAL DE DISCUSSÃO
      if msg.startswith('spotted:'):
        print("bot- foi pra discussão")
        await message.add_reaction("❌")
        await message.add_reaction("✔️")

    

@client.event
async def on_reaction_add(reaction, user): #FUNÇÃO PARA QUANDO ALGUM MODERADIR REAGE A MSG
  if user.bot == True:
    return
  else:
    messages = api.list_direct_messages()
    channel = reaction.message.channel
    content = reaction.message.content
    cemiterio_channel = client.get_channel(795441819902410842)
    discussão_channel = client.get_channel(794644643278487633)
    #for message in messages:
    if reaction.emoji == '❌': #SE A MSG FOR CANCELADA, REGISTRA AS INFORMAÇÕES E POSTA NO CANAL DE CEMITÉRIO
        print("❌")
        await channel.send("{} cancelou o envio do {}".format(user.name, reaction.message.content))
        print(content)
        await cemiterio_channel.send("spotted cancelado por {}, em {} \n {}".format(user.name, data_e_hora_sao_paulo_em_texto, reaction.message.content))
        print(content)
        await reaction.message.clear_reactions()
      
    if reaction.emoji == '✔️': #SE FOR APROVADA, PEGA O CONTEUDO DA MSG E POSTA NO TWITTER
        print("✔️")     
        await channel.send("{} aprovou o envio do {}".format(user.name, reaction.message.content))
        api.update_status(reaction.message.content)
        print(content)
        await reaction.message.clear_reactions()

    elif reaction.emoji == '🗣️': #SE FOR PRA DISCUSSÃO O BOT ENCAMINHA PRA UM CANAL ESPECIAL DO DISCORD, MARCA O @ DA EQUIPE E ABRE NOVAMENTE AS REAÇÕES(LINHA 67)
        print("🗣️")
        await channel.send("{} chamou reunião a respeito do {}".format(user.name, reaction.message.content))
        await discussão_channel.send("<@&794462660803821569>, {} acha melhor discutirmos esse {} \n \n votem quando chegarem em um consenso".format(user.name, reaction.message.content))
        await discussão_channel.send("{}".format(reaction.message.content))
        await reaction.message.clear_reactions()
        print(content)
    
    
#FECHOU DISCORD, DAQUI PARA BAIXO É TWITTER
@tasks.loop(seconds=100)
async def atualização_spotted():
    messages = api.list_direct_messages()
    desenvolvimento_channel = client.get_channel(794801047901831169)
    for message in messages: #SE TIVER MSG NA DM DO BOT NO TT
        spotted_channel = client.get_channel(794751006503469076)
        text = message.message_create["message_data"]["text"]
        id = message.message_create["sender_id"]
        spotted = f'spotted: {text}'

        if message.message_create["sender_id"] == "1299361275810586624": #SE A MSG FOR DO BOT, É UMA MSG AUTOMATICA, N TEM PQ ISSO SEGUIR PRA MODERAÇÃO, A MSG É DELETADA
          api.destroy_direct_message(message.id)

        elif len(spotted) >= 280: # MESMA COISA CASO A MSG TENHA MAIS DE 280 CARACTERES, LIMITE DO TT
          print("erro 02: mucho texto")
          privada_caracteres = "MENSAGEM AUTOMÁTICA \nseu spotted não pôde ser publicado por exeder o limite de caracteres"
          send = api.send_direct_message(message.message_create["sender_id"], privada_caracteres) #ELE ENVIA PARA O CANAL DE CEMITERIO DO DISCORD
          print("error 02: mucho texto")
          await cemiterio_channel.send("{} \n \n foi **cancelado** automaticamente por exceder o limite de 280 caracteres".format(message.message_create["message_data"]["text"]))

          api.destroy_direct_message(message.id) #E DELETA A MSG
        else:
          try: #SE A MSG TIVER ALGUM TIPO DE MIDIA, GIF, VIDEO, FOTO, A MSG É CANCELADA AUTOMATICAMENTE (NESSA VERSÃO, JA TEMOS BETAS COM SISTEMA DE MIDIA FUNCIONANDO)
            print(message.message_create["message_data"]["attachment"]["type"])
            print("é midia")
            send = api.send_direct_message(message.message_create["sender_id"],"MENSAGEM AUTOMÁTICA \narquivos de mídia ainda não são suportados, desculpe")
            api.destroy_direct_message(message.id)
          except:
            try:
              print("dentro do spotted") #PASSOU, A MSG VAI SER ENVIADA PARA A MODERAÇÃO
              api.destroy_direct_message(message.id) #E DELETADA
              await spotted_channel.send(spotted)
              print(message.message_create['message_data']['text'])
              print("deletado")

            except tweepy.TweepError as e: #INFORMAR CASO TENHA DADO ALGUM ERRO
              print(e.reason)
              await desenvolvimento_channel.send("error: {}".format(e.reason))
      else:
        print("nada bro") # SE NÃO TIVER MSG NA DM

#AUTENTICAÇÃO BOT DISCORD
client.run(os.getenv('token'))

#FECHOU O CODIGO, FML
```
### REGRAS E DIRETRIZES
Posts direcionados são os mais delicados, a equipe de moderação do spotted deve pausar o processo de publicação para consulta do citado.

Postagens que descumpram as diretrizes do twitter não serão publicadas no spotted. https://help.twitter.com/pt/rules-and-policies/twitter-rules

Destaca-se:
Segurança
Violência: não é permitido fazer ameaças de violência contra um indivíduo ou um grupo de pessoas. Também proibimos a glorificação da violência. Saiba mais sobre nossas políticas contra ameaças violentas e glorificação da violência. 
https://help.twitter.com/pt/rules-and-policies/violent-threats-glorification
https://help.twitter.com/pt/rules-and-policies/glorification-of-violence

Conduta de propagação de ódio: também não é permitido promover violência, ameaçar ou assediar outras pessoas com base em raça, etnia, nacionalidade, casta, orientação sexual, gênero, identidade de gênero, religião, idade, deficiência ou doença grave. Saiba mais. 
https://help.twitter.com/pt/rules-and-policies/hateful-conduct-policy

Abuso/assédio: não é permitido se envolver no assédio direcionado a alguém nem incitar outras pessoas a fazer isso, inclusive desejar que alguém sofra lesões. Saiba mais.
https://help.twitter.com/pt/rules-and-policies/abusive-behavior

Suicídio ou automutilação: não é permitido promover nem incentivar o suicídio ou a automutilação. Saiba mais.
https://help.twitter.com/pt/rules-and-policies/glorifying-self-harm

Privacidade
Informações privadas: não é permitido publicar informações privadas de outras pessoas (como número de telefone e endereço residencial) sem a permissão e a autorização expressas delas. Também é proibido ameaçar expor informações privadas ou incentivar outras pessoas a fazer isso. Saiba mais.
https://help.twitter.com/pt/rules-and-policies/personal-information
