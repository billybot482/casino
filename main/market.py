import logging
import random
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)

def market(update, context):
    name = update.effective_user.first_name
    username = update.effective_user.name
    VIP = DB.get_user_value(id, "vip")
    worth = DB.get_user_value(id, "worth")
    white = round(DB.get_user_value(id, "white"),4)
    red = round(DB.get_user_value(id, "red"),4)
    orange = round(DB.get_user_value(id, "orange"),4)
    yellow = round(DB.get_user_value(id, "yellow"),4)
    blue = round(DB.get_user_value(id, "blue"),4)
    purple = round(DB.get_user_value(id, "purple"),4)
    black = round(DB.get_user_value(id, "black"),4)

    value = round((white*1)+(red*5)+(orange*25)+(yellow*100)+(blue*500)+(purple*2000)+(black*15000),4)
    
    update.message.reply_text(f"Welcome {name} to the market 🏢\n\n1.items\n2.items\n3.items") 

def blackmarket(update, context):
    id = update.effective_user.id
    vip = DB.get_user_value(id,"vip")
    if vip>5:
     update.message.reply_text("This is black market🕋\n\nA place for rare items") 
    else:
     update.message.reply_text("Kids are not allowed in black market🕋") 
    





MARKET_HANDLER = CommandHandler('market', market)
dispatcher.add_handler(MARKET_HANDLER)

BLACK_HANDLER = CommandHandler('blackmarket', blackmarket)
dispatcher.add_handler(BLACK_HANDLER)
