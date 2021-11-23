import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
import random
from main import checker, dispatcher , game
import json
import os
from telegram.ext.dispatcher import run_async
import time
from main import database as DB
import requests

DB_PATH=os.environ['DATABASE_URL']
DB.init(DB_PATH)
DB.setup()

#state
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)
#callback data
S_START , S_INCREASE ,S_POP , SS_POP, FIRST , SECOND ,THIRD,CHECK, SHOW, *_ = range(1000)
owners = [163494588]
