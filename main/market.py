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
    update.message.reply_text("This is market : under building") 

def blackmarket(update, context):
    id = update.effective_user.id
    vip = DB.get_user_value(id,"vip")
    if vip>5:
     update.message.reply_text("This is black market") 
    else:
     update.message.reply_text("Kids are not allowed in black market") 
    





MARKET_HANDLER = CommandHandler('market', market)
dispatcher.add_handler(MARKET_HANDLER)

BLACK_HANDLER = CommandHandler('blackmarket', blackmarket)
dispatcher.add_handler(BLACK_HANDLER)
