import logging
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)

def mypet(update , context):
   pass
   








MYPET_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('mypet', mypet, pass_user_data=True)],
        states={
            TWO: [CallbackQueryHandler(wheelback, pattern="^back$", pass_user_data=True),
                  CallbackQueryHandler(wheelcheckodd, pattern="^check$", pass_user_data=True),
                  CallbackQueryHandler(wheelplay, pattern="^play$", pass_user_data=True),
                  CallbackQueryHandler(wheelselectchip, pattern="^chip$", pass_user_data=True),
                  CallbackQueryHandler(wheelinc, pattern="^inc$", pass_user_data=True),
                  CallbackQueryHandler(wheeldec, pattern="^dec$", pass_user_data=True)
            ],
            THREE: [CallbackQueryHandler(wheelchangechip, pattern="^.+$")]
        },
        fallbacks=[],
        allow_reentry=True,
        per_user=True
    )
dispatcher.add_handler(MYPET_HANDLER)
