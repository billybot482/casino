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
    Chat = update.effective_chat
    if update.effective_chat.type != Chat.PRIVATE:
       update.message.reply_text("Use in pm")
       return -1
    cd = context.chat_data
    query = update.callback_query
    cd['id'] = id = update.effective_user.id
    name = update.effective_user.first_name
    username = update.effective_user.name
    VIP = DB.get_user_value(id, "vip")
    cd['white'] =white = round(DB.get_user_value(id, "white"),4)
    cd['red'] =red = round(DB.get_user_value(id, "red"),4)
    cd['orange'] =orange = round(DB.get_user_value(id, "orange"),4)
    cd['yellow'] =yellow = round(DB.get_user_value(id, "yellow"),4)
    cd['blue'] = blue = round(DB.get_user_value(id, "blue"),4)
    cd['purple'] =purple = round(DB.get_user_value(id, "purple"),4)
    cd['black'] =black = round(DB.get_user_value(id, "black"),4)
    cat_quantity = DB.quantity_cat()
    cd['slot'] = slot = DB.get_user_value(id , 'slots')
    cd['cs'] = current_slot = len(DB.get_pet(id))
    
    value = round((white*1)+(red*5)+(orange*25)+(yellow*100)+(blue*500)+(purple*2000)+(black*15000),4)
    keyboard = [
         [InlineKeyboardButton('cat', callback_data='cat')]
     ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(f"Welcome {name} to the market 🏢\n<i>Here the list of things in sale</i>"
                              f"\n\n1.<b>Cat - 50🔵 </b>\nQuantity left : {cat_quantity}\n\nPress button below to buy", parse_mode = ParseMode.HTML, reply_markup = reply_markup)
    
    return ONE

def cancel(update , context):
    cd = context.chat_data
    query = update.callback_query
    query.edit_message_text('exited market')
    return ConversationHandler.END

def buy_cat(update , context):
    a = random.randint(1,999)
    talent = random.randint(5,30)
    distract = random.randint(5,30)
    confident = random.randint(5,200)
    slot = cd['slot']
    cs = ['cs']
    # max talent = 30
    # max distract = 30 
    # confident 200 
    tag = "#" + str(a).zfill(3)
    id = cd['id']
    cd = context.chat_data
    query = update.callback_query
    blue = cd['blue']
    if slot > cs:
     if blue >=50:
        DB.add_pet_cat(id , a , talent , distract , confident)
        query.edit_message_text(f'Congratulation you are now owner of Cat {tag}\n'
                                f'stats if your pet:\n'
                                f'Talent : {talent}\nDistract : {distract}\nConfident : {confident}', parse_mode = ParseMode.HTML)
        return ConversationHandler.END
     else:
        query.answer('Balance not enough')
    else:
        query.asnwer('Not enough slot')
    

def blackmarket(update, context):
    id = update.effective_user.id
    vip = DB.get_user_value(id,"vip")
    if vip>5:
     update.message.reply_text("This is black market🕋\n\nA place for rare items") 
    else:
     update.message.reply_text("Kids are not allowed in black market🕋") 
    


MARKET_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('market', market)],
        states={
            ONE: [CallbackQueryHandler(buy_cat, pattern='^' + str("cat") + '$'),
                   CallbackQueryHandler(cancel, pattern='^' + str("cancel") + '$')
            ],
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=True
    )

dispatcher.add_handler(MARKET_HANDLER)

BLACK_HANDLER = CommandHandler('blackmarket', blackmarket)
dispatcher.add_handler(BLACK_HANDLER)
