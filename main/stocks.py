import logging
import random
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB

ONE , TWO , THREE , FOUR , *_ = range(1000)
owners = [163494588]

def stock(update , context):
    cd = context.chat_data
    query = update.callback_query
    id = update.effective_user.id
    cd['name'] = name = update.message.text.split()[1]
    cd['symbol'] = symbol = update.message.text.split()[2]
    cd['price'] = price = update.message.text.split()[3]
    cd['supply'] = supply = update.message.text.split()[4]
    
    keyboard = [
        [
            InlineKeyboardButton("confirm", callback_data=str('confirm')),
            InlineKeyboardButton("cancel", callback_data=str('cancel'))
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if id in owners:
      update.message.reply_text(f'<b>Name :</b> {name}\n'
                                f'<b>symbol:</b> {symbol}\n'
                                f'<b>price:</b> {price}\n'
                                f'<b>supply:</b> {supply}\n\n'
                                f'Double check if all the info are correct before pressing confirm\n', reply_markup=reply_markup , parse_mode = ParseMode.HTML)
    else:
      update.message.reply_text('Not authorised')
    return ONE
    
def stock1(update , context):
    cd = context.chat_data
    query = update.callback_query
    query.answer()
    if update.callback_query.from_user.id in owners:
     query.edit_message_text('cancelled')
    
def stock2(update , context):
    cd = context.chat_data
    query = update.callback_query
    name = cd['name']
    symbol = cd['symbol']
    price = cd['price']
    supply = cd['supply']
    if update.callback_query.from_user.id not in owners:
      query.answer('not authorised')
    else:
      DB.add_stock(name , symbol , price , supply)
      query.edit_message_text(f'{name} is now tradeable stocks in exchange')
    
    
def exchange(update ,context):
    price = DB.get_price()
    all_stock = DB.get_stock() 
    n = 1
    b = "" 
    o = [] 
    for k in price:
     for p in k:
      o.append(p)
    
    for i in all_stock:
     for j in i:
      b+=str(j)+ " - " +str(o[n-1])+"$"+"\n"
     n+=1
     
  
    update.message.reply_text(f'<u>Welcome to exchange</u>\n\n'
                              f'<b>{b}</b>\n\n'
                              f'<i>current market price may change due to demand and supply.</i>'
                              f'\n<i>set order base on your judgement</i>', parse_mode = ParseMode.HTML)

    

def p(update, context):
    pick = update.message_text.split()[1] 
    name = DB.get_stock_value(pick,"name")
    price = DB.get_stock_value(pick,"price") 
    supply = DB.get_stock_value(pick, "supply") 

    update.message.reply_text(f'Name : {name}\n'
                              f'Price : {price}\n'
                              f'Supply : {supply}') 

























STOCK_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('stock', stock)],
        states={
            ONE: [
                CallbackQueryHandler(stock2, pattern='^' + str('confirm') + '$'),
                CallbackQueryHandler(stock1, pattern='^' + str('cancel') + '$')

            ],
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=True
    )


EXCHANGE_HANDLER = CommandHandler("exchange",exchange)
P_HANDLER = CommandHandler("p",p)



dispatcher.add_handler(STOCK_HANDLER)
dispatcher.add_handler(EXCHANGE_HANDLER)
dispatcher.add_handler(P_HANDLER)









