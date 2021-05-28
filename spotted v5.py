-----------------------------
'''program info'''

'''
programa: spotted_v5
linguagem: python v3.9
autores: Bruno Miguelez, Allan, Pedro Miguelez
versão: v5.9

destaques da versão 5: novas funções moderação- consulta citado automática, tw, confirmação apoio (msg autodepressiativas)
especificidades do 5.9: formulario de contato(?ajuda), otimizações no ranking dos moderadores(criação de função para adicionar pontos), correção de bug ao exibir dados armazenados no banco de dados(&gt; &lt; > <)
'''
-----------------------------


-----------------------------
'''import section'''
import tweepy
import time
import os
from keep_alive import keep_alive
import discord
import requests
from datetime import datetime
from pytz import timezone
from discord.ext import tasks, commands
from discord.utils import get
from discord.ext.tasks import loop
from discord.ext.commands import Bot
import sqlite3
import re
from moviepy.editor import *
from requests_oauthlib import OAuth1
from twython import Twython, TwythonError
import requests as req
import mysql.connector
import asyncio
-----------------------------


-----------------------------
'''configuration'''
BEARER = ""
APP_KEY = ""
APP_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""

DISCORD_TOKEN = ""
-----------------------------


-----------------------------
'''spotted v5.9'''
auth = tweepy.OAuthHandler(APP_KEY,APP_SECRET)
auth.set_access_token(OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
auth2 = OAuth1(APP_KEY,APP_SECRET,OAUTH_TOKEN,OAUTH_TOKEN_SECRET)
try:
  api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
except tweepy.RateLimitError as e:
  print(e)
  print(e.reason)
client = discord.Client()
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

banco = sqlite3.connect('database.db')

cursor = banco.cursor()

cursor.execute("SELECT spotted FROM data")
print(cursor.fetchall())

cursor.execute("SELECT destinatario,ce,contagem FROM CE")
print(cursor.fetchall())


cursor.execute("SELECT * FROM ranking")
print(cursor.fetchall())


print(timeinfo_sp)

class classe:
  @client.event
  async def on_ready():
    timeinfo_sp = datetime.now().astimezone(timezone('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M')
    desenvolvimento_channel = client.get_channel(794801047901831169)
    print('We have logged in as {0.user}'.format(client))
    try:
      classe.atualização_spotted.start()
    except RuntimeError as e:
      await desenvolvimento_channel.send("error: {}".format(e))
      print(e)
      return

  @client.event
  async def on_message(message):
    timeinfo_sp = datetime.now().astimezone(timezone('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M')
    msg = message.content
    aprovado_channel = client.get_channel(815727445126152223)
    desenvolvimento_channel = client.get_channel(794801047901831169)
    log_contato_channel = client.get_channel(839324301752401960)
    if msg.startswith('s-') or msg.startswith('S-'):
      try:
        print(msg)
        comando = msg.split(" ", 2)
        print(comando)
        contagem = comando[0].upper()
        cursor.execute("SELECT * FROM data WHERE contagem = ('" + contagem + "')")
        for row in cursor:
          print(row[0])
          content = row[0]
        print(contagem)
        if comando[1] == "tw":
          print("gatilho")
          #print(cursor.fetchall())
          cursor.execute("SELECT * FROM data WHERE contagem = ('" + contagem + "')")
          for row in cursor:
            string_row = row[0]
            for i in "&gt;":
              string_row = string_row.replace("&gt;", ">")
            for i in "&lt;":
              string_row = string_row.replace("&lt;", "<")

            print(row[0])
            content = row[0]
            api.update_status("tw // {}".format(comando[2]))
            last_tweet = api.user_timeline(id=1291744051193171969,count=1)[0]
            res = api.update_status(string_row, in_reply_to_status_id=last_tweet.id, auto_populate_reply_metadata=True)
            api.send_direct_message(row[1],"https://twitter.com/Spotted_do_tt/status/{}".format(last_tweet.id))
            await message.channel.send("o {} \n** foi aprovado** as {}".format(content, timeinfo_sp))
            await aprovado_channel.send("**aprovado** o envio do {}\nhttps://twitter.com/Spotted_do_tt/status/{}".format(content, last_tweet.id))
            cursor.execute("UPDATE data SET id = 'None' WHERE spotted = '" + content + "'")
            cursor.execute("UPDATE data SET envio=? WHERE spotted=?", (timeinfo_sp,content))
            banco.commit()
            await message.delete()

        elif comando[1] == "citado":
          print("citado")
          cursor.execute("SELECT * FROM data WHERE contagem = ('" + contagem + "')")
          for row in cursor:
            print(row[0])
            content = row[0]
            user_citado = api.get_user(comando[2])
            msg_citado = ""
            api.send_direct_message(user_citado.id,"MENSAGEM AUTOMATIZADA\n~consulta citado~\n\nEssa é uma mensagem de consulta automática, recebemos um spotted e achamos melhor você dar a palavra final.\n\n{}\n\nse achar suave postar digite:\n{} posta\ne o spotted será postado\n\nou se você se sente desconfortável e prefere que esse spotted não seja postado digite:\n{} nem\n\nqualquer dúvida entre em contato pelo discord https://discord.gg/R2uVD7pE7q".format(row[0],contagem,contagem))
            api.send_direct_message(row[1],"MENSAGEM AUTOMATIZADA\n~processo spotted {}~\n\nseu {}\nentrou para consulta automática com citado citado (@{})\nele(a) poderá decidir pela postagem ou não do spotted, previnindo posts que deixem pessoas do nosso circulo social desconfortáveis ou expostas\n\nqualquer dúvida entre em contato digitando ?ajuda [sua msg] ou entre pelo discord https://discord.gg/R2uVD7pE7q".format(row[2],row[0],comando[2]))
            cursor.execute("UPDATE data SET citado=? WHERE contagem=?", (user_citado.id,contagem))
            banco.commit()

            await message.delete()
        elif comando[1] == "contato":
          print("contato")
          cursor.execute("SELECT * FROM contato ORDER BY ref DESC LIMIT 1 ")
          for row in cursor:
            contagem = row[2]
            contagem = (int(re.sub('[^0-9]', '', contagem)) + 1)
            contagem = f'C-{contagem}'

          cursor.execute("SELECT * FROM data WHERE contagem = ('" + comando[0].upper() + "')")
          for row in cursor:
            await log_contato_channel.send("spotted: {}\nref: {}\n\nmensagem: {}\nautor: {}\nprotocolo de contato: {}".format(row[0], row[2], comando[2], message.author.name, contagem))
            print(row[0])
            api.send_direct_message(row[1],"MENSAGEM AUTOMATIZADA\n~Formulário de Contato~\n\nSpotted referido: {}\nRef: {}\n\nMensagem: {}\n\nQualquer dúvida entre em contato digitando ?ajuda [sua msg] aqui na dm ou pelo discord https://discord.gg/R2uVD7pE7q\n\nprotocolo de contato: {}".format(row[0], row[2], comando[2], contagem))
            cursor.execute("INSERT INTO contato (msg, id, ref, resposta, time) values (?,?,?,?,?)",(comando[2], message.author.name, contagem, row[2], timeinfo_sp))
            banco.commit()
            await message.delete()
        else:
          await message.channel.send("comando desconhecido")    

      except tweepy.TweepError as e:
        if e.reason == "[{'code': 187, 'message': 'Status is a duplicate.'}]":
          print("publicação duplicada")
        else:
          print(e.reason)
          await desenvolvimento_channel.send("error: {}\n{}".format(e.reason, content))
      except tweepy.RateLimitError as e:
        await desenvolvimento_channel.send("erro tempo: tentando novamente em 1 minuto\n{}".format(e.reason))
        time.sleep(60)
      except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print(er)
        await desenvolvimento_channel.send("error: {}".format(er.args))
        await desenvolvimento_channel.send(content)
        #api.send_direct_message(id, "erro: {}\n \nesse erro é bem incomum, ele ocorre ao armazenar o dado na database, verifique se não está usando caracteres especiais como ', ele ja deu problemas no passado.\nTente tira-lo de sua msg e envie novamente! Se o erro persistir entre em contato com o pessu de desenvolvimento no discord https://discord.gg/R2uVD7pE7q")
    elif msg.startswith('C-') or msg.startswith('c-'):
      try:
        cursor.execute("SELECT * FROM contato ORDER BY ref DESC LIMIT 1 ")
        for row in cursor:
          contagem = row[2]
          contagem = (int(re.sub('[^0-9]', '', contagem)) + 1)
          contagem = f'C-{contagem}'
        comando = msg.split(" ", 1)
        print(comando)
        print("contato resposta")
        cursor.execute("SELECT * FROM contato WHERE ref = ('" + comando[0].upper() + "')")
        print("contato resposta")
        for row in cursor:
          print("contato resposta")
          await log_contato_channel.send("contato: {}\nref: {}\ntime: {} \n\n\nresposta: {}\nref: {}\nautor: {}\ntime: {}".format(row[0], row[2], row[4], comando[1], contagem, message.author.name, timeinfo_sp))
          api.send_direct_message(int(row[1]),"CONTATO\n~em resposta ao: {}~\n\nResposta:{}\nref: {}\nautor:{}".format(row[2], comando[1], contagem, message.author.name))
          cursor.execute("INSERT INTO contato (msg, id, ref, resposta, time) values (?,?,?,?,?)",(comando[1], message.author.name, contagem, row[2], timeinfo_sp))
          banco.commit()
          await message.channel.send("enviado!\nmsg: {}\nref: {}".format(comando[1], contagem))
      except tweepy.TweepError as e:
        if e.reason == "[{'code': 187, 'message': 'Status is a duplicate.'}]":
          print("publicação duplicada")
        else:
          print(e.reason)
          await desenvolvimento_channel.send("error: {}\n{}".format(e.reason, content))
      except tweepy.RateLimitError as e:
        await desenvolvimento_channel.send("erro tempo: tentando novamente em 1 minuto\n{}".format(e.reason))
        time.sleep(60)
      except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print(er)
        await desenvolvimento_channel.send("error: {}".format(er.args))
        await desenvolvimento_channel.send(content)
    elif message.author.bot == True:
      if message.channel == client.get_channel(794467326660968459):
        if msg.startswith('spotted'):
          await message.add_reaction("❌")
          await message.add_reaction("🆔")
          await message.add_reaction("🗣️")
          await message.add_reaction("😭")
          await message.add_reaction("⚠️")
          await message.add_reaction("✔️")
          
      elif message.channel == client.get_channel(817212322967060521):
        if msg.startswith('[Para: @'):
          await message.add_reaction("🔴")
          #await message.add_reaction("🟡")
          await message.add_reaction("🟢")

      elif message.channel == client.get_channel(794644643278487633):
        if msg.startswith('spotted'):
          print("bot- foi pra discussão")
          await message.add_reaction("❌")
          await message.add_reaction("🆔")
          await message.add_reaction("😭")
          await message.add_reaction("⚠️")
          await message.add_reaction("✔️")

        elif msg.startswith('[Para: @'):
          await message.add_reaction("🔴")
          await message.add_reaction("🟢")

  @client.event
  async def on_raw_reaction_add(payload):
    timeinfo_sp = datetime.now().astimezone(timezone('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M')
    try:
      guild = client.get_guild(payload.guild_id)
      g_channel = guild.get_channel(payload.channel_id)
      disc_message = await g_channel.fetch_message(payload.message_id)
      if payload.member.bot == True:
        return
      elif payload.channel_id == 794751006503469076:
        print("teste")
        return
      else:
        #if payload.channel_id == 794467326660968459 or payload.channel_id == 794644643278487633:
        messages = api.list_direct_messages()
        channel = client.get_channel(payload.channel_id)
        print(channel)
        moderador_name = payload.member.name
        moderador_id = payload.user_id
        content = disc_message.content
        content = content.replace("&gt;", ">")
        content = content.replace("&lt;", "<")
        cemiterio_channel = client.get_channel(795441819902410842)
        discussão_channel = client.get_channel(794644643278487633)
        desenvolvimento_channel = client.get_channel(794801047901831169)
        ranking_channel = client.get_channel(804845726152654858)
        aprovado_channel = client.get_channel(815727445126152223)

        message = await channel.fetch_message(payload.message_id)
        reaction = get(message.reactions, emoji=payload.emoji.name)

        if payload.emoji.name == '❌':
          await disc_message.clear_reactions()
          print("❌")
          print(content)
          await cemiterio_channel.send("spotted **cancelado** por {}, em {} \n {}".format(moderador_name, timeinfo_sp, content))
          await disc_message.edit(content="{} \n**cancelado** por {} em {}".format(content, moderador_name, timeinfo_sp))
          privada_nagada = "MENSAGEM AUTOMATIZADA \nOptamos pela não publicação do seu {} \n\nQualquer dúvida entre em contato digitando ?ajuda [sua msg] aqui na dm ou pelo discord https://discord.gg/R2uVD7pE7q.".format(content)
          cursor.execute("SELECT * FROM data WHERE spotted = ('" + content + "')")
          for row in cursor:
            api.send_direct_message(row[1], privada_nagada)

          try:
            cursor.execute("UPDATE data SET id = 'None' WHERE spotted = '" + content + "'")
            cursor.execute("UPDATE data SET envio=? WHERE spotted=?", (timeinfo_sp,content))
            banco.commit()
          except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print(er)
            await desenvolvimento_channel.send("error: {}\n{}".format(er.args, content))
          except:
            print("dabase error")

        if payload.emoji.name == '✔️':
          try:

            await disc_message.clear_reaction('✔️')
            await disc_message.clear_reactions()
            if disc_message.attachments:
              link = disc_message.attachments[0].filename
              contagem = link.replace(link[link.find('.'):], '')
              arquivo = ""
              try:
                for y in range(len(link) - 1, -1, -1):
                    x = link[y]
                    if x == ".":
                        break
                    arquivo = x + arquivo
                ponto = ".{}".format(arquivo)
                if ponto == ".mp4":
                    video = open(link, 'rb')
                    response = twitter.upload_video(media=video, media_type='video/mp4', media_category='tweet_video', check_progress=True)
                    processing_info = response['processing_info']
                    state = processing_info['state']
                    wait = processing_info.get('check_after_secs', 1)
                    if (state == 'pending' or state == 'in_progress'):
                        print('Waiting ' + wait + 's')
                        time.sleep(wait)
                    else:
                      time.sleep(0.01)
                      twitter.update_status(status=content, media_ids=[response['media_id']])
                    
                elif ponto == ".gif":
                    time.sleep(0.01)
                    pic = api.media_upload(link)
                    time.sleep(0.01)
                    api.update_status(status = content, media_ids = [pic.media_id_string] )

                elif ponto == ".jpg":
                    photo = open(link, 'rb')
                    time.sleep(0.01)
                    response = twitter.upload_media(media=photo)
                    time.sleep(0.01)
                    twitter.update_status(status=content, media_ids=[response['media_id']])
                
                last_tweet = api.user_timeline(id=1291744051193171969,count=1)[0]
                cursor.execute("SELECT * FROM data WHERE contagem = ('" + contagem + "')")
                for row in cursor:
                  api.send_direct_message(row[1],"https://twitter.com/Spotted_do_tt/status/{}".format(last_tweet.id))
                  cursor.execute("UPDATE data SET id = 'None' WHERE spotted = '" + content + "'")
                  cursor.execute("UPDATE data SET envio=? WHERE spotted=?", (timeinfo_sp,content))
                  banco.commit()
              except TwythonError as e:
                await channel.send("erro: {}".format(e))
                await desenvolvimento_channel.send("erro: {}".format(e))
                await desenvolvimento_channel.send(content)
                cursor.execute("SELECT * FROM ce WHERE ce = ('" + content + "')")
                for row in cursor:
                  api.send_direct_message(row[1],"{} \n\nresultou no seguinte \nerror: {}".format(content, e.reason))
                try:
                  cursor.execute("UPDATE data SET id = 'None' WHERE contagem = ('" + contagem + "')")
                  cursor.execute("UPDATE data SET envio=? WHERE spotted=?", (timeinfo_sp,content))
                  #cursor.execute("INSERT INTO data (envio) values (?)",(timeinfo_sp,))
                  banco.commit()
                except sqlite3.Error as er:
                  print('SQLite error: %s' % (' '.join(er.args)))
                  print(er)
                  await desenvolvimento_channel.send("error: {}\n{}".format(er.args, content))

            else:
                api.update_status(content)
                last_tweet = api.user_timeline(id=1291744051193171969,count=1)[0]
                cursor.execute("SELECT * FROM data WHERE spotted = ('" + content + "')")
                for row in cursor:
                  api.send_direct_message(row[1],"https://twitter.com/Spotted_do_tt/status/{}".format(last_tweet.id))
                  cursor.execute("UPDATE data SET id = 'None' WHERE spotted = '" + content + "'")
                  cursor.execute("UPDATE data SET envio=? WHERE spotted=?", (timeinfo_sp,content))
                  banco.commit()
            
            
            try:
              link = disc_message.attachments[0].filename
              contagem = link.replace(link[link.find('.'):], '')
              arquivo = ""
              cursor.execute("SELECT * FROM data WHERE contagem = ('" + contagem + "')")
              FMT= '%d/%m/%Y %H:%M'
              for row in cursor:
                last_tweet = api.user_timeline(id=1291744051193171969,count=1)[0]
                print(row[0])
                print(row[4])
                print(row[3])
                tdelta = datetime.strptime(row[4], FMT) - datetime.strptime(row[3], FMT)
                minutes = tdelta.seconds/60
                chegada = datetime.strptime(row[3], FMT)
                print("ate aqui chegou")
                if chegada.hour >= 0 and chegada.hour <= 6:
                  print("madruga")
                  if minutes > 60:
                    print("demorou pra aprovar")
                    comment = 'MADRUGA\napesar de postado agr, esse post foi escrito {}:{} da manhã'.format(chegada.hour, chegada.minute)
                    resp = api.update_status(comment, in_reply_to_status_id=last_tweet.id, auto_populate_reply_metadata=True)
            except:
              cursor.execute("SELECT * FROM data WHERE spotted = ('" + content + "')")
              FMT= '%d/%m/%Y %H:%M'
              for row in cursor:
                last_tweet = api.user_timeline(id=1291744051193171969,count=1)[0]
                print(row[0])
                print(row[4])
                print(row[3])
                tdelta = datetime.strptime(row[4], FMT) - datetime.strptime(row[3], FMT)
                minutes = tdelta.seconds/60
                chegada = datetime.strptime(row[3], FMT)
                print("ate aqui chegou")
                
                if chegada.hour >= 0 and chegada.hour <= 6:
                  print("madruga")
                  if minutes > 60:
                    print("demorou pra aprovar")
                    comment = 'MADRUGA\napesar de postado agr, esse post foi escrito {}:{} da manhã'.format(chegada.hour, chegada.minute)
                    resp = api.update_status(comment, in_reply_to_status_id=last_tweet.id, auto_populate_reply_metadata=True)
            
            await classe.adicionar_ponto(moderador_id)

            await aprovado_channel.send("**{} aprovou** o envio do {}\nhttps://twitter.com/Spotted_do_tt/status/{}".format(moderador_name, content, last_tweet.id))
            try:
              await disc_message.edit(content="{} \n**aprovado** por {} em {}".format(content, moderador_name, timeinfo_sp))
            except:
              print("falha ao editar")
            
          except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print(er)
            await desenvolvimento_channel.send("error: {}\n{}".format(er.args, content))

        elif payload.emoji.name == '🗣️':
          await disc_message.clear_reactions()
          print("🗣️")
          await discussão_channel.send("<@&794462660803821569>, {} acha melhor discutirmos esse spotted: \n \n votem quando chegarem num consenso".format(moderador_name))

          if disc_message.attachments:
            link = disc_message.attachments[0].filename
            contagem = link.replace(link[link.find('.'):], '')
            await discussão_channel.send(content, file=discord.File(link))
            cursor.execute("SELECT * FROM data WHERE contagem = ('" + contagem + "')")
            for row in cursor:
              await discussão_channel.send("{}".format(row[2]))
              privada_discussão = "MENSAGEM AUTOMÁTICA \n seu {} \n \nteve o processo de publicação pausado para discussão entre os os moderadores.\n Logo mais te avisaremos da decisão tomada por aqui. \n não responda essa mensagem".format(content)
              api.send_direct_message(row[1], privada_discussão)
          else:
            await discussão_channel.send(content)
            cursor.execute("SELECT * FROM data WHERE spotted = ('" + content + "')")
            for row in cursor:
              await discussão_channel.send("{}".format(row[2]))
              privada_discussão = "MENSAGEM AUTOMÁTICA \n seu {} \n \nteve o processo de publicação pausado para discussão entre os os moderadores.\n Logo mais te avisaremos da decisão tomada por aqui. \n não responda essa mensagem".format(content)
              api.send_direct_message(row[1], privada_discussão)
            
            await disc_message.edit(content="{} \n convocada **reunião** por {} em {}".format(content, moderador_name, timeinfo_sp))

          print(content)

        elif payload.emoji.name == '⚠️':
          await disc_message.clear_reactions()
          cursor.execute("SELECT * FROM data WHERE spotted = ('" + content + "')")
          for row in cursor:
            await disc_message.edit(content="{}\n\n{}, para prosseguir no envio da postagem com alerta de gatilho, envie a seguinte mensagem nesse canal mesmo:\n\n{} tw [tipo de gatilho]".format(content, moderador_name, row[2]))
        
        elif payload.emoji.name == '🆔':
          await disc_message.clear_reactions()
          cursor.execute("SELECT * FROM data WHERE spotted = ('" + content + "')")
          for row in cursor:
            await disc_message.edit(content="{}\n\n{}, para prosseguir da consulta do citado, envie a seguinte mensagem nesse canal mesmo:\n\n{} citado [@ do citado]".format(content, moderador_name, row[2]))
        
        elif payload.emoji.name == '😭':
          await disc_message.clear_reactions()
          cursor.execute("SELECT * FROM data WHERE spotted = ('" + content + "')")
          for row in cursor:
            await disc_message.edit(content="{}\n\n {} colocou o spotteed pra confirmação com o remetente".format(content, moderador_name, row[2]))
            cursor.execute("UPDATE data SET citado = id WHERE spotted = ('" + content + "')")
            banco.commit()
            confirmação = "Olá! Vimos sua mensagem e, antes de publica-lá, gostaríamos de te falar uma coisa.\nApesar de não termos como te ajudar diretamente, vale relembrar que pedir ajuda, apesar de difícil, é bastante importante. Seja conversando com amigos, parentes, profissionais ou no Disque 188 (Centro de valorização a vida www.cvv.org.br/quero-conversar ).\n\nEstamos junto com você!🙂\n\nse quiser seguir com o envio do {}\ndigite:\n{} publique".format(row[0], row[2])
            api.send_direct_message(row[1], confirmação)


        elif payload.emoji.name == '🟡':
          print("🟡")
          print(content)
          await reaction.message.clear_reactions()
          CE_conteudo = content.split("[Para: @", 1)[-1].split("]", 1)[-1].split(" ", 1)[-1]
          CE_adaptado = "[Para: @||xxx|| ] {}".format(CE_conteudo)
          print(CE_conteudo)
          print(CE_adaptado)
          try:
            cursor.execute("SELECT * FROM ce WHERE ce = ('" + content + "')")
            for row in cursor:
              dest_name = row[3]
              await discussão_channel.send("<@&794462660803821569>, {} acha melhor discutirmos esse Correio Elegante:".format(moderador_name))
              await discussão_channel.send("[Para: @{} ] {}".format(dest_name, CE_conteudo))
              await discussão_channel.send("em resposta: #{}".format(row[4]))
              await disc_message.edit(content="{} \n**foi para discussão** por {} em {}".format(content, moderador_name, timeinfo_sp))
          except:
            print("nem pa men")

        elif payload.emoji.name == '🔴':
            print("🔴")
            await reaction.message.clear_reactions()
            await cemiterio_channel.send("spotted **cancelado** por {}, em {} \n {}".format(moderador_name, timeinfo_sp, content))
            await disc_message.edit(content="{} \n**cancelado** por {} em {}".format(content, moderador_name, timeinfo_sp))
            privada_nagada = "MENSAGEM AUTOMÁTICA \n seu Correio Elegante: {} \n vai contra nossas diretrizes. O envio foi cancelado.\n Entre em contato pelo discord caso sinta a necessidade https://discord.gg/6waCUeA38B .".format(content)
            cursor.execute("SELECT * FROM ce WHERE ce = ('" + content + "')")
            for row in cursor:
              api.send_direct_message(row[1], privada_nagada)

        elif payload.emoji.name == '🟢':
            print("🟢")
            await reaction.message.clear_reactions()
            CE_conteudo = content.split("[Para: @", 1)[-1].split("]", 1)[-1].split(" ", 1)[-1]
            CE_adaptado = "[Para: @||xxx|| ] {}".format(CE_conteudo)
            if content.split("[Para: @", 1)[-1].split(" ", 1)[-1].split("]", -1)[0] == "(Em resposta)":
              CE_adaptado = "[Para: @||xxx|| (Em resposta)] {}".format(CE_conteudo)
            try:
              cursor.execute("SELECT * FROM ce WHERE ce = ('" + content + "')")
              for row in cursor:
                  dest_name = row[3]
                  #dest_name = content.split("[Para: @", 1)[-1].split(" ")[0]
                  CE_conteudo = content.split("[Para: @", 1)[-1].split("]", 1)[-1].split(" ", 1)[-1]
                  dest_user = api.get_user(dest_name)
                  dest_id = dest_user.id
                  CE_aprovado_channel = client.get_channel(818509891101917244)
                  if content.split("[Para: @", 1)[-1].split(" ", 1)[-1].split("]", -1)[0] == "(Em resposta)":
                    print("em resposta")
                    CE_resp = "[Em resposta: #{}] {}".format(row[4], CE_conteudo)
                    api.send_direct_message(dest_id, CE_resp)
                  else:
                    print("normal")
                    api.send_direct_message(dest_id, CE_conteudo)
                  await CE_aprovado_channel.send("**{} aprovou** o envio do {}".format(moderador_name, content))  
                  cursor.execute("SELECT * FROM ce WHERE ce = ('" + CE_adaptado + "')")
                  for row in cursor:
                    enviado = ("enviado! #{}\n\n{}".format(row[2], row[0]))
                    api.send_direct_message(row[1], enviado)
                    await disc_message.edit(content="{} \n**aprovado** por {} em {}".format(content, moderador_name, timeinfo_sp))
                    print(row[2])
            except:
              cursor.execute("SELECT * FROM ce WHERE ce = ('" + content + "')")
              for row in cursor:
                  dest_name = row[3]
                  #dest_name = content.split("[Para: @", 1)[-1].split(" ")[0]
                  CE_conteudo = content.split("[Para: @", 1)[-1].split("]", 1)[-1].split(" ", 1)[-1]
                  dest_user = api.get_user(dest_name)
                  dest_id = dest_user.id
                  CE_aprovado_channel = client.get_channel(818509891101917244)
                  if content.split("[Para: @", 1)[-1].split(" ", 1)[-1].split("]", -1)[0] == "(Em resposta)":
                    print("em resposta")
                    CE_resp = "[Em resposta: #{}] {}".format(row[4], CE_conteudo)
                    api.send_direct_message(dest_id, CE_resp)
                  else:
                    print("normal")
                    api.send_direct_message(dest_id, CE_conteudo)
                  await CE_aprovado_channel.send("**{} aprovou** o envio do {}".format(moderador_name, content))  
                  cursor.execute("SELECT * FROM ce WHERE ce = ('" + content + "')")
                  for row in cursor:
                    enviado = ("enviado! #{}\n\n{}".format(row[2], row[0]))
                    api.send_direct_message(row[1], enviado)
                    await disc_message.edit(content="{} \n**aprovado** por {} em {}".format(content, moderador_name, timeinfo_sp))
                    print(row[2])

            await classe.adicionar_ponto(moderador_id)
        
        elif payload.emoji.name == '🗨️':
          if disc_message.attachments:
            link = disc_message.attachments[0].filename
            contagem = link.replace(link[link.find('.'):], '')
            cursor.execute("SELECT * FROM data WHERE contagem = ('" + contagem + "')")
            print(link)
            for row in cursor:
              print("ate aqui cheguei")
              await g_channel.send("{}".format(row[2]))
              print("ate aqui cheguei")
          else:
            cursor.execute("SELECT * FROM data WHERE spotted = ('" + content + "')")
            for row in cursor:
              
              await g_channel.send("{}".format(row[2]))

    except tweepy.TweepError as e:
      if e.reason == "[{'code': 187, 'message': 'Status is a duplicate.'}]":
        print("publicação duplicada")
      else:
        print(e.reason)
        await desenvolvimento_channel.send("error: {}\n{}".format(e.reason, content))
        await g_channel.send("error:{} \n\nfoi o erro q deu no \n {}".format(e.reason, content))
        cursor.execute("SELECT * FROM ce WHERE ce = ('" + content + "')")
        for row in cursor:
          api.send_direct_message(row[1],"{} \n\nresultou no seguinte \nerror: {}".format(content, e.reason))
        try:
          cursor.execute("UPDATE data SET id = 'None' WHERE spotted = '" + content + "'")
          banco.commit()
        except sqlite3.Error as er:
          print('SQLite error: %s' % (' '.join(er.args)))
          print(er)
          await desenvolvimento_channel.send("error: {}\n{}".format(er.args, content))
    except tweepy.RateLimitError as e:
      print(e)
      print(e.reason)
      await desenvolvimento_channel.send("erro tempo: {}\n{}".format(e.reason, content))
    except TwythonError as e:
      print(e)
      await desenvolvimento_channel.send("error: {}\n{}".format(e.reason, content))
      await g_channel.send("error:{} \n\nfoi o erro q deu no \n {}".format(e.reason, content))
      cursor.execute("SELECT * FROM ce WHERE ce = ('" + content + "')")
      for row in cursor:
        api.send_direct_message(row[1],"{} \n\nresultou no seguinte \nerror: {}".format(content, e.reason))
      try:
        cursor.execute("UPDATE data SET id = 'None' WHERE spotted = '" + content + "'")
        banco.commit()
      except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print(er)
        await desenvolvimento_channel.send("error: {}\n{}".format(er.args, content))

  @loop(seconds=180)
  async def atualização_spotted():

    messages = api.list_direct_messages()
    desenvolvimento_channel = client.get_channel(794801047901831169)
    cemiterio_channel = client.get_channel(795441819902410842)
    contato_channel = client.get_channel(839143168678559765)

    timeinfo_sp = datetime.now().astimezone(timezone('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M')
    for message in messages:
      spotted_channel = client.get_channel(794467326660968459)
      CE_channel = client.get_channel(817212322967060521)

      text = message.message_create["message_data"]["text"]
      print(text)
      for i in "'":
        text = text.replace(i, ' ')
      for i in "&gt;":
        text = text.replace("&gt;", ">")
      for i in "&lt;":
        text = text.replace("&lt;", "<")
      
      id = message.message_create["sender_id"]
      spotted = f'spotted: {text}'

      if message.message_create["sender_id"] == "1291744051193171969":
        api.destroy_direct_message(message.id)
        print("deletado")
      else:
          try:
            if text.startswith('s-') or text.startswith('S-'):
              print("citado")
              comando = text.split(" ", 1)
              contagem = comando[0].upper()
              aprovado_channel = client.get_channel(815727445126152223)
              cemiterio_channel = client.get_channel(795441819902410842)
              api.destroy_direct_message(message.id)
              try:
                cursor.execute("SELECT * FROM data WHERE contagem = ('" + contagem + "')")
                for row in cursor:
                  string_row = row[0]
                  for i in "&gt;":
                    string_row = string_row.replace("&gt;", ">")
                  for i in "&lt;":
                    string_row = string_row.replace("&lt;", "<")
                  print(id)
                  print(row[5])
                  if int(id) == int(row[5]):
                    print(string_row)
                    if comando[1] == "posta" or comando[1] == "sim":
                      api.update_status(string_row)
                      last_tweet = api.user_timeline(id=1291744051193171969,count=1)[0]
                      api.send_direct_message(row[1],"https://twitter.com/Spotted_do_tt/status/{}".format(last_tweet.id))
                      await aprovado_channel.send("**aprovado por citado** do envio do {}\nhttps://twitter.com/Spotted_do_tt/status/{}".format(spotted, last_tweet.id))
                      cursor.execute("UPDATE data SET id = 'None' WHERE spotted = '" + string_row + "'")
                      cursor.execute("UPDATE data SET envio=? WHERE spotted=?", (timeinfo_sp,string_row))
                      banco.commit()
                    elif comando[1] == "não" or comando[1] == "nem":
                      await cemiterio_channel.send("spotted **cancelado** por citado em {} \n {}".format(timeinfo_sp, content))
                      cursor.execute("UPDATE data SET id = 'None' WHERE spotted = '" + string_row + "'")
                      banco.commit()
                      api.send_direct_message(row[1], "spotted cancelado")
                      api.destroy_direct_message(message.id)
                    
                    elif comando[1] == "publique" or comando[1] == "publica":
                      print(string_row)
                      content = string_row
                      api.update_status("tw // autodepreciação")
                      last_tweet = api.user_timeline(id=1291744051193171969,count=1)[0]
                      res = api.update_status(string_row, in_reply_to_status_id=last_tweet.id, auto_populate_reply_metadata=True)
                      api.send_direct_message(row[1],"https://twitter.com/Spotted_do_tt/status/{}".format(last_tweet.id))
                      #await message.channel.send("o {} \n** foi aprovado (consulta)** as {}".format(content, timeinfo_sp))
                      await aprovado_channel.send("**aprovado** o envio do {}\nhttps://twitter.com/Spotted_do_tt/status/{}".format(content, last_tweet.id))
                      cursor.execute("UPDATE data SET id = 'None' WHERE spotted = '" + content + "'")
                      cursor.execute("UPDATE data SET envio=? WHERE spotted=?", (timeinfo_sp,content))
                      banco.commit()
                      api.destroy_direct_message(message.id)

                  else:
                    print("código inválido")
                    await desenvolvimento_channel.send("erro: código inválido\n{}".format(text))
                    api.send_direct_message(id,"erro: código inválido\n{}".format(text))
                    api.destroy_direct_message(message.id)

              except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print(er)
                await desenvolvimento_channel.send("db error: {}\n{}".format(er.args, text))
                api.send_direct_message(id, "erro no banco de dados\n{}\n{}".format(er.args, text))
                api.destroy_direct_message(message.id)
              except tweepy.TweepError as e:
                if e.reason == "[{'code': 187, 'message': 'Status is a duplicate.'}]":
                  print("publicação duplicada")
                else:
                  print(e.reason)
                  await desenvolvimento_channel.send("error: {}\n{}".format(e.reason, text))
                  api.send_direct_message(id, "tweepy error:\n{}\n{}".format(e.reason, text))
                  api.destroy_direct_message(message.id)
              except tweepy.RateLimitError as e:
                await desenvolvimento_channel.send("erro tempo: tentando novamente em 1 minuto\n{}".format(e.reason))
                time.sleep(60)

            elif text.startswith('?'):
              try:
                print(message.message_create["message_data"]["attachment"]["type"])
                print("é midia")
                api.send_direct_message(message.message_create["sender_id"],
                    "MENSAGEM AUTOMÁTICA \npor enquanto, arquivos de mídia são suportados somente pelo spotted, desculpe")
                api.destroy_direct_message(message.id)
              except:
                cursor.execute("SELECT * FROM ce ORDER BY contagem DESC LIMIT 1 ")
                for row in cursor:
                  contagem = row[2] + 1
                  if text.startswith('?para @'):
                    print("correio elegante")
                    dest_name = text.split("?para @", 1)[-1].split(" ")[0]
                    CE_conteudo = text.split("?para ", 1)[-1].split(" ", 1)[-1]
                    dest_id = api.get_user(dest_name).id_str
                    api.destroy_direct_message(message.id)
                    print(CE_conteudo)
                    aspas_simples = "'"
                    for i in aspas_simples:
                      CE_conteudo = CE_conteudo.replace(i, ' ')
                        
                    print(CE_conteudo)
                    try:
                      CE_pra_moderacao = "[Para: @||xxx|| ] #{} Correio Elegante: {}".format(contagem, CE_conteudo)
                      cursor.execute("INSERT INTO ce (ce, id, contagem, destinatario) values ('" + CE_pra_moderacao + "'," + str(id) + "," + str(contagem) + "," + str(dest_id) + ")")
                      banco.commit()
                      await CE_channel.send(CE_pra_moderacao)
                    except sqlite3.Error as er:
                      print('SQLite error: %s' % (' '.join(er.args)))
                      print(er)
                      await desenvolvimento_channel.send("error: {}".format(er.args))
                      await desenvolvimento_channel.send(text)
                      api.send_direct_message(id, "erro: {}\n \nesse erro é bem incomum, ele ocorre ao armazenar o dado na database, verifique se não está usando caracteres especiais como ', ele ja deu problemas no passado.\nTente tira-lo de sua msg e envie novamente! Se o erro persistir entre em contato com o pessu de desenvolvimento no discord https://discord.gg/R2uVD7pE7q")
                      api.destroy_direct_message(message.id)
                  elif text.startswith('?para #'):
                      print("responder")
                      CE_conteudo = text.split("?para ", 1)[-1].split(" ", 1)[-1]
                      cont_numb = text.split("?para #", 1)[-1].split(" ")[0]
                      cursor.execute("SELECT * FROM ce WHERE contagem = (" + str(cont_numb) + ")")
                      for row in cursor:
                        print(row[3])
                        print(id)
                        #se eles forem iguais subistituir a linha abaixo por
                        verificação_msg = (api.get_user(row[3]).screen_name == api.get_user(id).screen_name)
                        print(verificação_msg)
                        print("destinatario:{}".format(row[3]))
                        dest_id = row[1]
                        print(api.get_user(id).screen_name)
                        CE_pra_moderacao = "[Para: @||xxx|| (Em resposta)] #{} Correio Elegante: {}".format(contagem, CE_conteudo)
                        if row[3] == None or verificação_msg == True:
                          await CE_channel.send(CE_pra_moderacao)
                          cursor.execute("INSERT INTO ce (ce, id, contagem, destinatario, reply) values ('" + CE_pra_moderacao + "'," + str(id) + "," + str(contagem) + "," + str(dest_id) + "," + str(cont_numb) + ")")
                          banco.commit()
                          api.destroy_direct_message(message.id)
                        else:
                          await cemiterio_channel.send("Correio Elegante {} cancelado automaticamente cancelado automaticamente, codigo invalido".format(CE_pra_moderacao))
                          api.send_direct_message(id, "MENSAGEM AUTOMÁTICA\nParece que o código inserido não é válido. Confira se o digitou corretamente e tente novamente\nCorreio Elegante referido: {}\n [erro: acesso negado]".format(CE_conteudo))
                          api.destroy_direct_message(message.id)
                  elif text.startswith('?help'):
                    print("help")
                    api.send_direct_message(id, "MENSAGEM AUTOMATICA - help \nPara enviar Correios Elegantes digite ?para @destinatario sua mensagem\n exemplo: ?para @Bruno_Miguelez_ vai tomar banho.\n\n Para responder um correio elegante o processo é parecido, mas ao inves do @DaPessoa você vai colocar a # com o codigo da sua mensagem! ex: ?para #123 sua resposta\n \nSe não tiver conseguindo lança uma dm ou cola no discord https://discord.gg/rHGZGE85eS")
                    api.destroy_direct_message(message.id)
                  elif text.startswith('? para'):
                    print("? para")
                    api.send_direct_message(id, "MENSAGEM AUTOMATICA - sintaxe incorreta \nParece que voce colocou espaço entre o ponto de interrogação e o 'para'.\nPara enviar Correios Elegantes digite ?para @destinatario sua mensagem\n exemplo: ?para @Bruno_Miguelez_ vai tomar banho.\n\n Para responder um correio elegante o processo é parecido, mas ao inves do @DaPessoa você vai colocar a # com o codigo da sua mensagem! ex: ?para #123 sua resposta\n \nSe não tiver conseguindo lança uma dm ou cola no discord https://discord.gg/rHGZGE85eS")
                    api.destroy_direct_message(message.id)
                  elif text.startswith('?para@') or text.startswith('?para#'):
                    print("?para@")
                    api.send_direct_message(id, "MENSAGEM AUTOMATICA - sintaxe incorreta \nParece que voce deixou de colocar um espaço entre o ?para e o @ ou #.\nPara enviar Correios Elegantes digite ?para @destinatario sua mensagem\n exemplo: ?para @Bruno_Miguelez_ vai tomar banho.\n\n Para responder um correio elegante o processo é parecido, mas ao inves do @DaPessoa você vai colocar a # com o codigo da sua mensagem! ex: ?para #123 sua resposta\n \nSe não tiver conseguindo lança uma dm ou cola no discord https://discord.gg/rHGZGE85eS")
                    api.destroy_direct_message(message.id)
                  elif text.startswith('?ajuda') or text.startswith('?contato'):
                    cursor.execute("SELECT * FROM contato ORDER BY ref DESC LIMIT 1 ")
                    for row in cursor:
                      contagem = row[2]
                      contagem = (int(re.sub('[^0-9]', '', contagem)) + 1)
                      contagem = f'C-{contagem}'
                    print("contato pelo ?ajuda ou ?contato")
                    msg = message.message_create["message_data"]["text"]
                    comando = msg.split(" ", 1)
                    print("contato")
                    cursor.execute("INSERT INTO contato (msg, id, ref, time) values (?,?,?,?)",(comando[1], str(id), contagem, timeinfo_sp))
                    banco.commit()
                    await contato_channel.send("MENSAGEM DE CONTATO\nref: {}\n\n{}".format(contagem, comando[1]))
                    
                    api.send_direct_message(id,"MENSAGEM AUTOMATIZADA\nRecebemos sua mensagem:\n{}\nresponderemos o mais rápido possivel.\n\nref: {}".format(comando[1], contagem))
                    api.destroy_direct_message(message.id)
                  else:
                    #comando incorreto
                    api.send_direct_message(id, "MENSAGEM AUTOMATICA - comando desconhecido \nPara enviar Correios Elegantes digite ?para @destinatario sua mensagem\n exemplo: ?para @Bruno_Miguelez_ vai tomar banho.\n\n Para responder um correio elegante o processo é parecido, mas ao inves do @DaPessoa você vai colocar a # com o codigo da sua mensagem!\n \nSe não tiver conseguindo lança uma dm ou cola no discord https://discord.gg/rHGZGE85eS")
                    await cemiterio_channel.send("erro: sintaxe incorreta\n{}".format(text))
                    api.destroy_direct_message(message.id)
            else:
              if len(spotted) >= 280:
                print("erro 02: mucho texto")
                privada_caracteres = "MENSAGEM AUTOMÁTICA \nseu spotted não pôde ser publicado por exeder o limite de caracteres"
                api.send_direct_message(message.message_create["sender_id"],
                                        privada_caracteres)
                print("error 02: mucho texto")
                api.destroy_direct_message(message.id)
                try:
                  await cemiterio_channel.send("{} \n \n foi **cancelado** automaticamente por exceder o limite de 280 caracteres"
                    .format(message.message_create["message_data"]["text"]))
                except:
                  return
              if 'attachment' in message.message_create["message_data"]:
                print(message.message_create["message_data"]["attachment"]["type"])
                print("é midia")
                cursor.execute("SELECT * FROM data ORDER BY contagem DESC LIMIT 1 ")
                for row in cursor:
                    contagem = row[2]
                    contagem = (int(re.sub('[^0-9]', '', contagem)) + 1)
                    contagem = f'S-{contagem}'
                    print(contagem)
                ponto = None
                if message.message_create["message_data"]["attachment"]["media"]["type"] == 'animated_gif':
                    link = message.message_create["message_data"]["attachment"]["media"]["video_info"]["variants"][0]["url"]
                    print("é gif")
                    ponto = ".gif"
                elif message.message_create["message_data"]["attachment"]["media"]["type"] == 'video':
                    link = message.message_create["message_data"]["attachment"]["media"]["video_info"]["variants"][0]["url"]
                    link = link.replace(link[link.find('?'):], '')
                    print("video")
                    ponto = ".mp4"
                else:
                    link = message.message_create["message_data"]["attachment"]["media"]["media_url"]
                    print("imagem")
                    ponto = ".jpg"

                arquivo = ""
                for y in range(len(link) - 1, -1, -1):
                    x = link[y]
                    if x == ".":
                        break
                    arquivo = x + arquivo
                text = text
                text = text.partition('https')[0]
                time.sleep(0.01)
                media_content = req.get(link, auth=auth2)
                print(media_content)
                arquivo_ponto = ("{}.{}").format(contagem,arquivo)
                with open(arquivo_ponto, 'wb') as midia:
                    for chunk in media_content:
                        midia.write(chunk)

                print(arquivo_ponto)
                spotted = f'spotted: {text}'
                try:
                  cursor.execute("INSERT INTO data (spotted, id, contagem, chegada) values (?,?,?,?)",(spotted, str(id), contagem, timeinfo_sp))
                  banco.commit()
                except sqlite3.Error as er:
                  print('SQLite error: %s' % (' '.join(er.args)))
                  print(er)
                  await desenvolvimento_channel.send("error: {}".format(er.args))
                  api.send_direct_message(id, "erro no banco de dados\n{}\n{}".format(er.args, text))
                  api.destroy_direct_message(message.id)
                if ponto == ".gif":
                    clip = (VideoFileClip(arquivo_ponto))
                    clip.write_gif("{}.gif".format(contagem))
                    arquivo_ponto = "{}.gif".format(contagem)

                await spotted_channel.send(spotted, file=discord.File(arquivo_ponto))
                api.destroy_direct_message(message.id)  

              if not 'attachment' in message.message_create["message_data"]:
                print("spotted texto")
                text = message.message_create["message_data"]["text"]
                aspas_simples = "'"
                for i in aspas_simples:
                  text = text.replace(i, ' ')
                spotted = f'spotted: {text}'
                api.destroy_direct_message(message.id)
                await spotted_channel.send(spotted)
                cursor.execute("SELECT * FROM data ORDER BY contagem DESC LIMIT 1 ")
                for row in cursor:
                  print(row[2])
                  contagem = row[2]
                  contagem = (int(re.sub('[^0-9]', '', contagem)) + 1)
                  contagem = f'S-{contagem}'
                print(message.message_create['message_data']['text'])
                print("deletado")
                try:
                  cursor.execute("INSERT INTO data (spotted, id, contagem, chegada) values (?,?,?,?)",(spotted, str(id), contagem, timeinfo_sp))
                  banco.commit()
                except sqlite3.Error as er:
                  print('SQLite error: %s' % (' '.join(er.args)))
                  print(er)
                  await desenvolvimento_channel.send(
                      "error: {}".format(er.args))
                  api.send_direct_message(id, "erro no banco de dados\n{}\n{}".format(er.args, text))
                  api.destroy_direct_message(message.id)

          except tweepy.TweepError as e:
            if e.reason == "[{'code': 187, 'message': 'Status is a duplicate.'}]":
              print("publicação duplicada")
            else:
              print(e.reason)
              await desenvolvimento_channel.send("error: {}\n{}".format(e.reason, text))
              api.send_direct_message(id, "tweepy error: \n{}\n\nref:\n{}".format(e.reason, text))
              api.destroy_direct_message(message.id)
          except tweepy.RateLimitError as e:
            await desenvolvimento_channel.send("erro tempo: tentando novamente em 1 minuto\n{}".format(e.reason))
            time.sleep(60)
          except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print(er)
            await desenvolvimento_channel.send("error: {}".format(er.args))
            await desenvolvimento_channel.send(text)
            api.send_direct_message(id, "erro: {}\n \nesse erro é bem incomum, ele ocorre ao armazenar o dado na database, verifique se não está usando caracteres especiais como ', ele ja deu problemas no passado.\nTente tira-lo de sua msg e envie novamente! Se o erro persistir entre em contato com o pessu de desenvolvimento no discord https://discord.gg/R2uVD7pE7q")
            api.destroy_direct_message(message.id)
    else:
      print("nada bro")


  #função assíncrona para adicionar ponto ao moderador que aprovou a postagem
  async def adicionar_ponto(moderador_id):
    aprovado_por = None
    ranking_channel = client.get_channel(804845726152654858)
    if moderador_id == 752377953152794736:  #Dora
      print("aprovado por Dora")
      cursor.execute("UPDATE ranking SET pontos = pontos + 1 WHERE moderador = 'Dora'")
      banco.commit()
      aprovado_por = "Dora"

    elif moderador_id == 207678444052414466:  #Rick
      print("aprovado por Rick")
      cursor.execute("UPDATE ranking SET pontos = pontos + 1 WHERE moderador = 'Rick'")
      banco.commit()
      aprovado_por = "Rick"

    elif moderador_id == 710195991789305967:  #Bruno
      print("aprovado por Bruno")
      cursor.execute("UPDATE ranking SET pontos = pontos + 1 WHERE moderador = 'Bruno'")
      banco.commit()
      aprovado_por = "Bruno"

    elif moderador_id == 715676769092501636:  #Kinker
      print("aprovado por Kinker")
      cursor.execute("UPDATE ranking SET pontos = pontos + 1 WHERE moderador = 'Kinker'")
      banco.commit()
      aprovado_por = "Kinker"

    elif moderador_id == 323410392393056258:  #Isaac
      cursor.execute("UPDATE ranking SET pontos = pontos + 1 WHERE moderador = 'Isaac'")
      banco.commit()
      aprovado_por = "Isaac"

    cursor.execute("SELECT * FROM ranking ORDER BY pontos DESC")
    primeiro = cursor.fetchone()
    segundo = cursor.fetchone()
    terceiro = cursor.fetchone()
    quarto = cursor.fetchone()
    quinto = cursor.fetchone()
    result = await ranking_channel.send("**RANKING OFICIAL**\naprovado por : {}\n🏆{}: {}\n🥈{}: {}\n🥉{}: {}\n🥴{}: {}\n🙅‍♂️🤮{}: {} eww gross\n---------------------".format(aprovado_por, primeiro[0], primeiro[1], segundo[0], segundo[1], terceiro[0], terceiro[1], quarto[0], quarto[1], quinto[0], quinto[1]))

@client.event
async def on_comand_error(ctx, error):
  print(error)
  await ctx.send(error)

keep_alive()
client.run(DISCORD_TOKEN)
-----------------------------
