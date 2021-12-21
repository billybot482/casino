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
    type = update.message.text.split()[1]
    amount = update.message.text.split()[2]
    amount = int(amount)
    
    vip = int(vip)
    multy = (((vip+1)/10)+(vip*0.2))/100
    if amount <=0:
     update.message.reply_text('Cant be 0 or lower')
     return -1
     
     
    a = random.randint(1,6) 
    if a == 1:
     mult +=0
    if a == 2:
     mult +=0
    if a == 3:
     mult +=1
    if a == 4:
     mult +=1.5
    if a == 5:
     mult +=2
    if a == 6:
     mult +=2.5
     
    print('random generated') 
    if type == 'white':
     if amount <= white:
      update.message.reply_text(f'<b>Dice game classic</b>\n\n'
                              f'1🎲  0x \n2🎲  0x\n3🎲  1x\n4🎲  1.5x\n5🎲  2x\n6🎲  2.5x\n\n'
                              f'<b>You bet</b> {amount} {type} chip\n'
                              f'<b>You rolled </b> {a}\n'
                              f'<b>You got </b>{mult*amount} {type} chip', parse_mode = ParseMode.HTML)
      DB.add_white(id , -amount)
      DB.add_white(id, mult*amount)
      DB.add_wager(id , amount)
      DB.add_rbwhite(id , amount*multy)
     else:
      update.message.reply_text('Balance not enough')
    if type == 'red':
     if amount <= red:
      update.message.reply_text(f'<b>Dice game classic</b>\n\n'
                              f'1🎲  0x \n2🎲  0x\n3🎲  1x\n4🎲  1.5x\n5🎲  2x\n6🎲  2.5x\n\n'
                              f'<b>You bet</b> {amount} {type} chip\n'
                              f'<b>You rolled </b> {a}\n'
                              f'<b>You got </b>{mult*amount} {type} chip', parse_mode = ParseMode.HTML)
      DB.add_red(id , -amount)
      DB.add_red(id, mult*amount) 
      DB.add_wager(id , amount)
      DB.add_rbred(id , amount*multy)
     else:
      update.message.reply_text('Balance not enough')                         
    if type == 'orange':
     if amount <= orange:
      update.message.reply_text(f'<b>Dice game classic</b>\n\n'
                              f'1🎲  0x \n2🎲  0x\n3🎲  1x\n4🎲  1.5x\n5🎲  2x\n6🎲  2.5x\n\n'
                              f'<b>You bet</b> {amount} {type} chip\n'
                              f'<b>You rolled </b> {a}\n'
                              f'<b>You got </b>{mult*amount} {type} chip', parse_mode = ParseMode.HTML)
      DB.add_orange(id , -amount)
      DB.add_orange(id, mult*amount)
      DB.add_wager(id , amount)
      DB.add_rborange(id , amount*multy)
     else:
      update.message.reply_text('Balance not enough')
    if type == 'yellow':
     if amount <= yellow:
      update.message.reply_text(f'<b>Dice game classic</b>\n\n'
                              f'1🎲  0x \n2🎲  0x\n3🎲  1x\n4🎲  1.5x\n5🎲  2x\n6🎲  2.5x\n\n'
                              f'<b>You bet</b> {amount} {type} chip\n'
                              f'<b>You rolled </b> {a}\n'
                              f'<b>You got </b>{mult*amount} {type} chip', parse_mode = ParseMode.HTML)
      DB.add_yellow(id , -amount)
      DB.add_yellow(id, mult*amount)
      DB.add_wager(id , amount)
      DB.add_rbyellow(id , amount*multy)
     else:
      update.message.reply_text('Balance not enough')
    if type == 'blue':
      if amount <= blue:
       update.message.reply_text(f'<b>Dice game classic</b>\n\n'
                              f'1🎲  0x \n2🎲  0x\n3🎲  1x\n4🎲  1.5x\n5🎲  2x\n6🎲  2.5x\n\n'
                              f'<b>You bet</b> {amount} {type} chip\n'
                              f'<b>You rolled </b> {a}\n'
                              f'<b>You got </b>{mult*amount} {type} chip', parse_mode = ParseMode.HTML)
       DB.add_blue(id , -amount)
       DB.add_blue(id, mult*amount)
       DB.add_wager(id , amount)
       DB.add_rbblue(id , amount*multy)
      else:
       update.message.reply_text('Balance not enough')
    if type == 'purple':
      if amount <= purple:
       update.message.reply_text(f'<b>Dice game classic</b>\n\n'
                              f'1🎲  0x \n2🎲  0x\n3🎲  1x\n4🎲  1.5x\n5🎲  2x\n6🎲  2.5x\n\n'
                              f'<b>You bet</b> {amount} {type} chip\n'
                              f'<b>You rolled </b> {a}\n'
                              f'<b>You got </b>{mult*amount} {type} chip', parse_mode = ParseMode.HTML)
       DB.add_purple(id , -amount)
       DB.add_purple(id, mult*amount) 
       DB.add_wager(id , amount)
       DB.add_rbpurple(id , amount*multy)
      else:
       update.message.reply_text('Balance not enough')
    if type == 'black':
      if amount <= black:
       update.message.reply_text(f'<b>Dice game classic</b>\n\n'
                              f'1🎲  0x \n2🎲  0x\n3🎲  1x\n4🎲  1.5x\n5🎲  2x\n6🎲  2.5x\n\n'
                              f'<b>You bet</b> {amount} {type} chip\n'
                              f'<b>You rolled </b> {a}\n'
                              f'<b>You got </b>{mult*amount} {type} chip', parse_mode = ParseMode.HTML)
       DB.add_black(id , -amount)
       DB.add_black(id, mult*amount)
       DB.add_wager(id , amount)
       DB.add_rbblack(id , amount*multy)
      else:
       update.message.reply_text('Balance not enough')







DICE_HANDLER = CommandHandler('dice', dice)

dispatcher.add_handler(DICE_HANDLER)



