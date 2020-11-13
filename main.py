import messages as messages
import os
import re
from bot import bot
from keyboards import *
import lists
import db as db
import time
import flask
import telebot
from TOKEN import *


def operations(message, operation):
    """Set of basic operations that available for user in bot.

    Args:
        message (message): Utility telebot object.
        operation (string): Operation that user want to be execute.

    Returns:
        lambda: Function that shoud be executed by user command.
    """
    operation = re.findall(r'\w*', operation)
    op_string = ''
    operation = op_string.join(operation)
    chat_id = message.chat.id
    set_of_operations = {
        'addoffer': lambda: send_msg_and_register_next(
            message=message,
            msg=messages.choosing_market,
            next_handler=get_item,
            ),
        'offerslist': lambda: bot.send_message(
            chat_id,
            messages.choose_section,
            reply_markup=keyboard_offers_list,
            ),
        'back': lambda: bot.send_message(
            chat_id,
            messages.choose_section,
            reply_markup=keyboard_main,
            ),
        'myoffers': lambda: bot.send_message(
            chat_id,
            messages.choose_section,
            reply_markup=keyboard_my_offers,
            ),
        'alloffers': lambda: lists.all_offers(
            message=message,
            ),
        'drop': lambda: approve_offer(
            message=message,
            approved=False,
            chat_id=chat_id,
            ),
        'confirm': lambda: approve_offer(
            message=message,
            approved=True,
            chat_id=chat_id,
            ),
        'publishedoffers': lambda: lists.published_offers(
            message
            ),
        'takenoffers': lambda: lists.taken_offers(
            message
            ),
    }
    try:
        return set_of_operations[operation.lower()]()
    except KeyError:
        bot.send_message(chat_id, 'Can not understand you')
    

def send_msg_and_register_next(message, msg, next_handler, markup=None):
    """Template function that take send message to user and call next handler.

    Args:
        message: answer from telegram api.
        msg: text of message that should be send to user.
        next_handler: function that execute next message from user.
        markup: keyboard for user. Defaults to None.
    """
    chat_id = message.chat.id
    bot.send_message(chat_id, msg, reply_markup=markup)
    bot.register_next_step_handler(message, next_handler)


@bot.message_handler(commands=['start'])
def start_message(message):
    """Greeting of useer when he first time in bot. 
    And also create entry in database for his information

    Args:
        message: answer from telegram api.
    """
    chat_id = message.chat.id
    bot.send_message(
        message.chat.id,
        messages.intro_message,
        reply_markup=keyboard_main,
        )
    if not db.user_exists(chat_id):
        db.new_user(chat_id, message.from_user.username)
        
   
@bot.message_handler(commands=['cancel'])
def cancel_off(message):
    """TODO: implement function to cancel offers during filling fields (shop, item, bounty)
    """    
    chat_id = message.chat.id
    


@bot.message_handler(content_types=['text'])
def choose_section(message):
    """General message handler.

    Args:
        message: answer from telegram api.
    """
    msg = message.text

    operations(message, msg)  # Function to processes commands by given message


def get_item(message):
    """Function to ger item for offer

    Args:
        message (): shop name for offer
    """
    chat_id = message.chat.id
    shop = message.text

    bot.send_message(chat_id, messages.choosing_item)
    bot.register_next_step_handler(message, set_bounty, shop)


def set_bounty(message, shop):
    """Function to get bounty for offer

    Args:
        message (): item for offer
        shop (str): shop for offer
    """
    chat_id = message.chat.id
    item = message.text
    
    bot.send_message(chat_id,
                     messages.set_bounty
                     )
    bot.register_next_step_handler(message, add_offer, shop, item)
    
    
def add_offer(message, shop, item):
    """add dungling offer that user need to approve

    Args:
        message (): bounty
        shop (str): shop for offer 
        item (str): item for offer
    """
    chat_id = message.chat.id
    bounty = message.text
    
    # Если юзер не прожимал старт во время запуска бота(хз как) создаем его док в базе
    if db.user_exists(chat_id):
        db.add_dungling_offer(chat_id, shop, item, bounty)
    else:
        db.new_user(chat_id, message.from_user.username)
        db.add_dungling_offer(chat_id, shop, item, bounty)
    
    bot.send_message(chat_id, 
                    messages.print_offer.format(shop,
                                               item,
                                               bounty
                                               ),
                    reply_markup=keyboard_confirmation
                    )



def approve_offer(message, approved, chat_id):
    """approving affer then add it to list of published offer in db

    Args:
        message ([type]): for next handler
        approved (boolean): if True then approved
        chat_id ([type]): id of user that offer we should approve
    """
    if approved:
        db.approve_offer(chat_id)
        
        bot.send_message(int(chat_id), 
                         messages.confirm_offer,
                         reply_markup=keyboard_main
                         )
    
    else:
        bot.send_message(chat_id, 
                         messages.drop_offer,
                         reply_markup=keyboard_main
                         )

    bot.register_next_step_handler(message, choose_section)


app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        data = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(data)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

def start_app():        

    time.sleep(1)
    # Set webhook
    bot.set_webhook(url='https://a1dc5c5aaa4e.ngrok.io'+ WEBHOOK_URL_PATH)
                    # certificate=open(WEBHOOK_SSL_CERT, 'r'))
    
    app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        # ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)
