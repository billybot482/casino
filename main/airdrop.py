import logging
import random
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)

def airdrop(update , context):
    user = update.effective_user.first_name
    msg = update.message
    user_id = update.effective_user.id
    query = update.callback_query
    cd = context.chat_data
    VIP = DB.get_user_value(id, "vip")
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
    owner = 163494588

    keyboard = [
        [InlineKeyboardButton('claim', callback_data='claim')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    a = context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=update.effective_user.id).status
    
    if user_id in owners or VIP >1:
     update.message.reply_text(f"{user} created an airdrop of {units} {type} chip \n\n First one to click claim will receive it",
                              reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
     context.bot.delete_message(chat_id = update.effective_chat.id, message_id = msg.message_id)
  
    else:
      update.message.reply_text('You must be VIP 3 or above to use this functions')
    return ONE

def airdrop2(update , context):
    user = update.effective_user.first_name
    user_id = update.effective_user.id
    query = update.callback_query
    query.answer()
    cd = context.chat_data
    name = update.callback_query.from_user.first_name
    user_id = update.callback_query.from_user.id
    
    units = cd['units']
    type = cd['type']
    
    white = cd['white']
    red = cd['red']
    orange = cd['orange']
    yellow = cd['yellow']
    blue = cd['blue']
    purple = cd['purple']
    black = cd['black']
    
    emote = {'white':'⚪️', 'red':'🔴', 'orange':'🟠', 'yellow': '🟡', 'blue':'🔵', 'purple': '🟣', 'black':'⚫️'}
    
    if cd['type'] == 'white'
     DB.add_white(user_id, units)
      
    if cd['type'] == 'red'
     DB.add_red(user_id, units)
      
    if cd['type'] == 'orange'
     DB.add_orange(user_id, units)
      
    if cd['type'] == 'yellow'
     DB.add_yellow(user_id, units)
      
    if cd['type'] == 'blue'
     DB.add_blue(user_id, units)
      
    if cd['type'] == 'purple'
     DB.add_purple(user_id, units)
      
    if cd['type'] == 'black'
     DB.add_black(user_id, units)
    
    
    query.message.edit_text(f'{name} claimed {units} {type} {emote[{type}]} chip\n\n Congrats 🎊', parse_mode = ParseMode.MARKDOWN_V2)

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
