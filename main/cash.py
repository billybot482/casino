import logging
import random
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB

def calculate_worth(white=0, red=0, orange=0, yellow=0, blue=0, purple=0, black=0):
    return round((white*1)+(red*5)+(orange*25)+(yellow*100)+(blue*500)+(purple*2000)+(black*15000),4)
  
 
