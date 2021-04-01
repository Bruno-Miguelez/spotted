'''
programa: spotted_do_tt
linguagem: python v3.8
autor: @Bruno_Miguelez_
versão: v1.2
'''

#importar as bibilhotecas necessarias para o projeto
import tweepy #bibilhoteca não nativa, precisa digitar o comando 'pip install tweepy' no terminal para baixar
import time 

#logar pela api do twitter
auth = tweepy.OAuthHandler()
auth.set_access_token()

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True) #estabelece limite de tempo entre requests
messages = api.list_direct_messages() #defini mensagem


for message in messages: #abre um loop, algo do tipo "se receber uma mensagem"
        try:
            text = message.message_create["message_data"]["text"] # filtra só o texto da msg e ""copia""
            api.update_status(f'spotted: {text}') #publica essa msg no perfil
            api.destroy_direct_message(message.id) #apaga a dm
        
        
        except tweepy.TweepError as e: #se der qualquer erro
            print(e.reason)            #me fala qual é
        
else: #se n tiver nenuma DM
        print ("nada bro") #fala q n tem nd
        time.sleep(60) #espera 60 segundos (tempo limite da API do twitter) e volta pro começo, vê dnv se chegou alguma coisa
