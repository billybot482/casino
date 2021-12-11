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
   print('entered')
   
   keyboard = [
        [InlineKeyboardButton("1", callback_data="1"),InlineKeyboardButton("2", callback_data="2"),InlineKeyboardButton("3", callback_data="3")],
      [InlineKeyboardButton("Previous", callback_data="back"),InlineKeyboardButton("Next", callback_data="next")]
    ]
   reply_markup = InlineKeyboardMarkup(keyboard)
    
   update.message.reply_text(f'<b><u>My pet collections</u></b>\n\n<b>Quill #0001</b>\n<b>Blaze #0001</b>\n<b>Dinosaur #0001</b>',reply_markup=reply_markup, parse_mode=ParseMode.HTML)








'''MYPET_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('mypet', mypet, pass_user_data=True)],
        states={
            TWO: [#CallbackQueryHandler(wheelback, pattern="^back$", pass_user_data=True)
            ],
        },
        fallbacks=[],
        allow_reentry=True,
        per_user=True
    )'''
MYPET_HANDLER = CommandHandler('mypet', mypet)
dispatcher.add_handler(MYPET_HANDLER)
