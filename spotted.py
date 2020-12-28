import tweepy
import time
import random

auth = tweepy.OAuthHandler()
auth.set_access_token()
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

messages = api.list_direct_messages()
for message in messages:
        try:
            print (message.message_create['message_data']['text'])
            text = message.message_create["message_data"]["text"]
            api.update_status(f'spotted: {text}')
            # remove DM
            api.destroy_direct_message(message.id)
else:
        print ("nada bro")
        time.sleep(60)
