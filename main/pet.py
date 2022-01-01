import logging
import enum
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)
owners = [163494588]


def mint(update , context):
   id = update.effective_user.id
   type = update.message.text.split()[1]
   amount = int(update.message.text.split()[2])
   if id in owners:
      DB.mint_pet(type , amount)
      update.message.reply_text(f'minted extra {amount} {type}')
   else:
      update.message.reply_text(f'not authorised')
      
def petcontrol(update , context):
   id = update.effective_user.id
   check = len(DB.quantity_cat())
   if check ==1:
      update.message.reply_text('pet control already initiated')
      return -1
   if id in owners:
      DB.pet_control()
      update.message.reply_text(f'added pet control system')
   else:
      update.message.reply_text(f'not authorised')

def mypet(update , context):
   cd = context.chat_data
   query = update.callback_query
   id = update.effective_user.id
   name = update.effective_user.first_name
   username = update.effective_user.name
   n = 1
   text = '' 
   cat_id = DB.get_cat(id)
   for i in cat_id:
    text += str(n)+'.'+ ' Cat #'+str(i).zfill(3)+'\n'
    n+=1
   update.message.reply_text('Pet collection\n\n{text}')
   

def check(update , context):
    pass





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
PETCONTROL_HANDLER = CommandHandler('petcontrol', petcontrol)
MINT_HANDLER = CommandHandler('mint', mint)
dispatcher.add_handler(MINT_HANDLER)
dispatcher.add_handler(MYPET_HANDLER)
dispatcher.add_handler(PETCONTROL_HANDLER)





