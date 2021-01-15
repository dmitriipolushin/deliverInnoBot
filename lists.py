from telebot import types
from bot import bot
from keyboards import *
from db import *
from messages import *

"""Implementing all listings of offers in bot 
    deletions of offers 
    and take open offers
"""

def published_offers(message):
    """List of own user offer.

    Args:
        message: answer from telegram api.
    """
    chat_id = message.chat.id
    if not user_exists(chat_id):
            new_user(chat_id, message.from_user.username)
    # list of published offers from MongoDB
    offers_list = list_published_offers(chat_id)
    if len(offers_list) == 0:
        bot.send_message(chat_id, empty_list)
    for offer in offers_list:
        offer_number = offer
        delete_button = types.InlineKeyboardMarkup(row_width=1)
        delete_button.add(
            types.InlineKeyboardButton('Delete', 
                                        callback_data='delete published {}'.format(offer_number)
                                        )
            )
        if 'alias' in offers_list[offer_number]:
            bot.send_message(
                chat_id,
                taken_published_offer.format(
                    offer_number,
                    offers_list[offer_number]['taker_alias'],
                    offers_list[offer_number]['shop'],
                    offers_list[offer_number]['item'],
                    offers_list[offer_number]['bounty'],
                    ), reply_markup=delete_button
                )
        else:    
            bot.send_message(
                chat_id,
                published_offer.format(
                    offer_number,
                    offers_list[offer_number]['shop'],
                    offers_list[offer_number]['item'],
                    offers_list[offer_number]['bounty'],
                    ), reply_markup=delete_button
                )


def taken_offers(message):
    """List of user taken offer.

    Args:
        message: answer from telegram api.
    """
    chat_id = message.chat.id
    if not user_exists(chat_id):
        new_user(chat_id, message.from_user.username)
    offers_list = list_taken_offers(chat_id)
    if len(offers_list) == 0:
        bot.send_message(chat_id, empty_list)
    for offer in offers_list:
        offer_number = offer
        delete_button = types.InlineKeyboardMarkup(row_width=1)
        delete_button.add(
            types.InlineKeyboardButton('Delete', 
                                        callback_data='delete taken {}'.format(offer_number)
                                        )
            )
        if 'taken' not in offer:
            bot.send_message(
                chat_id,
                list_my_taken_offers.format(
                    offers_list[offer_number]['alias'],
                    offers_list[offer_number]['shop'],
                    offers_list[offer_number]['item'],
                    offers_list[offer_number]['bounty'],
                    ), reply_markup=delete_button
                )
        else:
            bot.send_message(
                chat_id,
                list_other_taken_offers.format(
                    offers_list[offer_number]['alias'],
                    offers_list[offer_number]['shop'],
                    offers_list[offer_number]['item'],
                    offers_list[offer_number]['bounty'],
                    ), reply_markup=delete_button
                )
        

def all_offers(message):
    """List of all offers open to accept for user.
    
    Args:
        message: answer from telegram api.
    """
    chat_id = message.chat.id
    if not user_exists(chat_id):
        new_user(chat_id, message.from_user.username)
    # we get the information about every user except the one with id - chat_id
    all_users = list_all_offers(chat_id)
    offer_counter = 0
    for user in all_users:
        for offer in user['published_offers']:
            offer_number = offer
            take_button = types.InlineKeyboardMarkup(row_width=1)
            take_button.add(
                types.InlineKeyboardButton('Take', 
                                            callback_data='take {} {}'.format(user['_id'], offer_number)
                                            )
                )
            bot.send_message(
                chat_id,
                list_offers.format(
                    user['published_offers'][offer]['shop'],
                    user['published_offers'][offer]['item'],
                    user['published_offers'][offer]['bounty'],
                    ), reply_markup=take_button
                )
            offer_counter += 1
                
    
    if offer_counter == 0:
        bot.send_message(chat_id, empty_list)
        

def profile(message):
    chat_id = message.chat.id
    db.change_profile(chat_id)
    kazan_button = types.InlineKeyboardMarkup(row_width=1)
    profile_num = db.get_profile_num(chat_id)
    # 0 - published_offers
    # 1 - taken_offers
    # 2 - in_kazan
    if profile_num[2] == 0:    
        kazan_button.add(
            types.InlineKeyboardButton('Arrive in Kazan', 
                                        callback_data='kazan {} {}'.format(chat_id, 1)
                                        )
            )
    else:
        kazan_button.add(
            types.InlineKeyboardButton('Left Kazan', 
                                        callback_data='kazan {} {}'.format(chat_id, 0)
                                        )
            )
    bot.send_message(chat_id,
                     profile_message.format(profile_num[0], profile_num[1]), 
                     reply_markup=kazan_button)


def notify_users(chat_id, offer):
    users_in_kazan = db.list_users_in_kazan(chat_id)
    for user in users_in_kazan:
        user_id = user['_id']
        take_button.add(
            types.InlineKeyboardButton('Take', 
                                       callback_data='take {} {}'.format(user_id, offer_number)
                                       )
            )
        bot.send_message(
            user_id,
            list_offers.format(
                offer['shop'],
                offer['item'],
                offer['bounty'],
                ), reply_markup=take_button
            )
        

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    response = call.data
    chat_id = call.from_user.id
    response = response.split(' ')
    if 'delete' in response:
        try:
            # request to delete looks like 'delete <number>'
            # to get the number we split it py space and take second element
            number = response[2]
            if response[1] == 'published':
                delete_published_offer(chat_id, number)
            else:
                delete_taken_offer(chat_id, number)
            bot.answer_callback_query(callback_query_id=call.id,
                                        text=delet_offer_from_published.format(number)
                                        )
        except KeyError as e:
            bot.answer_callback_query(callback_query_id=call.id)
            print('error')
        
    if 'take' in response:
        try:
            # request to take looks like 'take <user_id> <number>'
            # to get the id of employer and number of offer we split it py space and take first and second element
            user_id = int(response[1])
            number = response[2]
            if not user_exists(chat_id):
                new_user(chat_id, message.from_user.username)
            take_offer(chat_id, user_id, number)

            # message to person who will deliver
            bot.answer_callback_query(callback_query_id=call.id)
            bot.send_message(chat_id, performer_message.format(get_alias(user_id)))
            # message to person who will recieve
            bot.send_message(user_id, recipient_message.format(number, get_alias(chat_id)))
        except KeyError as e:
            bot.answer_callback_query(callback_query_id=call.id)
            print('error')
    
    if 'kazan' in response:
        try:
            number = response[2]
            if number == 1:
                db.kazan_status(chat_id, number)
                bot.answer_callback_query(callback_query_id=call.id)
                bot.send_message(chat_id, arrive_message)
            else:
                db.kazan_status(chat_id, number)
                bot.answer_callback_query(callback_query_id=call.id)
                bot.send_message(chat_id, left_message)
        except KeyError as e:
            bot.answer_callback_query(callback_query_id=call.id)
            print('error')
    