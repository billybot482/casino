import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
import datetime
import random

updater = Updater(token='2134036370:AAEzHQDtUCn9dHsW4VxMz7ufEhcusqkNEUg', use_context=True)
dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()

from main.__main__ import claim_reset
updater.job_queue.run_daily(claim_reset,
			    datetime.time(0,0,0),
			    context=None,
			    name="claim_reset")

updater.start_polling(drop_pending_updates = True)

