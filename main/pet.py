import logging
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)

def mypet(update , context):
   cd = context.chat_data
   query = update.callback_query
   id = update.effective_user.id
   name = update.effective_user.first_name
   username = update.effective_user.name
   
   keyboard = [
        [InlineKeyboardButton("1", callback_data="1"),InlineKeyboardButton("2", callback_data="2"),InlineKeyboardButton("3", callback_data="3")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(f'<b>Quill #0001</breply_markup=reply_markup, parse_mode=ParseMode.HTML)








'''MYPET_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('mypet', mypet, pass_user_data=True)],
        states={
            TWO: [CallbackQueryHandler(wheelback, pattern="^back$", pass_user_data=True)
            ],
            THREE: [CallbackQueryHandler(wheelchangechip, pattern="^.+$")]
        },
        fallbacks=[],
        allow_reentry=True,
        per_user=True
    )
dispatcher.add_handler(MYPET_HANDLER)'''
