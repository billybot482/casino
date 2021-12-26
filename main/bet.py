import logging
import random
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)
values = {'white': 1, 'red': 5, 'orange': 25, 'yellow': 100, 'blue': 500, 'purple': 2000, 'black': 15000}
colour = ['white', 'red', 'orange', 'yellow', 'blue', 'purple', 'black']
rb = ['rbwhite', 'rbred', 'rborange', 'rbyellow', 'rbblue', 'rbpurple', 'rbblack']

def bet(update, context):
    '''Chat = update.effective_chat
    if update.effective_chat.type != Chat.PRIVATE:
       update.message.reply_text("play in pm")
       return -1'''
    cd = context.chat_data
    query = update.callback_query
    id = update.effective_user.id
    name = update.effective_user.first_name
    username = update.effective_user.name
    VIP = DB.get_user_value(id, "vip")
    cd["white"] = white = DB.get_user_value(id, "white")
    cd["red"] = red = DB.get_user_value(id, "red")
    cd["orange"] = orange = DB.get_user_value(id, "orange")
    cd["yellow"] = yellow = DB.get_user_value(id, "yellow")
    cd["blue"] = blue = DB.get_user_value(id, "blue")
    cd["purple"] = purple = DB.get_user_value(id, "purple")
    cd["black"] = black = DB.get_user_value(id, "black")
    c = {1:white, 2:red, 3:orange, 4:yellow, 5:blue, 6:purple, 7:black}
    vip = int(VIP)
    mult = (((vip+1)/10)+(vip*0.2))/100
    n =1
    
    try:
     type = update.message.text.split()[1]
     amount = update.message.text.split()[2]
     amount = int(amount)
    except TypeError:
        return -1
    except IndexError:
        return -1
    except ValueError:
        return -1
    except AttributeError:
        return -1
    print('hi')
    for i in colour:
      if type in colour:
        if type == i:
          if amount <=c[n]:
            if amount >0:
              a = random.randint(1,2)
              if a ==1:
                DB.add_chip(id , i , amount)
                DB.add_rbchip(id ,rb[n-1] , mult*amount)
                DB.add_win(id , 1)
                DB.add_wager(id, amount*values[colour[n-1]])
                update.message.reply_text(f"Congrats, you won {amount} {type} chip") 
              else:
                DB.sub_chip(id , i , amount)
                DB.add_rbchip(id ,rb[n-1] , mult*amount)
                DB.add_loss(id , 1)
                DB.add_wager(id, amount*values[colour[n-1]])
                update.message.reply_text(f" Unfortunately you lost {amount} of {type} chip") 
            else:
             update.message.reply_text("Cannot bet negative or 0")
          else:
           update.message.reply_text("Not enough chip. consider do some /exchange or get some donation")
      if type not in colour:
       update.message.reply_text(f"Available option \n{colour}") 
 
    
    



BET_HANDLER = CommandHandler('bet', bet)
dispatcher.add_handler(BET_HANDLER)
