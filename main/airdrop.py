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
colours = {1:white, 2:red, 3:orange, 4:yellow, 5:blue, 6:purple, 7:black}
owners = [163494588]

def airdrop(update , context):
    cd = context.chat_data
    user = update.effective_user.first_name
    msg = update.message
    cd['id'] = id = update.effective_user.id
    query = update.callback_query
    cd['VIP'] = VIP = DB.get_user_value(id, "vip")
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
    n = 1
    keyboard = [
        [InlineKeyboardButton('claim', callback_data='claim')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    for i in colour:
       if unit <= colours[n]:  
         if type == i:
            if id in owners or VIP>1:
              update.message.reply_text(f"{user} created an airdrop of {units} {type} chip {emote[type]} \n\n First one to click claim will receive it",
                              reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN_V2)
              context.bot.delete_message(chat_id = update.effective_chat.id, message_id = msg.message_id)
         else:
          update.message.reply_text('You must be VIP 3 or above to use this functions')
         return ONE
       else:
          update.message.reply_text('Balance not enough to create an airdrop')
              
    
    
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
    
    
    
    for i in colour:
      if cd['type'] == i:
        DB.add_chip(user_id , i , units)
        DB.sub_chip(user_id , i , units)
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
