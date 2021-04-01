'''
programa: spotted_v3
linguagem: python v3.9
autor: @Bruno_Miguelez_ , @allan
versão: v3.4
destaque: adição correio elegante
'''
import tweepy
import time
import os
from keep_alive import keep_alive
import discord
from discord import Webhook, RequestsWebhookAdapter
import requests
from datetime import datetime
from pytz import timezone
from discord.ext import tasks, commands
from discord.utils import get
from discord.ext.tasks import loop
from discord.ext.commands import Bot
import sqlite3
import pickle
from operator import itemgetter

timeinfo_sp = datetime.now().astimezone(timezone('America/Sao_Paulo')).strftime('%d/%m/%Y %H:%M')

print(timeinfo_sp)

auth = tweepy.OAuthHandler((os.getenv('consumer_key')),
                           (os.getenv('consumer_secret')))
auth.set_access_token((os.getenv('access_token')),
                      (os.getenv('access_token_secret')))
try:
  api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
except tweepy.RateLimitError as e:
  print(e)
  print(e.reason)
client = discord.Client()
banco = sqlite3.connect('database.db')
cursor = banco.cursor()


keep_alive()


class classe:
  @client.event
  async def on_ready():
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
    msg = message.content
    if message.author.bot == True:
      if message.channel == client.get_channel(794467326660968459):
        if msg.startswith('spotted'):
          await message.add_reaction("❌")
          await message.add_reaction("🗣️")
          await message.add_reaction("🕗")
          time.sleep(10)
          await message.clear_reaction('🕗')
          await message.add_reaction("✔️")
      elif message.channel == client.get_channel(817212322967060521):
        if msg.startswith('[to: @'):
          await message.add_reaction("🔴")
          await message.add_reaction("🟡")
          await message.add_reaction("🟢")

    if message.author.bot == True:
      if message.channel == client.get_channel(794644643278487633):
        if msg.startswith('spotted'):
          print("bot- foi pra discussão")
          await message.add_reaction("✔️")
          await message.add_reaction("❌")

        elif msg.startswith('[to: @'):
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
        cemiterio_channel = client.get_channel(795441819902410842)
        discussão_channel = client.get_channel(794644643278487633)
        desenvolvimento_channel = client.get_channel(794801047901831169)
        ranking_channel = client.get_channel(804845726152654858)
        aprovado_channel = client.get_channel(815727445126152223)

        message = await channel.fetch_message(payload.message_id)
        reaction = get(message.reactions, emoji=payload.emoji.name)
        #print(payload.emoji.name)
        #for message in message:

        if payload.emoji.name == '❌':
          await disc_message.clear_reactions()
          print("❌")
          #await channel.send("{} cancelou o envio do {}".format(moderador_name, content))
          print(content)
          await cemiterio_channel.send("spotted **cancelado** por {}, em {} \n {}".format(moderador_name, timeinfo_sp, content))
          await disc_message.edit(content="{} \n**cancelado** por {} em {}".format(content, moderador_name, timeinfo_sp))
          privada_nagada = "MENSAGEM AUTOMÁTICA \n seu {} \n vai contra nossas diretrizes. O envio foi cancelado.\nO motivo do cancelamento e o status da sua conta serão enviados em breve.".format(content)

          cursor.execute("SELECT * FROM data WHERE spotted = ('" + content + "')")
          for row in cursor:
            api.send_direct_message(row[1], privada_nagada)

          try:
            cursor.execute("DELETE FROM data WHERE spotted = '" +
                           content + "'")
            banco.commit()
          except sqlite3.Error as er:
            print('SQLite error: %s' % (' '.join(er.args)))
            print(er)
            await desenvolvimento_channel.send("error: {}\n{}".format(er.args, content))
          except:
            print("dabase error")
          #privada_nagada = "MENSAGEM AUTOMÁTICA \n consideramos que seu {} \n vai contra nossas diretrizes. Entre em contato pelo discord caso sinta necessidade https://discord.gg/gfUkYdSsWY ".format(
          #    content)
          #send = api.send_direct_message(db_id, privada_nagada)

        if payload.emoji.name == '✔️':
          '''if reaction and reaction.count > 2:
                print(reaction.count)
                await channel.send("LOL {} loser kkkkkkkkkkkk".format(moderador_name))
                return
              else:
                print(reaction.count) '''

          await disc_message.clear_reaction('✔️')
          await disc_message.clear_reactions()
          try:
            api.update_status(content)

            print("✔️")

            last_tweet = api.user_timeline(id=1291744051193171969,count=1)[0]
            await aprovado_channel.send("**{} aprovou** o envio do {}\nhttps://twitter.com/Spotted_do_tt/status/{}".format(moderador_name, content, last_tweet.id))
            cursor.execute("SELECT * FROM ranking")
            print(cursor.fetchall())
            cursor.execute("SELECT * FROM data WHERE spotted = ('" + content + "')")
            for row in cursor:
              api.send_direct_message(row[1],"https://twitter.com/Spotted_do_tt/status/{}".format(last_tweet.id))
            await disc_message.edit(content="{} \n**aprovado** por {} em {}".format(content, moderador_name, timeinfo_sp))
            aprovado_por = ""
            #print(ranking_dic)
            print(moderador_name)

            #print(reaction.message)
            #print(ranking_message.content)
            #print(ranking_message)

            if moderador_id == 752377953152794736:  #Dora
              print("aprovado por Dora")
              cursor.execute(
                  "UPDATE ranking SET pontos = pontos + 1 WHERE moderador = 'Dora'"
              )
              banco.commit()

              aprovado_por = "Dora"

            elif moderador_id == 207678444052414466:  #Rick
              print("aprovado por Rick")
              cursor.execute(
                  "UPDATE ranking SET pontos = pontos + 1 WHERE moderador = 'Rick'"
              )
              banco.commit()
              aprovado_por = "Rick"

            elif moderador_id == 710195991789305967:  #Bruno
              print("aprovado por Bruno")
              cursor.execute(
                  "UPDATE ranking SET pontos = pontos + 1 WHERE moderador = 'Bruno'"
              )
              banco.commit()
              aprovado_por = "Bruno"

            elif moderador_id == 715676769092501636:  #Kinker
              print("aprovado por Kinker")
              cursor.execute(
                  "UPDATE ranking SET pontos = pontos + 1 WHERE moderador = 'Kinker'"
              )
              banco.commit()
              aprovado_por = "Kinker"

            cursor.execute(
                "SELECT * FROM ranking ORDER BY pontos DESC")
            await ranking_channel.send(
                "**RANKING OFICIAL**\naprovado por : {}\n{}\n---------------------------------------------------------"
                .format(aprovado_por, cursor.fetchall()))
            ''' ordenado = sorted(ranking_dic.items(), key=itemgetter(1), reverse=True)

                  await ranking_channel.send("**RANKING OFICIAL**\naprovado por : {}\n🏆{}: {}\n🥈{}: {}\n🥉{}: {}\n🙅‍♂️🤮{}: {} eww gross\n---------------------".format(aprovado_por, ordenado[0][0], ordenado[0][1], ordenado[1][0], ordenado[1][1], ordenado[2][0], ordenado[2][1], ordenado[3][0], ordenado[3][1])) '''

            #print(ranking_message.content)
            try:
              cursor.execute(
                  "DELETE FROM data WHERE spotted = '" + content + "'")
              banco.commit()
            except sqlite3.Error as er:
              print('SQLite error: %s' % (' '.join(er.args)))
              print(er)
              await desenvolvimento_channel.send("error: {}\n{}".format(er.args, content))

          except tweepy.TweepError as e:
            print(e.reason)
            return
          except tweepy.RateLimitError as e:
            print(e)
            print(e.reason)

        elif payload.emoji.name == '🗣️':
          await disc_message.clear_reactions()
          print("🗣️")
          await discussão_channel.send("<@&794462660803821569>, {} acha melhor discutirmos esse spotted: \n \n votem quando chegarem num consenso"
              .format(moderador_name))
          await discussão_channel.send("{}".format(content))
          await disc_message.edit(content="{} \n convocada **reunião** por {} em {}".format(content, moderador_name, timeinfo_sp))

          #privada_discussão = "MENSAGEM AUTOMÁTICA \n seu {} \n teve o processo de publicação pausado para consulta do citado ou discussão entre a comissão. \n Logo mais te avisaremos da decisão tomada por aqui. \n não responda essa mensagem".format(content)
          #send = api.send_direct_message(sender_id[content], privada_discussão)
          print(content)

        elif payload.emoji.name == '🟡':
            print("🟡")
            await reaction.message.clear_reactions()
            await discussão_channel.send("<@&794462660803821569>, {} acha melhor discutirmos esse {} \n \n votem quando chegarem num consenso".format(moderador_name, content))
            await discussão_channel.send("{}".format(content))
            await disc_message.edit(content="{} \n**foi para discussão** por {} em {}".format(content, moderador_name, timeinfo_sp))

        elif payload.emoji.name == '🔴':
            print("🔴")
            await reaction.message.clear_reactions()
            await cemiterio_channel.send("spotted **cancelado** por {}, em {} \n {}".format(moderador_name, timeinfo_sp, content))
            await disc_message.edit(content="{} \n**cancelado** por {} em {}".format(content, moderador_name, timeinfo_sp))
            privada_nagada = "MENSAGEM AUTOMÁTICA \n seu {} \n vai contra nossas diretrizes. O envio foi cancelado.\nO motivo do cancelamento e o status da sua conta serão enviados em breve.".format(content)
            cursor.execute("SELECT * FROM ce WHERE ce = ('" + content + "')")
            for row in cursor:
              api.send_direct_message(row[1], privada_nagada)
              ''' try:
                cursor.execute("DELETE FROM ce WHERE ce = '" + content + "'")
                banco.commit()
              except sqlite3.Error as er:
                print('SQLite error: %s' % (' '.join(er.args)))
                print(er)
                await desenvolvimento_channel.send("error: {}\n{}".format(er.args, content)) '''

        elif payload.emoji.name == '🟢':
            print("🟢")
            await reaction.message.clear_reactions()
            dest_name = content.split("[to: @", 1)[-1].split(" ")[0]
            CE_conteudo = content.split("[to: @", 1)[-1].split("]", 1)[-1].split(" ", 1)[-1]
            dest_user = api.get_user(dest_name)
            dest_id = dest_user.id
            CE_aprovado_channel = client.get_channel(818509891101917244)
            if content.split("[to: @", 1)[-1].split(" ", 1)[-1].split("]", -1)[0] == "(in reply)":
              print("em resposta")
              cursor.execute("SELECT * FROM ce WHERE ce = ('" + content + "')")
              for row in cursor:
                CE_resp = "[in reply:#{}] {}".format(row[4], CE_conteudo)
                api.send_direct_message(dest_id, CE_resp)
            else:
              api.send_direct_message(dest_id, CE_conteudo)

            await disc_message.edit(content="{} \n**aprovado** por {} em {}".format(content, moderador_name, timeinfo_sp))
            await CE_aprovado_channel.send("**{} aprovou** o envio do {}".format(moderador_name, content))  
            cursor.execute("SELECT * FROM ce WHERE ce = ('" + content + "')")
            for row in cursor:
              enviado = ("enviado! #{}".format(row[2]))
              api.send_direct_message(row[1], enviado)
              print(row[2])

    except tweepy.TweepError as e:
      print(e.reason)
      await desenvolvimento_channel.send("error: {}\n{}".format(e.reason, content))
      await g_channel.send("error:{} \n\nfoi o erro q deu no \n {}".format(e.reason, content))
      cursor.execute("SELECT * FROM ce WHERE ce = ('" + content + "')")
      for row in cursor:
        api.send_direct_message(row[1],"{} \n\nresultou no seguinte \nerror: {}".format(content, e.reason))
      try:
        cursor.execute("DELETE FROM data WHERE spotted = '" + content + "'")
        banco.commit()
      except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print(er)
        await desenvolvimento_channel.send("error: {}\n{}".format(er.args, content))
    except tweepy.RateLimitError as e:
      print(e)
      print(e.reason)

  @loop(seconds=120)
  async def atualização_spotted():

    messages = api.list_direct_messages()
    desenvolvimento_channel = client.get_channel(794801047901831169)
    cemiterio_channel = client.get_channel(795441819902410842)

    for message in messages:
      spotted_channel = client.get_channel(794467326660968459)
      CE_channel = client.get_channel(817212322967060521)

      text = message.message_create["message_data"]["text"]
      id = message.message_create["sender_id"]
      spotted = f'spotted: {text}'
      print(text)

      if message.message_create["sender_id"] == "1291744051193171969":
        api.destroy_direct_message(message.id)
        print("deletado")
      else:
        try:
          print(message.message_create["message_data"]["attachment"]["type"])
          print("é midia")
          api.send_direct_message(message.message_create["sender_id"],
              "MENSAGEM AUTOMÁTICA \narquivos de mídia ainda não são suportados, desculpe")
          api.destroy_direct_message(message.id)
        except:
          try:
            if text.startswith('?'):
              cursor.execute("SELECT * FROM ce ORDER BY contagem DESC LIMIT 1 ")
              for row in cursor:
                contagem = row[2] + 1
                if text.startswith('?para @'):
                  print("correio elegante")
                  dest_name = text.split("?para @", 1)[-1].split(" ")[0]
                  CE_conteudo = text.split("?para ", 1)[-1].split(" ", 1)[-1]
                  api.destroy_direct_message(message.id)
                  try:
                    CE_pra_moderacao = "[to: @{} ] #{} Correio Elegante: {}".format(dest_name, contagem, CE_conteudo)
                    cursor.execute("INSERT INTO ce (ce, id, contagem, destinatario) values ('" + CE_pra_moderacao + "'," + str(id) + "," + str(contagem) + ",'" + dest_name + "')")
                    banco.commit()
                    await CE_channel.send(CE_pra_moderacao)
                  except sqlite3.Error as er:
                    print('SQLite error: %s' % (' '.join(er.args)))
                    print(er)
                    await desenvolvimento_channel.send("error: {}".format(er.args))
                    await desenvolvimento_channel.send(text)
                elif text.startswith('?para #'):
                    print("responder")
                    CE_conteudo = text.split("?para ", 1)[-1].split(" ", 1)[-1]
                    cont_numb = text.split("?para #", 1)[-1].split(" ")[0]
                    #try:
                    cursor.execute("SELECT * FROM ce WHERE contagem = (" + str(cont_numb) + ")")
                    for row in cursor:
                          verificação_msg = (row[3] == api.get_user(id).screen_name)
                          print(verificação_msg)
                          await desenvolvimento_channel.send(verificação_msg)
                          print("destinatario:{}".format(row[3]))
                          dest_id = row[1]
                          dest_user = api.get_user(dest_id)
                          dest_name = dest_user.screen_name
                          #print("destinatario: {}".format(dest_name))
                          print(api.get_user(id).screen_name)
                          CE_pra_moderacao = "[to: @{} (in reply)] #{} Correio Elegante: {}".format(dest_name, contagem, CE_conteudo)
                          await CE_channel.send(CE_pra_moderacao)
                          cursor.execute("INSERT INTO ce (ce, id, contagem, destinatario, reply) values ('" + CE_pra_moderacao + "'," + str(id) + "," + str(contagem) + ",'" + dest_name + "'," + str(cont_numb) + ")")
                          banco.commit()
                          api.destroy_direct_message(message.id)
                          if verificação_msg == False:
                            await CE_channel.send("vale verificar essa daí, <@&794462688994394112>, reprovou na verificação.")
                          ''' 
                        except tweepy.TweepError as e:
                          print(e.reason)
                          await desenvolvimento_channel.send("error: {}\n{}".format(e.reason, text))
                    except sqlite3.Error as er:
                      print('SQLite error: %s' % (' '.join(er.args)))
                      print(er)
                      await desenvolvimento_channel.send("error: {}".format(er.args))
 '''
                else:
                  #comando incorreto
                  api.send_direct_message(id, "MENSAGEM AUTOMATICA - sintaxe incorreta \n Para enviar Correios Elegantes digite ?para @destinatario sua mensagem\n exemplo: ?para @Bruno_Miguelez_ vai tomar banho\n se não tiver conseguindo lança uma dm ou cola no discord https://discord.gg/rHGZGE85eS")
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
                
              else:
                print("dentro do spotted")
                api.destroy_direct_message(message.id)
                await spotted_channel.send(spotted)

                print(message.message_create['message_data']['text'])
                print("deletado")
                try:
                  cursor.execute("INSERT INTO data (spotted, id) values ('" + spotted + "'," + str(id) + ")")
                  banco.commit()
                except sqlite3.Error as er:
                  print('SQLite error: %s' % (' '.join(er.args)))
                  print(er)
                  await desenvolvimento_channel.send(
                      "error: {}".format(er.args))

          except tweepy.TweepError as e:
            print(e.reason)
            await desenvolvimento_channel.send("error: {}\n{}".format(e.reason, text))
    else:
      print("nada bro")


@client.event
async def on_comand_error(ctx, error):
  print(error)
  await ctx.send(error)


client.run(os.getenv('token'))
 '''
