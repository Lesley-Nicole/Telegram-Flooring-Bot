import re
from time import sleep
from flask import Flask, request
import telegram
From telebot.ai import generate_smart_reply
from telebot.credentials import bot_token, bot_user_name,URL

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

  #start flask app                 
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    #retrieve the message in JSON and transfer to telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    
    #Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()
    #for debugging purposes only
    print("got text message :", text)
    #here call your smart reply
    reply = generate_smart_reply(text)
    bot.sendMessage(chat_id=chat_id, text=reply, reply_to_message_id=msg_id)
    #the first time you chat with the bot AKA welcoming message
    if text == "/start":
        #print the welcoming message
        bot_welcome = """
        Welcome to coolAvatar bot, the bot is using the service from the
        http://avatars.adorable.io/ to generate cool looking avatars based on
        the name you enter so please enter a name and the bot will reply with
        an avatar for your name."""
        
        #send the welcoming message
        bot.sendChatAction(chat_id=chat_id, action="typing")
        sleep(1.5)
        bot.sendMessage(chat_id=chat_id, text=bot_welcome,
                        reply_to_message_id=msg_id)
        
    else:
        try:
            #clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)
            #create the api link for the avatar based on http://avatars.adorable.io/
            url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
            #reply with a photo to the name the user sent,
            #note that you can send photos by url and telegram will fetch for you
            bot.sendChatAction(chat_id=chat_id, action="upload_photo")
            sleep(2)
            bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
        except Exception:
            #if things went wrong
            bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name",
                            reply_to_message_id=msg_id)
            
            return 'ok'
        
        @app.route('/set_webhook', methods=['GET', 'POST'])
        def set_webhook():
            s = bot.setWebhook('{https://git.heroku.com/a-lflooringbot.git}{/setwebhook}'.format(URL=URL, HOOK=TOKEN))
            if s:
                return "webhook setup ok"
            else:
                return "webhook setup failed"
            
            @app.route('/')
            def index():
                return '.'
            
            
            if __name__ == '__main__':
                app.run(threaded=True)
