from time import sleep
from dotenv import load_dotenv
import tweepy as tw
import telegram
import os

load_dotenv()

class StreamListener(tw.StreamListener):
    def __init__(self):
        self.initialize_tokens()

    def initialize_tokens(self):
        """
        This function intitializes all the reqired tokens to connect to twitter and telegram bot
        :return: None
        """
        self.consumer_key = os.getenv('CONUSUMER_KEY')
        self.consumer_secret = os.getenv('CONUSUMER_SECRET')
        self.bearer_token = os.getenv('BEARER_TOKEN')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
        self.bot_token = os.getenv('BOT_TOKEN')
        self.chat_id = os.getenv('CHAT_ID')
        self.auth = tw.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tw.API(self.auth, wait_on_rate_limit=True)
        self.usernames = ['20536157', '783214', ]

    def send(self, msg, chat_id, token):
        """
        This function sends a particular message to the group chat/ persons chat id on telegram
        :param msg:
        :param chat_id:
        :param token:
        :return:
        """
        bot = telegram.Bot(token=token)
        bot.sendMessage(chat_id=chat_id, text=msg)

    def on_status(self, status):
        if (str(status.user.id) in self.usernames) and ('RT @' not in status.text):
            data_tweet = "@"+status.user.screen_name+": "+status.text
            print(data_tweet)
            self.send(data_tweet, self.chat_id, self.bot_token)

    def on_error(self, status_code):
        if status_code == 420:
            return False
        else:
            pass

def executeBot():
    stream_listener = StreamListener()
    stream_listener.api.user_timeline()
    stream = tw.Stream(auth=stream_listener.api.auth, listener=stream_listener)
    stream.filter(follow=stream_listener.usernames)

if __name__ == '__main__':
    try:
        print("Starting Service")
        executeBot()
    except:
        print("Error Occured... Restrating")
        sleep(5)
        executeBot()