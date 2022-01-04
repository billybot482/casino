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
    '''Chat = update.effective_chat
    if update.effective_chat.type != Chat.PRIVATE:
       update.message.reply_text("Use in pm")
       return -1'''
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
    dog_quantity = DB.quantity_dog()
    fish_quantity = DB.quantity_fish()
    dog = 0
    fish = 0
    cat = 0
    for i in cat_quantity:
      for b in i:
        cat = b
        
    for i in dog_quantity:
      for b in i:
        dog = b    
        
    for i in fish_quantity:
      for b in i:
        fish = b    
        
        
    cd['slot'] = slot = DB.get_user_value(id , 'slots')
    cd['cs'] = current_slot = len(DB.get_pet(id))
    
    

    value = round((white*1)+(red*5)+(orange*25)+(yellow*100)+(blue*500)+(purple*2000)+(black*15000),4)
    keyboard = [
         [InlineKeyboardButton('cat', callback_data='cat')],
        [InlineKeyboardButton('dog', callback_data='dog')],
        [InlineKeyboardButton('fish', callback_data='fish')]
     ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    update.message.reply_text(f"Welcome {name} to the market 🏢\n<i>Here the list of things in sale</i>"
                              f"\n\n1.<b>Cat - 50🔵 </b>\nQuantity left : {cat}\n"
                              f"\n\n1.<b>Dog - 50🔵 </b>\nQuantity left : {dog}\n"
                              f"\n\n1.<b>Fish - 50🔵 </b>\nQuantity left : {fish}\n\n"
                              f'Press button below to buy', parse_mode = ParseMode.HTML, reply_markup = reply_markup)
    
    return ONE

def get_cat_tag(a):
  print(a)
  n = 0
  while n ==0:
   b = random.randint(1,999)
   if b not in a:
    return b
    n+=1
    
def get_dog_tag(a):
  print(a)
  n = 0
  while n ==0:
   b = random.randint(1,999)
   if b not in a:
    return b
    n+=1
    
def get_fish_tag(a):
  print(a)
  n = 0
  while n ==0:
   b = random.randint(1,999)
   if b not in a:
    return b
    n+=1

def cancel(update , context):
    cd = context.chat_data
    query = update.callback_query
    query.edit_message_text('exited market')
    return ConversationHandler.END

def buy_cat(update , context):
    cd = context.chat_data
    query = update.callback_query
    id = cd['id']
    a = DB.get_cat(id)
    a = get_cat_tag(a)
    talent = random.randint(5,30)
    distract = random.randint(5,30)
    confident = random.randint(50,200)
    cat_quantity = DB.quantity_cat()
    cat = 0
    for i in cat_quantity:
      for b in i:
        cat = b
    slot = cd['slot']
    cs = cd['cs']
    # max talent = 30
    # max distract = 30 
    # confident 200 
    tag = "#" + str(a).zfill(3)
    print(cq)
    blue = cd['blue']
    if slot > cs:
     if cat > 0:   
      if blue >=50:
         DB.add_pet_cat(id , a , talent , distract , confident)
         DB.sub_mint('cat', 1)
         DB.sub_chip(id,'blue',50)
         query.edit_message_text(f'🎊Congratulation !!🎊\nyou are now owner of <b>Cat {tag}</b>\n\n'
                                f'<i><b>stats of your pet:</b></i>\n'
                                f'🔆Talent : {talent}/30\n♨️Distract : {distract}/30\n❤‍🔥Confident : {confident}/200', parse_mode = ParseMode.HTML)
         return ConversationHandler.END
      else:
         query.answer('Balance not enough')
     else:
        query.answer('Out of stock')
    else:
        query.asnwer('Not enough slot')
    
def buy_dog(update , context):
    cd = context.chat_data
    query = update.callback_query
    id = cd['id']
    a = DB.get_dog(id)
    a = get_dog_tag(a)
    dog_quantity = DB.quantity_dog()
    dog = 0
    for i in dog_quantity:
      for b in i:
        dog = b
    talent = random.randint(5,40)
    distract = random.randint(5,30)
    confident = random.randint(30,150)
    slot = cd['slot']
    cs = cd['cs']
    # max talent = 40
    # max distract = 30 
    # confident 150
    tag = "#" + str(a).zfill(3)
    
    blue = cd['blue']
    if slot > cs:
     if dog > 0:
      if blue >=50:
         DB.add_pet_cat(id , a , talent , distract , confident)
         DB.sub_mint('dog')
         DB.sub_chip(id,'blue',50)
         query.edit_message_text(f'🎊Congratulation !!🎊\nyou are now owner of <b>Cat {tag}</b>\n\n'
                                f'<i><b>stats of your pet:</b></i>\n'
                                f'🔆Talent : {talent}/40\n♨️Distract : {distract}/30\n❤‍🔥Confident : {confident}/150', parse_mode = ParseMode.HTML)
         return ConversationHandler.END
      else:
         query.answer('Balance not enough')
     else:
        query.asnwer('Out of stock')
    else:
        query.asnwer('Not enough slot')
        
def buy_fish(update , context):
    cd = context.chat_data
    query = update.callback_query
    id = cd['id']
    a = DB.get_fish(id)
    a = get_fish_tag(a)
    fish_quantity = DB.quantity_fish()
    fish = 0
    for i in fish_quantity:
      for b in i:
        fish = b
    talent = random.randint(5,40)
    distract = random.randint(5,35)
    confident = random.randint(30,120)
    slot = cd['slot']
    cs = cd['cs']
    # max talent = 40
    # max distract = 35
    # confident 120
    tag = "#" + str(a).zfill(3)
    
    blue = cd['blue']
    if slot > cs:
     if fish > 0:
      if blue >=50:
         DB.add_pet_cat(id , a , talent , distract , confident)
         DB.sub_mint('cat', 1)
         DB.sub_chip(id,'blue',50)
         query.edit_message_text(f'🎊Congratulation !!🎊\nyou are now owner of <b>Fish {tag}</b>\n\n'
                                f'<i><b>stats of your pet:</b></i>\n'
                                f'🔆Talent : {talent}/40\n♨️Distract : {distract}/35\n❤‍🔥Confident : {confident}/120', parse_mode = ParseMode.HTML)
         return ConversationHandler.END
        
      else:
        query.answer('Balance not enough')
     else:   
        query.answer('Out of stock')
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
                  CallbackQueryHandler(buy_dog, pattern='^' + str("dog") + '$'),
                  CallbackQueryHandler(buy_fish, pattern='^' + str("fish") + '$'),
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
