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
    cd["worth"] = worth = DB.get_user_value(id, "worth")
    cd["white"] = white = DB.get_user_value(id, "white")
    cd["red"] = red = DB.get_user_value(id, "red")
    cd["orange"] = orange = DB.get_user_value(id, "orange")
    cd["yellow"] = yellow = DB.get_user_value(id, "yellow")
    cd["blue"] = blue = DB.get_user_value(id, "blue")
    cd["purple"] = purple = DB.get_user_value(id, "purple")
    cd["black"] = black = DB.get_user_value(id, "black")
    print("test2") 
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
'''
    if type in colour:
     if type == "black":
      if amount <= black:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_black(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} ⚫ Black chip") 
        else:
         DB.add_black(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of ⚫ Black chip") 
       else:
        update.message.reply_text("Cannot bet negative or 0")
      else:
       update.message.reply_text("Not enough ⚫ black chip, consider do some /exchange or get some donation")
     else:
      update.message.reply_text(f"Available option \n{colour}") 
    else:
     update.message.reply_text("use format /bet <type of chip> <amount>") 
        

    if type in colour:
     if type == "purple":
      if amount <= purple:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_purple(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} 🟣 purple chip") 
        else:
         DB.add_purple(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of 🟣 purple chip") 
       else:
        update.message.reply_text("Cannot bet negative or 0")
      else:
       update.message.reply_text("Not enough 🟣 purple chip , consider do some /exchange or get some donation")
     else:
      update.message.reply_text(f"Available option \n{colour}") 
    else:
     update.message.reply_text("use format /bet <type of chip> <amount>") 
        

    if type in colour:
     if type == "blue":
      if amount <= blue:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_blue(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} 🔵 blue chip") 
        else:
         DB.add_blue(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of 🔵 blue chip") 
       else:
        update.message.reply_text("Cannot bet negative or 0")
      else:
       update.message.reply_text("Not enough 🔵 blue chip, consider do some /exchange or get some donation")
     else:
      update.message.reply_text(f"Available option \n{colour}") 
    else:
     update.message.reply_text("use format /bet <type of chip> <amount>") 
        

    if type in colour:
     if type == "yellow":
      if amount <= yellow:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_yellow(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} 🟡 yellow chip") 
        else:
         DB.add_yellow(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of 🟡 yellow chip") 
       else:
        update.message.reply_text("Cannot bet negative or 0")
      else:
       update.message.reply_text("Not enough 🟡 yellow chip, consider do some /exchange or get some donation")
     else:
      update.message.reply_text(f"Available option \n{colour}") 
    else:
     update.message.reply_text("use format /bet <type of chip> <amount>") 
        

    if type in colour:
     if type == "orange":
      if amount <= orange:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_orange(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} 🟠 orange chip") 
        else:
         DB.add_orange(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of 🟠 orange chip") 
       else:
        update.message.reply_text("Cannot bet negative or 0")
      else:
       update.message.reply_text("Not enough 🟠 orange chip, consider do some /exchange or get some donation")
     else:
      update.message.reply_text(f"Available option \n{colour}") 
    else:
     update.message.reply_text("use format /bet <type of chip> <amount>") 
        

    if type in colour:
     if type == "red":
      if amount <= red:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_red(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} 🔴 Red chip") 
        else:
         DB.add_red(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of 🔴 Red chip") 
       else:
        update.message.reply_text("Cannot bet negative or 0")
      else:
       update.message.reply_text("Not enough 🔴 red chip, consider do some /exchange or get some donation")
     else:
      update.message.reply_text(f"Available option \n{colour}") 
    else:
     update.message.reply_text("use format /bet <type of chip> <amount>") 
 '''      

   if type in colour:
     if type == "white":
      if amount <= white:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_white(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} ⚪ White chip") 
        else:
         DB.add_white(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of ⚪ White chip") 
     if type == "red":
      if amount <= red:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_red(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} 🔴 Red chip") 
        else:
         DB.add_red(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of 🔴 Red chip") 
     if type == "orange":
      if amount <= orange:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_orange(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} 🟠 orange chip") 
        else:
         DB.add_orange(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of 🟠 orange chip") 
     if type == "yellow":
      if amount <= yellow:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_yellow(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} 🟡 yellow chip") 
        else:
         DB.add_yellow(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of 🟡 yellow chip") 
     if type == "blue":
      if amount <= blue:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_blue(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} 🔵 blue chip") 
        else:
         DB.add_blue(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of 🔵 blue chip") 
     if type == "purple":
      if amount <= purple:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_purple(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} 🟣 purple chip") 
        else:
         DB.add_purple(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of 🟣 purple chip") 
     if type == "black":
      if amount <= black:
       if amount >0:
        a = random.randint(1,2)
        if a == 1:
         DB.add_black(id , amount)
         update.message.reply_text(f"Congrats, you won {amount} ⚫ Black chip") 
        else:
         DB.add_black(id , -amount)
         update.message.reply_text(f" Unfortunately you lost {amount} of ⚫ Black chip") 

       else:
        update.message.reply_text("Cannot bet negative or 0")
      else:
       update.message.reply_text("Not enough chip. consider do some /exchange or get some donation")
     else:
      update.message.reply_text(f"Available option \n{colour}") 
    else:
     update.message.reply_text("use format /bet <type of chip> <amount>") 
    
    



BET_HANDLER = CommandHandler('bet', bet)
dispatcher.add_handler(BET_HANDLER)
