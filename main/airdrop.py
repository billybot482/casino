import logging
import random
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)

emote = {'white':'⚪️', 'red':'🔴', 'orange':'🟠', 'yellow': '🟡', 'blue':'🔵', 'purple': '🟣', 'black':'⚫️'}
colour = ['white', 'red', 'orange', 'yellow','blue', 'purple', 'black']

owners = [163494588]

def airdrop(update , context):
    cd = context.chat_data
    user = update.effective_user.first_name
    msg = update.message
    cd['id'] = id = update.effective_user.id
    query = update.callback_query
    cd['VIP'] = VIP = DB.get_user_value(id, "vip")
    cd["worth"] = worth = DB.get_user_value(id, "worth")
    cd["white"] = white = DB.get_user_value(id, "white")
    cd["red"] = red = DB.get_user_value(id, "red")
    cd["orange"] = orange = DB.get_user_value(id, "orange")
    cd["yellow"] = yellow = DB.get_user_value(id, "yellow")
    cd["blue"] = blue = DB.get_user_value(id, "blue")
    cd["purple"] = purple = DB.get_user_value(id, "purple")
    cd["black"] = black = DB.get_user_value(id, "black")
    
    cd['type'] = type = update.message.text.split()[1]
    cd['units'] = units = update.message.text.split()[2]
    units = int(units)
    owner = 163494588

    keyboard = [
        [InlineKeyboardButton('claim', callback_data='claim')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if type == 'white':
       if units <= white:
         if id in owners or VIP >1:
          update.message.reply_text(f"{user} created an airdrop of {units} {type} chip {emote[type]} \n\n First one to click claim will receive it",
                              reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
          context.bot.delete_message(chat_id = update.effective_chat.id, message_id = msg.message_id)
         else:
          update.message.reply_text('You must be VIP 3 or above to use this functions')
         return ONE
       else:
          update.message.reply_text('Balance not enough to create an airdrop')
    if type == 'red':
       if units <= red:
         if id in owners or VIP >1:
          update.message.reply_text(f"{user} created an airdrop of {units} {type} chip {emote[type]} \n\n First one to click claim will receive it",
                              reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
          context.bot.delete_message(chat_id = update.effective_chat.id, message_id = msg.message_id)
         else:
          update.message.reply_text('You must be VIP 3 or above to use this functions')
         return ONE
       else:
          update.message.reply_text('Balance not enough to create an airdrop') 
    if type == 'orange':
       if units <= orange:
         if id in owners or VIP >1:
          update.message.reply_text(f"{user} created an airdrop of {units} {type} chip {emote[type]} \n\n First one to click claim will receive it",
                              reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
          context.bot.delete_message(chat_id = update.effective_chat.id, message_id = msg.message_id)
         else:
          update.message.reply_text('You must be VIP 3 or above to use this functions')
         return ONE
       else:
          update.message.reply_text('Balance not enough to create an airdrop') 
    if type == 'yellow':
       if units <= yellow:
         if id in owners or VIP >1:
          update.message.reply_text(f"{user} created an airdrop of {units} {type} chip {emote[type]} \n\n First one to click claim will receive it",
                              reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
          context.bot.delete_message(chat_id = update.effective_chat.id, message_id = msg.message_id)
         else:
          update.message.reply_text('You must be VIP 3 or above to use this functions')
         return ONE
       else:
          update.message.reply_text('Balance not enough to create an airdrop')
    if type == 'blue':
       if units <= blue:
         if id in owners or VIP >1:
          update.message.reply_text(f"{user} created an airdrop of {units} {type} chip {emote[type]} \n\n First one to click claim will receive it",
                              reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
          context.bot.delete_message(chat_id = update.effective_chat.id, message_id = msg.message_id)
         else:
          update.message.reply_text('You must be VIP 3 or above to use this functions')
         return ONE
       else:
          update.message.reply_text('Balance not enough to create an airdrop') 
    if type == 'purple':
       if units <= purple:
         if id in owners or VIP >1:
          update.message.reply_text(f"{user} created an airdrop of {units} {type} chip {emote[type]} \n\n First one to click claim will receive it",
                              reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
          context.bot.delete_message(chat_id = update.effective_chat.id, message_id = msg.message_id)
         else:
          update.message.reply_text('You must be VIP 3 or above to use this functions')
         return ONE
       else:
          update.message.reply_text('Balance not enough to create an airdrop') 
    if type == 'black':
       if units <= black:
         if id in owners or VIP >1:
          update.message.reply_text(f"{user} created an airdrop of {units} {type} chip {emote[type]} \n\n First one to click claim will receive it",
                              reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
          context.bot.delete_message(chat_id = update.effective_chat.id, message_id = msg.message_id)
         else:
          update.message.reply_text('You must be VIP 3 or above to use this functions')
         return ONE
       else:
          update.message.reply_text('Balance not enough to create an airdrop') 
    if type not in colour:
        update.message.reply_text(f"Choose from these chips to do airdrop \n\n {colour}")


def airdrop2(update , context):
    query = update.callback_query
    query.answer()
    cd = context.chat_data
    id = cd['id']
    name = update.callback_query.from_user.first_name
    user_id = update.callback_query.from_user.id
    
    units = cd['units']
    type = cd['type']
    units = int(units)
    
    VIP = cd['VIP']
    white = cd['white']
    red = cd['red']
    orange = cd['orange']
    yellow = cd['yellow']
    blue = cd['blue']
    purple = cd['purple']
    black = cd['black']
    
    
    
    if cd['type'] == 'white':
     DB.add_white(user_id, units)
     DB.add_white(id, -units) 
    if cd['type'] == 'red':
     DB.add_red(user_id, units)
     DB.add_red(id, -units)
      
    if cd['type'] == 'orange':
     DB.add_orange(user_id, units)
     DB.add_orange(id, -units)
      
    if cd['type'] == 'yellow':
     DB.add_yellow(user_id, units)
     DB.add_yellow(id, -units)
      
    if cd['type'] == 'blue':
     DB.add_blue(user_id, units)
     DB.add_blue(id, -units)
      
    if cd['type'] == 'purple':
     DB.add_purple(user_id, units)
     DB.add_purple(id, -units)
      
    if cd['type'] == 'black':
     DB.add_black(user_id, units)
     DB.add_black(id, -units)
    
    
    query.message.edit_text(f'{name} claimed {units} {type} {emote[type]} chip\n\n Congrats 🎊', parse_mode = ParseMode.MARKDOWN_V2)

    return ConversationHandler.END
  
  
AIRDROP_HANDLER = ConversationHandler(
    entry_points=[CommandHandler('airdrop', airdrop)],
    states={
        ONE:
            [
                CallbackQueryHandler(airdrop2, pattern="^claim$")
            ]
    },
    fallbacks=[],
    allow_reentry=True,
    per_user=False

)
dispatcher.add_handler(AIRDROP_HANDLER)
