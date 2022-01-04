import logging
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
import random
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)

dict = {'white': 1, 'red': 5, 'orange': 25, 'yellow': 100, 'blue': 500, 'purple': 2000, 'black': 15000}
colours = ["white", "red", "orange", "yellow", "blue", "purple", "black"]

rb = ["rbwhite", "rbred", "rborange", "rbyellow", "rbblue", "rbpurple", "rbblack"]

def dice(update , context):
    print('entry')
    id = update.message.from_user.id
    name = update.message.from_user.first_name
    username = update.message.from_user.name
    vip = DB.get_user_value(id, "vip")
    white = DB.get_user_value(id, "white")
    red = DB.get_user_value(id, "red")
    orange = DB.get_user_value(id, "orange")
    yellow = DB.get_user_value(id, "yellow")
    blue = DB.get_user_value(id, "blue")
    purple = DB.get_user_value(id, "purple")
    black = DB.get_user_value(id, "black")
    mult = 0
    c = {1:white, 2:red, 3:orange, 4:yellow, 5:blue, 6:purple, 7:black}
    type = update.message.text.split()[1]
    amount = update.message.text.split()[2]
    amount = int(amount)
    n = 0
    vip = int(vip)
    multy = (((vip+1)/10)+(vip*0.2))/100
    print(multy)
    if amount <=0:
     update.message.reply_text('Cant be 0 or lower')
     return -1
     
     
    a = random.randint(1,6) 
    if a == 1:
     mult +=0
    if a == 2:
     mult +=0
    if a == 3:
     mult +=0
    if a == 4:
     mult +=1.5
    if a == 5:
     mult +=2
    if a == 6:
     mult +=2.5

    for i in colours:
        n+=1
        if type == i:
            if amount <=c[n]:
              update.message.reply_text(f'<b>Dice game classic</b>\n\n'
                              f'1🎲  0x \n2🎲  0x\n3🎲  0x\n4🎲  1.5x\n5🎲  2x\n6🎲  2.5x\n\n'
                              f'<b>You bet</b> {amount} {type} chip\n'
                              f'<b>You rolled </b> {a}\n'
                              f'<b>You got </b>{mult*amount} {type} chip', parse_mode = ParseMode.HTML)
              DB.add_chip(id, i , mult*amount)
              DB.sub_chip(id, i , amount)
              print("before") 
              DB.add_wager(id , amount*dict[colours[n-1]])
              print("after") 
              DB.add_rbchip(id , i ,amount*multy)
              print('rb done')
              if a>3:
               DB.add_win(id,1)
              else:
               DB.add_loss(id,1)
            
            else:
             update.message.reply_text('Balance not enough')
            
            




DICE_HANDLER = CommandHandler('dice', dice)

dispatcher.add_handler(DICE_HANDLER)



