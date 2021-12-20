import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
import random
from main import wheel, dispatcher, bet , airdrop, pet, market, janken, cash, stocks
import os
from telegram.ext.dispatcher import run_async
from main import database as DB
from queue import Queue

DB_PATH=os.environ['DATABASE_URL']
DB.init(DB_PATH)
DB.setup()

#state
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)
#callback data
S_START , S_INCREASE ,S_POP , SS_POP, FIRST , SECOND ,THIRD,CHECK, SHOW, *_ = range(1000)
owners = [163494588]
sudo = []

def start(update , context):
    id = update.effective_user.id
    name = update.effective_user.first_name
    username = update.effective_user.name
    user_registered = DB.get_user_value(id, "COUNT(*)")

    if user_registered:
     return

    text = f"Welcome <b>{name}</b> to <u><b><i>Casino 482</i></b></u>\n\n" \
           f"We have registered you under our player lists with your below information\n" \
           f"\n# username : <code>{username}</code>\n# ID : <code>{id}</code>"
    context.bot.send_photo(chat_id = update.effective_chat.id, caption = text , photo = "https://telegra.ph/file/b50d95b7d42b2f866fcac.jpg", parse_mode=ParseMode.HTML)
    DB.add_user(id)

def games(update , context):
    text = "<b><u>Available Games</u></b>\n\n/Dice\n/Hilo\n/Blackjack\n/Wheel"
    context.bot.send_message(chat_id = update.effective_chat.id, text = text, parse_mode = ParseMode.HTML)

def value(update , context):
    text = "<b><u>Values of each chips</u></b>\n\n⚪️ white chip : 1$\n" \
           "🔴 red chip : 5$\n🟠 orange chip : 25$\n🟡 yellow chip : 100$\n🔵 blue chip : 500$" \
           "\n🟣 purple chip : 2000$\n⚫️ black chip : 15000$"
    context.bot.send_message(chat_id = update.effective_chat.id , text = text, parse_mode = ParseMode.HTML)
 
def rakeback(update, context):
    cd = context.chat_data
    query = update.callback_query
    id = update.effective_user.id
    VIP = DB.get_user_value(id, "vip")
    cd['id'] = id
    name = update.effective_user.first_name
    cd['white'] = rbwhite = round(DB.get_user_value(id, "rbwhite"),4)
    cd['red'] =  rbred = round(DB.get_user_value(id, "rbred"),4)
    cd['orange'] = rborange = round(DB.get_user_value(id, "rborange"),4)
    cd['yellow'] = rbyellow = round(DB.get_user_value(id, "rbyellow"),4)
    cd['blue'] = rbblue = round(DB.get_user_value(id, "rbblue"),4)
    cd['purple'] = rbpurple = round(DB.get_user_value(id, "rbpurple"),4)
    cd['black'] = rbblack = round(DB.get_user_value(id, "rbblack"),4)
    value = round((rbwhite*1)+(rbred*5)+(rborange*25)+(rbyellow*100)+(rbblue*500)+(rbpurple*2000)+(rbblack*15000),4)
    vip = int(VIP)
    mult = ((vip+1)/10)+(0.2*vip)
    
    keyboard = [
         [InlineKeyboardButton('claim', callback_data='claim'),InlineKeyboardButton('cancel', callback_data='cancel')]
     ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
     update.message.reply_text(f"<u><b>{name}'s Rakeback account</b></u>\n"
                              f"🎖 VIP : {VIP}\n"
                              f"Rakeback percent : {mult}%\n\n"
                              f"<b>⚪️White Chip</b> : {rbwhite}\n"
                              f"<b>🔴Red Chip</b> : {rbred}\n"
                              f"<b>🟠Orange Chip</b> : {rborange}\n"
                              f"<b>🟡Yellow Chip</b> : {rbyellow}\n"
                              f"<b>🔵Blue Chip</b> : {rbblue}\n"
                              f"<b>🟣Purple Chip</b> : {rbpurple}\n"
                              f"<b>⚫Black Chip</b> : {rbblack}\n\n"
                              f"<i>Total worth Worth</i> : {value}$\n"
                              f"click claim below to claim all rakeback to your main wallet or cancel if you do not wish to claim it",
                              parse_mode=ParseMode.HTML, reply_markup = reply_markup)
    except TypeError:
     update.message.reply_text('start the bot /start')
    
    return FOUR

def rakeback3(update , context):
    cd = context.chat_data
    query = update.callback_query
    query.edit_message_text('closed')
    return ConversationHandler.END
    

def rakeback2(update , context):
    cd = context.chat_data
    query = update.callback_query
    id = cd['id']
    white = cd['white']
    red = cd['red']
    orange = cd['orange']
    yellow = cd['yellow']
    blue = cd['blue']
    purple = cd['purple']
    black = cd['black']
    
    query.edit_message_text('rakeback has been added to your main wallet')
    DB.add_white(id , white)
    DB.add_rbwhite(id , -white)
    
    DB.add_red(id , red)
    DB.add_rbred(id , -red)
    
    DB.add_orange(id , orange)
    DB.add_rborange(id , -orange)
    
    DB.add_yellow(id , yellow)
    DB.add_rbyellow(id , -yellow)
    
    DB.add_blue(id , blue)
    DB.add_rbblue(id , -blue)
    
    DB.add_purple(id , purple)
    DB.add_rbpurple(id , -purple)
    
    DB.add_black(id , black)
    DB.add_rbblack(id , -black)
    
    return ConversationHandler.END

def calculate_worth(white=0, red=0, orange=0, yellow=0, blue=0, purple=0, black=0):
    return round((white*1)+(red*5)+(orange*25)+(yellow*100)+(blue*500)+(purple*2000)+(black*15000),4)

def system(update , context):
    member = DB.get_all_value("user_id")
    w,r,o,y,b,p,bbb=0,0,0,0,0,0,0
    ww,ll = 0,0
    white = DB.get_all_value("white")
    red = DB.get_all_value("red")
    orange = DB.get_all_value("orange")
    yellow = DB.get_all_value("yellow")
    blue = DB.get_all_value("blue")
    purple = DB.get_all_value("purple")
    black = DB.get_all_value("black")
    win = DB.get_all_value("win")
    loss = DB.get_all_value("loss")
    stock = DB.get_stock()
    stock = len(stock)
    
    for aa in white:
        for bb in aa:
            w+=int(bb)
    for aa in red:
        for bb in aa:
            r+=int(bb)
    for aa in orange:
        for bb in aa:
            o+=int(bb)
    for aa in yellow:
        for bb in aa:
            y+=int(bb)
    for aa in blue:
        for bb in aa:
            b+=int(bb)
    for aa in purple:
        for bb in aa:
            p+=int(bb)
    for aa in black:
        for bb in aa:
            bbb+=int(bb)
    for aa in win:
        for bb in aa:
            ww+=int(bb)
    for aa in loss:
        for bb in aa:
            ll+=int(bb)
            
    tt = w+r+o+y+b+p+bbb        
    
    update.message.reply_text(f'<b><u>system data</u></b>\n'
                              f'<b>┗━Total chips in circulations</b>\n'
                              f'<b>┃    ⚪️White </b>: {w}\n'
                              f'<b>┃    🔴Red</b>: {r}\n'
                              f'<b>┃    🟠Orange</b>: {o}\n'
                              f'<b>┃    🟡Yellow</b>: {y}\n'
                              f'<b>┃    🔵Blue</b>: {b}\n'
                              f'<b>┃    🟣Purple</b>: {p}\n'
                              f'<b>┃    ⚫Black</b>: {bbb}\n┃\n'
                              f'<b>┗Total members : {len(member)}</b>\n'
                              f'<b>┗Circulating value: {tt}$</b>\n'
                              f'<b>┗Total stock : {stock}</b>\n'
                              f'<b>┗Total game played : {ww+ll}</b>\n'
                              f'<b>┗Total pet in game: Na</b>', parse_mode = ParseMode.HTML)
    
  
def wallet(update , context):
    id = update.effective_user.id
    name = update.effective_user.first_name
    username = update.effective_user.name
    VIP = DB.get_user_value(id, "vip")
    white = round(DB.get_user_value(id, "white"),4)
    red = round(DB.get_user_value(id, "red"),4)
    orange = round(DB.get_user_value(id, "orange"),4)
    yellow = round(DB.get_user_value(id, "yellow"),4)
    blue = round(DB.get_user_value(id, "blue"),4)
    purple = round(DB.get_user_value(id, "purple"),4)
    black = round(DB.get_user_value(id, "black"),4)

    value = calculate_worth(white, red, orange, yellow, blue, purple, black)
    try:
     update.message.reply_text(f"<u><b>{name}'s Wallet</b></u>\n"
                              f"🎖 VIP : {VIP}\n\n"
                              f"<b>⚪️White Chip</b> : {white}\n"
                              f"<b>🔴Red Chip</b> : {red}\n"
                              f"<b>🟠Orange Chip</b> : {orange}\n"
                              f"<b>🟡Yellow Chip</b> : {yellow}\n"
                              f"<b>🔵Blue Chip</b> : {blue}\n"
                              f"<b>🟣Purple Chip</b> : {purple}\n"
                              f"<b>⚫Black Chip</b> : {black}\n\n"
                              f"<i>Net Worth</i> : {value}$",
                              parse_mode=ParseMode.HTML)
    except TypeError:
     update.message.reply_text('start the bot /start')

    
def exec(update , context):
    type = update.message.text.split()[1]
    value = update.message.text.split()[2]
    avalue = int(value)
    id = update.effective_user.id
    name = update.effective_user.first_name
    to_id = update.message.reply_to_message.from_user.id
    to_name = update.message.reply_to_message.from_user.first_name
    vip = DB.get_user_value(to_id, 'vip')
   
    if id in owners:
     if type == 'vip':
      if vip <10 and (vip+avalue)<=10:
       DB.add_vip(to_id , value)
       update.message.reply_text(f'<b>Call by :</b> {name}\n<b>Position :</b> Owner ✪ ✪ ✪ \n<b>Execution Type :</b> Increase VIP\nFrom VIP <b>{vip}</b> to VIP <b>{vip+avalue}</b>\n\n<b>Status :</b> Completed ✅\n{to_name} is now VIP <b>{vip+avalue}</b>',parse_mode=ParseMode.HTML )
      else: 
        update.message.reply_text('this person is already VIP10 🎖 which is maximum VIP\nOr will be Over 10 is you promote this much')
        return -1
     if type == 'sudo':
        if value == '1':
         sudo.append(to_id)
         update.message.reply_text(f'<b>Call by :</b> {name}\n'
                              f'<b>Position :</b> Owner ✪ ✪ ✪ \n'
                              f'<b>Execution Type :</b> promotion to High Table\n'
                              f'<b>Candidate</b> : {to_name}n\n'
                              f'<b>Status :</b> Completed ✅\n'
                              f'{to_name} is now part of High Table', parse_mode=ParseMode.HTML)
    elif id in sudo:
     if type == 'vip': 
      if vip<10 and (vip+avalue)<=10:
       DB.add_vip(to_id , value)
       update.message.reply_text(f'<b>Call by :</b> {name}\n<b>Position :</b> High Table ✪✪\n<b>Execution Type :</b> Increase VIP\nFrom VIP <b>{vip}</b> to VIP <b>{vip+avalue}</b>\n\n<b>Status :</b> Completed ✅',parse_mode=ParseMode.HTML )
      else: 
        update.message.reply_text('this person is already VIP10 🎖 which is maximum VIP\nOr will be Over 10 is you promote this much')
        return -1
    
    elif vip >0:
       update.message.reply_text(f'<b>Call by :</b> {name}\n<b>Position :</b> VIP {vip} ✪ \n<b>Execution Type :</b> Increase VIP\nFrom VIP <b>{vip}</b> to VIP <b>{vip+avalue}</b>\n\n<b>Status :</b> Failed ❌',parse_mode=ParseMode.HTML)
       return -1
                                 
    elif vip ==0:
       update.message.reply_text(f'<b>Call by :</b> {name}\n<b>Position :</b> member\n<b>Execution Type :</b> Increase VIP\nFrom VIP <b>{vip}</b> to VIP <b>{vip+avalue}</b>\n\n<b>Status :</b> Failed ❌',parse_mode=ParseMode.HTML)
       return -1
        
     
    
def statistic(update, context):
    id = update.effective_user.id
    name = update.effective_user.first_name
    username = update.effective_user.name
    wager = DB.get_user_value(id , "wager")
    win = DB.get_user_value(id , "win")
    loss = DB.get_user_value(id , "loss")
    vip = DB.get_user_value(id, "vip")
    white = round(DB.get_user_value(id, "white"),4)
    red = round(DB.get_user_value(id, "red"),4)
    orange = round(DB.get_user_value(id, "orange"),4)
    yellow = round(DB.get_user_value(id, "yellow"),4)
    blue = round(DB.get_user_value(id, "blue"),4)
    purple = round(DB.get_user_value(id, "purple"),4)
    black = round(DB.get_user_value(id, "black"),4)
    pet_count = 0
    try:
        ratio = round(((win/loss)/2)*100,2)
        winrate = round(win/(win+loss)*100,2) 
        lossrate = round(loss/(win+loss)*100,2)
    except ZeroDivisionError:
        ratio = 'NA'
        winrate = 'NA'
        lossrate = 'NA'

    value = (white*1)+(red*5)+(orange*25)+(yellow*100)+(blue*500)+(purple*2000)+(black*15000)
    
    update.message.reply_text(f'<b><u>statistic of {name}</u></b>\n\n'
                              f'<b>🎖 VIP  : {vip}</b>\n'
                              f'<b>★ Current assets :</b> {value}$ \n'
                              f'<b>★ Total wagered :</b> {wager}$\n'
                              f'<b>★ Total win :</b> {win}\n'
                              f'<b>★ Total loss : </b>{loss}\n'
                              f'<b>★ Win rate : </b>{winrate}%\n'
                              f'<b>★ Loss rate : </b>{lossrate}%\n'
                              f'<b>★ Ratio : </b>{ratio}%\n\n'
                              f'<b>💫 Pet owned : </b>{pet_count}', parse_mode = ParseMode.HTML)
    
                
def gift(update , context):
    if not update.message.reply_to_message:
             update.message.reply_text('reply to someone')
             return
    user_name = update.message.from_user.first_name
    to = update.message.reply_to_message.from_user.first_name
    user_id = update.message.reply_to_message.from_user.id
    id = update.message.from_user.id
    if id in owners:
        DB.add_white(user_id , 100)
        DB.add_red(user_id , 100)
        DB.add_orange(user_id , 50)
        DB.add_yellow(user_id , 30) 
        DB.add_blue(user_id , 10)
        update.message.reply_text("Gift added in batch of 100 white, 100 red, 50 orange, 30 yellow and 10 blue chips.") 
    else:
        update.message.reply_text('Not authorised')

        
        
def add(update , context):
    if not update.message.reply_to_message:
             update.message.reply_text('reply to someone')
             return
    type = update.message.text.split()[1]
    units = update.message.text.split()[2]
    user_name = update.message.from_user.first_name
    to = update.message.reply_to_message.from_user.first_name
    user_id = update.message.reply_to_message.from_user.id
    id = update.message.from_user.id

    a = context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=update.effective_user.id).status
    msg = int(units)
    if id in owners:
        if type == "white":
         DB.add_white(user_id, units)
         update.message.reply_text(f'{to} received {units}  ⚪️ white chips')
        if type == "red":
         DB.add_red(user_id, units)
         update.message.reply_text(f'{to} received {units}  🔴 red chips')
        if type == "orange":
         DB.add_orange(user_id, units)
         update.message.reply_text(f'{to} received {units}  🟠 orange chips')
        if type == "yellow":
         DB.add_yellow(user_id, units)
         update.message.reply_text(f'{to} received {units} 🟡 yellow chips')
        if type == "blue":
         DB.add_blue(user_id, units)
         update.message.reply_text(f'{to} received {units} 🔵 blue chips')
        if type == "purple":
         DB.add_purple(user_id, units)
         update.message.reply_text(f'{to} received {units} 🟣 purple chips')
        if type == "black":
         DB.add_black(user_id, units)
         update.message.reply_text(f'{to} received {units} ⚫️ black chips')
    else:
         update.message.reply_text('not authorized')
         return -1

        
def swap(update , context):
    cd = context.chat_data
    query = update.callback_query
    id = update.effective_user.id
    name = update.effective_user.first_name
    username = update.effective_user.name
    queue = cd.get("queue", False)
    cd["queue"] = Queue() if not queue else queue

    if cd["queue"].qsize():
        cd["queue"].get().delete()

    cd["white"] = white = DB.get_user_value(id, "white")
    cd["red"] = red = DB.get_user_value(id, "red")
    cd["orange"] = orange = DB.get_user_value(id, "orange")
    cd["yellow"] = yellow = DB.get_user_value(id, "yellow")
    cd["blue"] = blue = DB.get_user_value(id, "blue")
    cd["purple"] = purple = DB.get_user_value(id, "purple")
    cd["black"] = black = DB.get_user_value(id, "black")
    colour = ['white', 'red', 'orange', 'yellow', 'blue', 'purple', 'black']

    values = {'white': 1, 'red': 5, 'orange': 25, 'yellow': 100, 'blue': 500, 'purple': 2000, 'black': 15000}

    try:
     cd['type'] = type = update.message.text.split()[1]
     cd['units'] = units = int(update.message.text.split()[2])

     cd['exwhite'] = exwhite  = round(units/values['white'],4)
     cd['exred'] = exred = round(units/values['red'], 4)
     cd['exorange'] = exorange = round(units / values['orange'], 4)
     cd['exyellow'] = exyellow = round(units / values['yellow'], 4)

     cd['ex2white'] = ex2white = round(units * values['red'], 4)
     cd['ex2red'] = ex2red = round(units / values['white'], 4)
     cd['ex2orange'] = ex2orange = round(values['red'] / values['orange']*units, 4)
     cd['ex2yellow'] = ex2yellow = round(values['red'] / values['yellow']*units, 4)
     cd['ex2blue'] = ex2blue = round(values['red'] / values['blue']*units, 4)

     cd['ex3white'] = ex3white = round(values['orange'] / values['white']*units, 4)
     cd['ex3red'] = ex3red = round(values['orange'] / values['red']*units, 4)
     cd['ex3orange'] =ex3orange = round(values['orange'] / values['orange']*units, 4)
     cd['ex3yellow'] =ex3yellow = round(values['orange'] / values['yellow']*units, 4)
     cd['ex3blue'] =ex3blue = round(values['orange'] / values['blue']*units, 4)
     cd['ex3purple'] = ex3purple = round(values['orange'] / values['purple']*units, 4)

     cd['ex4white'] = ex4white = round(values['yellow'] / values['white']*units, 4)
     cd['ex4red'] = ex4red = round(values['yellow'] / values['red']*units, 4)
     cd['ex4orange'] = ex4orange = round(values['yellow'] / values['orange']*units, 4)
     cd['ex4yellow'] = ex4yellow = round(values['yellow'] / values['yellow']*units, 4)
     cd['ex4blue'] = ex4blue = round(values['yellow'] / values['blue']*units, 4)
     cd['ex4purple'] = ex4purple = round(values['yellow'] / values['purple']*units, 4)
     cd['ex4black'] = ex4black = round(values['yellow'] / values['black']*units, 4)

     cd['ex5white'] = ex5white = round(values['blue'] / values['white']*units, 4)
     cd['ex5red'] =ex5red = round(values['blue'] / values['red']*units, 4)
     cd['ex5orange'] = ex5orange = round(values['blue'] / values['orange']*units, 4)
     cd['ex5yellow'] =ex5yellow = round(values['blue'] / values['yellow']*units, 4)
     cd['ex5blue'] = ex5blue = round(values['blue'] / values['blue']*units, 4)
     cd['ex5purple'] = ex5purple = round(values['blue'] / values['purple']*units, 4)
     cd['ex5black'] =ex5black = round(values['blue'] / values['black']*units, 4)

     cd['ex6white'] =ex6white = round(values['purple'] / values['white']*units, 4)
     cd['ex6red'] = ex6red =  round(values['purple'] / values['red']*units, 4)
     cd['ex6orange'] =ex6orange =  round(values['purple'] / values['orange']*units, 4)
     cd['ex6yellow'] =ex6yellow =  round(values['purple'] / values['yellow']*units, 4)
     cd['ex6blue'] =ex6blue =  round(values['purple'] / values['blue']*units, 4)
     cd['ex6purple'] =ex6purple =  round(values['purple'] / values['purple']*units, 4)
     cd['ex6black'] =ex6black =  round(values['purple'] / values['black']*units, 4)

     cd['ex7white'] = ex7white =  round(values['black'] / values['white']*units, 4)
     cd['ex7red'] =ex7red = round(values['black'] / values['red']*units, 4)
     cd['ex7orange'] =ex7orange = round(values['black'] / values['orange']*units, 4)
     cd['ex7yellow'] = ex7yellow = round(values['black'] / values['yellow']*units, 4)
     cd['ex7blue'] = ex7blue = round(values['black'] / values['blue']*units, 4)
     cd['ex7purple'] =ex7purple = round(values['black'] / values['purple']*units, 4)
     cd['ex7black'] =ex7black = round(values['black'] / values['black']*units, 4)

     keyboard1 = [
         [InlineKeyboardButton(f'{exwhite} ⚪', callback_data='white'),InlineKeyboardButton(f'{exred} 🔴', callback_data='red')],
         [InlineKeyboardButton(f'{exorange} 🟠', callback_data='orange'),InlineKeyboardButton(f'{exyellow} 🟡', callback_data='yellow')],
     ]
     reply_markup1 = InlineKeyboardMarkup(keyboard1)

     keyboard2 = [
         [InlineKeyboardButton(f'{ex2white} ⚪', callback_data='white2'),
          InlineKeyboardButton(f'{ex2red} 🔴', callback_data='red2')],
         [InlineKeyboardButton(f'{ex2orange} 🟠', callback_data='orange2'),
          InlineKeyboardButton(f'{ex2yellow} 🟡', callback_data='yellow2')],
         [InlineKeyboardButton(f'{ex2blue} 🔵', callback_data='blue2'),]
     ]
     reply_markup2 = InlineKeyboardMarkup(keyboard2)

     keyboard3 = [
         [InlineKeyboardButton(f'{ex3white} ⚪', callback_data='white3'),
          InlineKeyboardButton(f'{ex3red} 🔴', callback_data='red3')],
         [InlineKeyboardButton(f'{ex3orange} 🟠', callback_data='orange3'),
          InlineKeyboardButton(f'{ex3yellow} 🟡', callback_data='yellow3')],
         [InlineKeyboardButton(f'{ex3blue} 🔵', callback_data='blue3'),
          InlineKeyboardButton(f'{ex3purple} 🟣', callback_data='purple3')],
     ]
     reply_markup3 = InlineKeyboardMarkup(keyboard3)

     keyboard4 = [
         [InlineKeyboardButton(f'{ex4white} ⚪', callback_data='white4'),
          InlineKeyboardButton(f'{ex4red} 🔴', callback_data='red4')],
         [InlineKeyboardButton(f'{ex4orange} 🟠', callback_data='orange4'),
          InlineKeyboardButton(f'{ex4yellow} 🟡', callback_data='yellow4')],
         [InlineKeyboardButton(f'{ex4blue} 🔵', callback_data='blue4'),
          InlineKeyboardButton(f'{ex4purple} 🟣', callback_data='purple4')],
         [InlineKeyboardButton(f'{ex4black} ⚫', callback_data='black4'), ]
     ]
     reply_markup4 = InlineKeyboardMarkup(keyboard4)

     keyboard5 = [
         [InlineKeyboardButton(f'{ex5white} ⚪', callback_data='white5'),
          InlineKeyboardButton(f'{ex5red} 🔴', callback_data='red5')],
         [InlineKeyboardButton(f'{ex5orange} 🟠', callback_data='orange5'),
          InlineKeyboardButton(f'{ex5yellow} 🟡', callback_data='yellow5')],
         [InlineKeyboardButton(f'{ex5blue} 🔵', callback_data='blue5'),
          InlineKeyboardButton(f'{ex5purple} 🟣', callback_data='purple5')],
         [InlineKeyboardButton(f'{ex5black} ⚫', callback_data='black5'), ]
     ]
     reply_markup5 = InlineKeyboardMarkup(keyboard5)

     keyboard6 = [
         [InlineKeyboardButton(f'{ex6white} ⚪', callback_data='white6'),
          InlineKeyboardButton(f'{ex6red} 🔴', callback_data='red6')],
         [InlineKeyboardButton(f'{ex6orange} 🟠', callback_data='orange6'),
          InlineKeyboardButton(f'{ex6yellow} 🟡', callback_data='yellow6')],
         [InlineKeyboardButton(f'{ex6blue} 🔵', callback_data='blue6'),
          InlineKeyboardButton(f'{ex6purple} 🟣', callback_data='purple6')],
         [InlineKeyboardButton(f'{ex6black} ⚫', callback_data='black6'), ]
     ]
     reply_markup6 = InlineKeyboardMarkup(keyboard6)

     keyboard7 = [
         [InlineKeyboardButton(f'{ex7white} ⚪', callback_data='white7'),
          InlineKeyboardButton(f'{ex7red} 🔴', callback_data='red7')],
         [InlineKeyboardButton(f'{ex7orange} 🟠', callback_data='orange7'),
          InlineKeyboardButton(f'{ex7yellow} 🟡', callback_data='yellow7')],
         [InlineKeyboardButton(f'{ex7blue} 🔵', callback_data='blue7'),
          InlineKeyboardButton(f'{ex7purple} 🟣', callback_data='purple7')],
         [InlineKeyboardButton(f'{ex7black} ⚫', callback_data='black7'), ]
     ]
     reply_markup7 = InlineKeyboardMarkup(keyboard7)

     markups = [reply_markup1, reply_markup2,
                  reply_markup3, reply_markup4,
                  reply_markup5, reply_markup6,
                  reply_markup7]

     type = type.lower()
     if type not in colour:
        update.message.reply_text(f"please type either\n\n{colour}")
     if units > cd[type]:
        update.message.reply_text('You dont have enough to do this conversion')
     if units <= cd[type] and units > 0:
        msg = update.message.reply_text(f'Exchange <b>{units}</b> {type} chip for : \n\n', reply_markup=markups[colour.index(type)], parse_mode = ParseMode.HTML)
        cd["queue"].put(msg)
     if units < 0:
        update.message.reply_text('You cannot exchange negative , make sure it is larger than 1')
    except IndexError:
        update.message.reply_text("use this format\n\n/swap <type of chip> <amount>")
    return THREE

def exchange2(update , context):
    cd = context.chat_data
    query = update.callback_query
    id = update.effective_user.id
    name = update.effective_user.first_name
    username = update.effective_user.name
    VIP = DB.get_user_value(id, "vip")
    cd["white"] = white = DB.get_user_value( id, "white")
    cd["red"] = red = DB.get_user_value(id, "red")
    cd["orange"] = orange = DB.get_user_value(id, "orange")
    cd["yellow"] = yellow = DB.get_user_value( id, "yellow")
    cd["blue"] = blue = DB.get_user_value( id, "blue")
    cd["purple"] = purple = DB.get_user_value( id, "purple")
    cd["black"] = black = DB.get_user_value( id, "black")

    white = cd['exwhite'] #EXCHANGED TO AMOUNT (INT)
    red = cd['exred']
    orange = cd['exorange']
    yellow = cd['exyellow']

    white2 = cd['ex2white']
    red2 = cd['ex2red']
    orange2 = cd['ex2orange']
    yellow2 = cd['ex2yellow']
    blue2 =cd['ex2blue']

    white3 = cd['ex3white']
    red3 =cd['ex3red']
    orange3 = cd['ex3orange']
    yellow3 = cd['ex3yellow']
    blue3 = cd['ex3blue']
    purple3 = cd['ex3purple']

    white4 = cd['ex4white']
    red4 = cd['ex4red']
    orange4 = cd['ex4orange']
    yellow4 = cd['ex4yellow']
    blue4 = cd['ex4blue']
    purple4 = cd['ex4purple']
    black4 = cd['ex4black']

    white5 = cd['ex5white']
    red5 = cd['ex5red']
    orange5 = cd['ex5orange']
    yellow5 = cd['ex5yellow']
    blue5 = cd['ex5blue']
    purple5 = cd['ex5purple']
    black5 = cd['ex5black']

    white6 = cd['ex6white']
    red6 = cd['ex6red']
    orange6 = cd['ex6orange']
    yellow6 = cd['ex6yellow']
    blue6 = cd['ex6blue']
    purple6 = cd['ex6purple']
    black6 = cd['ex6black']

    white7 = cd['ex7white']
    red7 = cd['ex7red']
    orange7 = cd['ex7orange']
    yellow7 = cd['ex7yellow']
    blue7 = cd['ex7blue']
    purple7 = cd['ex7purple']
    black7 = cd['ex7black']

    type = cd['type']
    units =cd['units']

    if query.data == 'white':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {white} white chip')
        DB.add_white(id , white) # minus
        DB.add_white(id , -white) # add
    if query.data == 'red':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {red} red chip')
        DB.add_white(id , -white) # minus
        DB.add_red(id , red) # add
    if query.data == 'orange':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {orange} orange chip')
        DB.add_white(id , -white) # minus
        DB.add_orange(id , orange) # add
    if query.data == 'yellow':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {yellow} yellow chip')
        DB.add_white(id , -white) # minus
        DB.add_yellow(id , yellow) # add
    if query.data == 'white2':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {white2} white chip')
        DB.add_red(id , -red2) # minus
        DB.add_white(id , white2) # add
    if query.data == 'red2':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {red2} red chip')
        DB.add_red(id , -red2) # minus
        DB.add_red(id , red2) # add
    if query.data == 'orange2':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {orange2} orange chip')
        DB.add_red(id , -red2) # minus
        DB.add_orange(id , orange2) # add
    if query.data == 'yellow2':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {yellow2} yellow chip')
        DB.add_red(id , -red2) # minus
        DB.add_yellow( id , yellow2) # add
    if query.data == 'blue2':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {blue2} blue chip')
        DB.add_red(id , -red2) # minus
        DB.add_blue(id , blue2) # add
    if query.data == 'white3':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {white3} white chip')
        DB.add_orange(id , -orange3) # minus
        DB.add_white(id , white3) # add
    if query.data == 'red3':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {red3} red chip')
        DB.add_orange(id , -orange3) # minus
        DB.add_red(id , red3) # add
    if query.data == 'orange3':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {orange2} orange chip')
        DB.add_orange(id , -orange3) # minus
        DB.add_orange(id , orange3) # add
    if query.data == 'yellow3':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {yellow3} yellow chip')
        DB.add_orange(id , -orange3) # minus
        DB.add_yellow( id , yellow3) # add
    if query.data == 'blue3':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {blue3} blue chip')
        DB.add_orange(id , -orange3) # minus
        DB.add_blue( id , blue3) # add
    if query.data == 'purple3':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {purple3} purple chip')
        DB.add_orange(id , -orange3) # minus
        DB.add_purple( id , purple3) # add
    if query.data == 'white4':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {white4} white chip')
        DB.add_yellow( id , -yellow4) # minus
        DB.add_white( id , white4) # add
    if query.data == 'red4':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {red4} red chip')
        DB.add_yellow(id , -yellow4) # minus
        DB.add_red(id , red4) # add
    if query.data == 'orange4':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {orange4} orange chip')
        DB.add_yellow(id , -yellow4) # minus
        DB.add_orange( id , orange4) # add
    if query.data == 'yellow4':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {yellow4} yellow chip')
        DB.add_yellow(id , -yellow4) # minus
        DB.add_yellow(id , yellow4) # add
    if query.data == 'blue4':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {blue4} blue chip')
        DB.add_yellow(id , -yellow4) # minus
        DB.add_blue(id , blue4) # add
    if query.data == 'purple4':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {purple4} purple chip')
        DB.add_yellow(id , -yellow4) # minus
        DB.add_purple(id , purple4) # add
    if query.data == 'black4':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {black4} black chip')
        DB.add_yellow(id , -yellow4) # minus
        DB.add_black( id , black4) # add
    if query.data == 'white5':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {white5} black chip')
        DB.add_blue(id , -blue5) # minus
        DB.add_white(id , white5) # add
    if query.data == 'red5':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {red5} red chip')
        DB.add_blue(id , -blue5) # minus
        DB.add_red( id , red5) # add
    if query.data == 'orange5':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {orange5} orange chip')
        DB.add_blue( id , -blue5) # minus
        DB.add_orange( id , orange5) # add
    if query.data == 'yellow5':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {yellow5} yellow chip')
        DB.add_blue(id , -blue5) # minus
        DB.add_yellow( id , yellow5) # add
    if query.data == 'blue5':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {blue5} blue chip')
        DB.add_blue(id , -blue5) # minus
        DB.add_blue(id , blue5) # add
    if query.data == 'purple5':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {purple5} purple chip')
        DB.add_blue(id , -blue5) # minus
        DB.add_purple( id , purple5) # add
    if query.data == 'black5':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {black5} black chip')
        DB.add_blue( id , -blue5) # minus
        DB.add_black(id , black5) # add
    if query.data == 'white6':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {white6} white chip')
        DB.add_purple(id , -purple6) # minus
        DB.add_white(id , white6) # add
    if query.data == 'red6':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {red6} red chip')
        DB.add_purple(id , -purple6) # minus
        DB.add_red(id , red6) # add
    if query.data == 'orange6':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {orange6} orange chip')
        DB.add_purple(id , -purple6) # minus
        DB.add_orange(id , orange6) # add
    if query.data == 'yellow6':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {yellow6} yellow chip')
        DB.add_purple( id , -purple6) # minus
        DB.add_yellow(id , yellow6) # add
    if query.data == 'blue6':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {blue6} blue chip')
        DB.add_purple(id , -purple6) # minus
        DB.add_blue( id , blue6) # add
    if query.data == 'purple6':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {purple6} purple chip')
        DB.add_purple(id , -purple6) # minus
        DB.add_pruple(id , purple6) # add
    if query.data == 'black6':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {black6} black chip')
        DB.add_purple(id , -purple6) # minus
        DB.add_black( id , black6) # add
    if query.data == 'white7':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {white7} white chip')
        DB.add_black(id , -black7) # minus
        DB.add_white( id , white7) # add
    if query.data == 'red7':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {red7} red chip')
        DB.add_black( id, -black7)  # minus
        DB.add_red(id, red7)  # add
    if query.data == 'orange7':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {orange7} orange chip')
        DB.add_black(id, -black7)  # minus
        DB.add_orange(id, orange7)  # add
    if query.data == 'yellow7':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {yellow7} yellow chip')
        DB.add_black(id, -black7)  # minus
        DB.add_yellow( id, yellow7)  # add
    if query.data == 'blue7':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {blue7} blue chip')
        DB.add_black( id, -black7)  # minus
        DB.add_blue(id, blue7)  # add
    if query.data == 'purple7':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {purple7} purple chip')
        DB.add_black(id, -black7)  # minus
        DB.add_purple(id, purple7)  # add
    if query.data == 'black7':
        query.edit_message_text(f'Successfully exchanged {units} {type} chip to {black7} black chip')
        DB.add_black(id, -black7)  # minus
        DB.add_black( id, black7)  # add

def claim(update , context):
    id = update.effective_user.id
    name = update.effective_user.first_name
    username = update.effective_user.name
    VIP = DB.get_user_value(id, "vip")
    white = DB.get_user_value( id, "white")
    red = DB.get_user_value(id, "red")
    orange = DB.get_user_value( id, "orange")
    yellow = DB.get_user_value( id, "yellow")
    blue = DB.get_user_value(id, "blue")
    purple = DB.get_user_value( id, "purple")
    black = DB.get_user_value( id, "black")
    value = (white * 1) + (red * 5) + (orange * 25) + (yellow * 100) + (blue * 500) + (purple * 2500) + (black * 15000)
    average = DB.get_average_cash()
    claimed = DB.get_user_value(id, "claimed")
    if claimed:
        update.message.reply_text("You already claimed today's bonus , come back tommorow")
        return
    if value < average:
        claim_amount = average // 10
        DB.add_white(id, claim_amount)
        DB.set_user_value(id, "claimed", True)
        update.message.reply_text(f"You received {claim_amount} ⚪️ white chip")
    else:
     update.message.reply_text(f"You cannot claim free chips if your wallet balance is equal or more than average ({average}$)")

def claim_reset(context):
    DB.reset_daily_claims()
    print("claim_reset(): claim columns set to 0")

SWAP_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('swap', swap)],
        states={
            THREE: [CallbackQueryHandler(exchange2, pattern='^' + str("white") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("red") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("red4") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("orange") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("orange4") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("yellow") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("yellow4") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("white2") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("blue4") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("red2") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("purple4") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("orange2") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("black4") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("yellow2") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("white5") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("blue2") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("red5") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("white3") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("orange5") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("red3") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("yellow5") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("orange3") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("blue5") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("blue3") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("purple5") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("purple3") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("black5") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("white4") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("white6") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("white7") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("red6") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("red7") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("orange6") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("orange7") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("yellow6") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("yellow7") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("blue6") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("blue7") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("purple6") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("purple7") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("black6") + '$'),
CallbackQueryHandler(exchange2, pattern='^' + str("black7") + '$'),CallbackQueryHandler(exchange2, pattern='^' + str("yellow3") + '$')



            ],
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=True
    )

RAKEBACK_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('rakeback', rakeback)],
        states={
            FOUR: [CallbackQueryHandler(rakeback2, pattern='^' + str("claim") + '$'),
                   CallbackQueryHandler(rakeback3, pattern='^' + str("cancel") + '$'),
            ],
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=True
    )


START_HANDLER = CommandHandler('start', start)
WALLET_HANDLER = CommandHandler('wallet', wallet)
GAMES_HANDLER = CommandHandler('games', games)
ADD_HANDLER = CommandHandler('add', add)
VALUE_HANDLER = CommandHandler('value', value)
CLAIM_HANDLER = CommandHandler('claim', claim)
EXEC_HANDLER = CommandHandler('exec', exec)
STATS_HANDLER = CommandHandler('statistic', statistic)
GIFT_HANDLER = CommandHandler('gift',gift)  
SYSTEM_HANDLER = CommandHandler('system',system) 

dispatcher.add_handler(START_HANDLER)
dispatcher.add_handler(WALLET_HANDLER)
dispatcher.add_handler(GAMES_HANDLER)
dispatcher.add_handler(ADD_HANDLER)
dispatcher.add_handler(VALUE_HANDLER)
dispatcher.add_handler(CLAIM_HANDLER)
dispatcher.add_handler(SWAP_HANDLER)
dispatcher.add_handler(EXEC_HANDLER)
dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(RAKEBACK_HANDLER)
dispatcher.add_handler(GIFT_HANDLER)
dispatcher.add_handler(SYSTEM_HANDLER)





