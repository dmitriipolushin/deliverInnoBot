from telebot import types

# Initial keyboard
keyboard_main = types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
keyboard_main.row(
    '📌 Add Offer',
    '🗓 Offers List',
    )
# keyboard to navigate over different offers lists
keyboard_offers_list = types.ReplyKeyboardMarkup(True)
keyboard_offers_list.row('📒 My Offers', 'All offers', '⬅️ Back')
# keyboard to accept or drop new offer
keyboard_confirmation = types.ReplyKeyboardMarkup(True)
keyboard_confirmation.row('✅ Confirm', '❌ Drop')
# keybord to navigate over user offers
keyboard_my_offers = types.ReplyKeyboardMarkup(True)
keyboard_my_offers.row('📕 Published Offers', '📗 Taken Offers', '⬅️ Back')


not_offers_list = ['next_offer_id', 'alias', 'dungling_offer', 'profile']