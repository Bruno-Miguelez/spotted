<h1 align="center">
    <a href="https://twitter.com/Spotted_do_tt">spotted</a>
</h1>
<p align="center">portal oficial do fogo no cu</p>

[![](https://img.shields.io/discord/794297088246153246?color=7289da&label=Discord&logo=Discord&style=for-the-badge)](https://discord.gg/fHaMSAKsg7)
[![](https://img.shields.io/static/v1?label=project%20version&message=v2.1&color=sucess&style=for-the-badge)](https://github.com/apatacadof/spotted/blob/main/spotted.py)
[![](https://img.shields.io/github/license/apatacadof/spotted?logo=&style=for-the-badge)](https://raw.githubusercontent.com/apatacadof/spotted/7a1142bd2d2aef7e32b69a8038080377b415d953/LICENSE)
[![](https://img.shields.io/static/v1?label=pyhon&message=2.7|3.5|3.6|3.7|3.8&logo=python&color=informational&style=for-the-badge)](https://www.python.org/)
[![](https://img.shields.io/static/v1?label=project&message=beta&color=yellowgreen&style=for-the-badge)](https://github.com/apatacadof/spotted/blob/main/spotted.py)
[![](https://img.shields.io/uptimerobot/status/m786806468-a734c9b76f9e14caac6270ec?style=for-the-badge)]()
[![](https://img.shields.io/uptimerobot/ratio/7/m786806468-a734c9b76f9e14caac6270ec?style=for-the-badge)]()
[![](https://img.shields.io/uptimerobot/ratio/m786806468-a734c9b76f9e14caac6270ec?label=uptime%20last%2030%20days&style=for-the-badge)]()

### entenda o código: linha por linha

essencialmente esse é o código.
    
    for message in messages:
        try:
            text = message.message_create["message_data"]["text"]
            api.update_status(f'spotted: {text}')
            api.destroy_direct_message(message.id)
        except tweepy.TweepError as e:
            print(e.reason)
    else:
        print ("nada bro")
        time.sleep(60)
        
Esse é um recorte, tem umas enrrolações antes, você pode conferir essa versão completa [clicando aqui](https://github.com/apatacadof/spotted/blob/main/spotted.py)

bora destrinchar isso aí
