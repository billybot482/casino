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

def janken(update: Update, context: CallbackContext):
    cd = context.chat_data
    
    cd['fighter'] = name = update.effective_user.first_name
    cd['fighterid'] = fid = update.effective_user.id
    
    cd['round'] = 1
    cd['fromhp'] = 3
    cd['tohp'] = 3
    
    
    white = round(DB.get_user_value(fid, "white"),4)
    red = round(DB.get_user_value(fid, "red"),4)
    orange = round(DB.get_user_value(fid, "orange"),4)
    yellow = round(DB.get_user_value(fid, "yellow"),4)
    blue = round(DB.get_user_value(fid, "blue"),4)
    purple = round(DB.get_user_value(fid, "purple"),4)
    black = round(DB.get_user_value(fid, "black"),4)
    type = update.message.text.split()[1]
    amount = update.message.text.split()[2]
    
    n =1 
    cc =  {1: 'white', 2: 'red', 3:'orange', 4:'yellow', 5:'blue', 6:'purple', 7:'black'}
    dd = {1:white, 2:red , 3:orange, 4:yellow , 5:blue , 6:purple , 7:black}
    
    amount = int(amount)
    cd['amount'] = amount
    cd['type '] = type
    keyboard = [
        [
            InlineKeyboardButton("Play", callback_data=str('play')),
            InlineKeyboardButton("Rules", callback_data=str('rules'))]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    for i in range(7):
     if type in colour:
      if type  == cc[n] and amount <=dd[n]:
       update.message.reply_text(f'<b>{name}</b> created a rock paper scissor game\n\n'
                              f'<b>Type of chip :</b> {type}\n\n'
                              f'<b>Amount :</b> {amount}', reply_markup = reply_markup , parse_mode = ParseMode.HTML)
      n+=1   
        
    print('entry done')
    return ONE
    
def rules(update: Update, context: CallbackContext):
    cd = context.chat_data
    f = cd['fighter']
    t = cd['to']
    fid = cd['fighterid']
    tid = cd['toid']
   
    query = update.callback_query
    query.answer('1.Rocks beats scissor , scissor beats paper , paper beats rock', show_alert = True)
    return None

def play(update: Update, context: CallbackContext):
    cd = context.chat_data
    query = update.callback_query
    cd['to_id'] = toid =update.callback_query.from_user.id
    cd['to_name'] = toname = update.callback_query.from_user.first_name
    
    
    f = cd['fighter']
    id = cd['fighterid']
    toid =cd['to_id']
    t =cd['to_name']
    type = cd['type']
    amount = cd['amount']
    
    
    white = round(DB.get_user_value(toid, "white"),4)
    red = round(DB.get_user_value(toid, "red"),4)
    orange = round(DB.get_user_value(toid, "orange"),4)
    yellow = round(DB.get_user_value(toid, "yellow"),4)
    blue = round(DB.get_user_value(toid, "blue"),4)
    purple = round(DB.get_user_value(toid, "purple"),4)
    black = round(DB.get_user_value(toid, "black"),4)
    n =1 
    cc =  {1: 'white', 2: 'red', 3:'orange', 4:'yellow', 5:'blue', 6:'purple', 7:'black'}
    dd = {1:white, 2:red , 3:orange, 4:yellow , 5:blue , 6:purple , 7:black}

    keyboard = [
        [
            InlineKeyboardButton("✊", callback_data=str('rock')),
            InlineKeyboardButton("✋", callback_data=str('paper')),
            InlineKeyboardButton("✌️", callback_data=str('scissor'))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    for i in range(7):
     if type == cc[n] and amount<dd[n]:
        query.answer('Balance not enough to play this game')
        n +=1
        return None
     else:
      query.edit_message_text(
        text=f"_*Round : {cd['round']}*_\n\n"
             f"{f}❤ : {cd['fromhp']}\n{t}❤ : {cd['tohp']}\n\n"
             f"*{f}* make your decision\n", reply_markup=reply_markup,parse_mode = ParseMode.MARKDOWN_V2
    )
    return ONE

def first(update: Update, context: CallbackContext):
    cd = context.chat_data
    query = update.callback_query
    f = cd['fighter']
    t = cd['to_name']
    fid = cd['fighterid']
    tid = cd['to_id']


    keyboard = [
        [
            InlineKeyboardButton("✊", callback_data=str('rock')),
            InlineKeyboardButton("✋", callback_data=str('paper')),
            InlineKeyboardButton("✌️", callback_data=str('scissor'))
        ]
    ]
    
    reply_markup2 = InlineKeyboardMarkup(keyboard)
    if update.callback_query.from_user.id != fid:
        query.answer('player 2 not ur turn')
        return None
    query.edit_message_text(
        text=f"_*Round : {cd['round']}*_\n\n"
             f"{f}❤ : {cd['fromhp']}\n{t}❤ : {cd['tohp']}\n\n"
             f"*{t}* choose one elemental\n"
             f"*{t}* 选一个攻击属性", reply_markup=reply_markup2, parse_mode = ParseMode.MARKDOWN_V2
    )
    cd['round']+=1
    cd['choice1'] = query.data
    if tid == 163494588:
     context.bot.send_message(chat_id=163494588, text = f'{f} choose : {query.data}')
    if tid == 652962567:
     context.bot.send_message(chat_id=652962567, text=f'{f} choose : {query.data}')
    print('player 1 choose : '+str(cd['choice1'])+ ',id : ' + str(update.callback_query.from_user.id))
    return TWO

def res(update: Update, context: CallbackContext):
    cd = context.chat_data
    query = update.callback_query
    query.answer()
    cd['choice2'] = query.data
    f = cd['fighter']
    t = cd['to']
    fid = cd['fighterid']
    tid = cd['toid']
    fchose = cd['choice1']
    tchose = cd['choice2']
    
    type = cd['type']
    amount =cd['amount']
    
    n =1 
    cc =  {1: 'white', 2: 'red', 3:'orange', 4:'yellow', 5:'blue', 6:'purple', 7:'black'}
    dd = {1:white, 2:red , 3:orange, 4:yellow , 5:blue , 6:purple , 7:black}
    fwin = {1: DB.add_white(fid,amount*2), 2: DB.add_red(fid,amount*2), 3: DB.add_orange(fid,amount*2), 4: DB.add_yellow(fid,amount*2), 5: DB.add_blue(fid,amount*2), 6:DB.add_purple(fid,amount*2), 7:DB.add_black(fid,amount*2)} 
    twin = {1: DB.add_white(tid,amount*2), 2: DB.add_red(tid,amount*2), 3: DB.add_orange(tid,amount*2), 4: DB.add_yellow(tid,amount*2), 5: DB.add_blue(tid,amount*2), 6:DB.add_purple(tid,amount*2), 7:DB.add_black(tid,amount*2)} 
    floss = {1: DB.add_white(fid,-amount), 2: DB.add_red(fid,-amount), 3: DB.add_orange(fid,-amount), 4: DB.add_yellow(fid,-amount), 5: DB.add_blue(fid,-amount), 6:DB.add_purple(fid,-amount), 7:DB.add_black(fid,-amount)} 
    tloss = {1: DB.add_white(tid,-amount), 2: DB.add_red(tid,-amount), 3: DB.add_orange(tid,-amount), 4: DB.add_yellow(tid,-amount), 5: DB.add_blue(tid,-amount), 6:DB.add_purple(tid,-amount), 7:DB.add_black(tid,-amount)} 
    
    keyboard = [
        [
            InlineKeyboardButton("✊", callback_data=str('rock')),
            InlineKeyboardButton("✋", callback_data=str('paper')),
            InlineKeyboardButton("✌️", callback_data=str('scissor'))
        ]
    ]
    reply_markup3 = InlineKeyboardMarkup(keyboard)
    if update.callback_query.from_user.id != tid:
        query.answer('player 2 not ur turn')
        return None
    choice = {
            "rock": "✊",
            "paper": "✋",
             "scissor": "✌️"
                        }

    a = choice[cd['choice1']]
    b = choice[cd['choice2']]
    if update.callback_query.from_user.id != tid:
        query.answer('player 1 not ur turn')
        return None
      
      
    if cd['choice1'] == cd['choice2']:
        cd['fromhp'] -= 1
        cd['tohp'] -= 1
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'_its a Draw_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}*Make you decision\n"
                                f'{t}', parse_mode=ParseMode.MARKDOWN_V2, reply_markup= reply_markup3)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
          if cd['fromhp'] > cd['tohp']:
                for i in range(7):
                 if type == cc[n]:
                  fwin[n]
                  tloss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f} won {amount} {type} chip\n')
                 n+=1
                
          elif cd['tohp'] > cd['fromhp']:
               for i in range(7):
                 if type == cc[n]:
                  twin[n]
                  floss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t} won {amount} {type} chip\n')  
                 n+=1
          else:
                
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f" Draw , cost has been returned to respective wallet!!\n")
          return ConversationHandler.END
          
        return ONE
     
    elif cd['choice1'] == 'rock' and cd['choice2'] == 'scissor':
        cd['fromhp'] -= 0
        cd['tohp'] -= 1
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'_[{f}](tg://user?id={fid}) wins_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}*Make you decision\n"
                                , parse_mode=ParseMode.MARKDOWN_V2,reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
          if cd['fromhp'] > cd['tohp']:
                for i in range(7):
                 if type == cc[n]:
                  fwin[n]
                  tloss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f} won {amount} {type} chip\n')
                 n+=1
                
          elif cd['tohp'] > cd['fromhp']:
               for i in range(7):
                 if type == cc[n]:
                  twin[n]
                  floss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t} won {amount} {type} chip\n')  
                 n+=1
          else:
                
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f" Draw , cost has been returned to respective wallet!!\n")
          return ConversationHandler.END

        return ONE

    elif cd['choice1'] == 'scissor' and cd['choice2'] == 'rock':
        cd['fromhp'] -= 1
        cd['tohp'] -= 0
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'_[{t}](tg://user?id={tid}) wins_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}*Make you decision\n"
                                , parse_mode=ParseMode.MARKDOWN_V2,reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
          if cd['fromhp'] > cd['tohp']:
                for i in range(7):
                 if type == cc[n]:
                  fwin[n]
                  tloss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f} won {amount} {type} chip\n')
                 n+=1
                
          elif cd['tohp'] > cd['fromhp']:
               for i in range(7):
                 if type == cc[n]:
                  twin[n]
                  floss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t} won {amount} {type} chip\n')  
                 n+=1
          else:
                
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f" Draw , cost has been returned to respective wallet!!\n")
          return ConversationHandler.END

        return ONE

    elif cd['choice1'] == 'rock' and cd['choice2'] == 'paper':
        cd['fromhp'] -= 1
        cd['tohp'] -= 0
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'_[{t}](tg://user?id={tid}) wins_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}*Make you decision\n"
                                , parse_mode=ParseMode.MARKDOWN_V2,reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
          if cd['fromhp'] > cd['tohp']:
                for i in range(7):
                 if type == cc[n]:
                  fwin[n]
                  tloss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f} won {amount} {type} chip\n')
                 n+=1
                
          elif cd['tohp'] > cd['fromhp']:
               for i in range(7):
                 if type == cc[n]:
                  twin[n]
                  floss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t} won {amount} {type} chip\n')  
                 n+=1
          else:
                
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f" Draw , cost has been returned to respective wallet!!\n")
          return ConversationHandler.END

        return ONE

    elif cd['choice1'] == 'paper' and cd['choice2'] == 'rock':
        cd['fromhp'] -= 0
        cd['tohp'] -= 1
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'_[{f}](tg://user?id={fid}) wins_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}*Make you decision\n"
                                , parse_mode=ParseMode.MARKDOWN_V2,reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
          if cd['fromhp'] > cd['tohp']:
                for i in range(7):
                 if type == cc[n]:
                  fwin[n]
                  tloss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f} won {amount} {type} chip\n')
                 n+=1
                
          elif cd['tohp'] > cd['fromhp']:
               for i in range(7):
                 if type == cc[n]:
                  twin[n]
                  floss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t} won {amount} {type} chip\n')  
                 n+=1
          else:
                
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f" Draw , cost has been returned to respective wallet!!\n")
          return ConversationHandler.END
        return ONE

    elif cd['choice1'] == 'paper' and cd['choice2'] == 'scissor':
        cd['fromhp'] -= 1
        cd['tohp'] -= 0
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'_[{t}](tg://user?id={tid}) wins_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}*Make you decision\n"
                                , parse_mode=ParseMode.MARKDOWN_V2,reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
          if cd['fromhp'] > cd['tohp']:
                for i in range(7):
                 if type == cc[n]:
                  fwin[n]
                  tloss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f} won {amount} {type} chip\n')
                 n+=1
                
          elif cd['tohp'] > cd['fromhp']:
               for i in range(7):
                 if type == cc[n]:
                  twin[n]
                  floss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t} won {amount} {type} chip\n')  
                 n+=1
          else:
                
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f" Draw , cost has been returned to respective wallet!!\n")
          return ConversationHandler.END

        return ONE

    elif cd['choice1'] == 'scissor' and cd['choice2'] == 'paper':
        cd['fromhp'] -= 0
        cd['tohp'] -= 1
        query.message.edit_text(f'*{f}* chose {fchose}{a} and *{t}* chose {tchose}{b}\n'
                                f'_[{f}](tg://user?id={fid}) wins_\n\n'
                                f"_*Round : {cd['round']}*_\n"
             f"❤{f} : {cd['fromhp']}\n❤{t} : {cd['tohp']}\n\n"
             f"*{f}*Make you decision\n"
                                , parse_mode=ParseMode.MARKDOWN_V2,reply_markup= reply_markup)

        if cd['fromhp'] == 0 or cd['tohp'] == 0:
          if cd['fromhp'] > cd['tohp']:
                for i in range(7):
                 if type == cc[n]:
                  fwin[n]
                  tloss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{f} win !!\n"
                                        f'{f} won {amount} {type} chip\n')
                 n+=1
                
          elif cd['tohp'] > cd['fromhp']:
               for i in range(7):
                 if type == cc[n]:
                  twin[n]
                  floss[n]
                  query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f"{t} win !!\n"
                                        f'{t} won {amount} {type} chip\n')  
                 n+=1
          else:
                
                query.message.edit_text(f"{f} ❤️Hp : {cd['fromhp']}\n{t} ❤️Hp: {cd['tohp']}\n\n"
                                        f" Draw , cost has been returned to respective wallet!!\n")
          return ConversationHandler.END

        return ONE
      
janken_handler = ConversationHandler(
        entry_points=[CommandHandler('janken', janken)],
        states={
            ONE: [
                CallbackQueryHandler(play, pattern='^' + str('play') + '$'),
                CallbackQueryHandler(rules, pattern='^' + str('rules') + '$'),
                CallbackQueryHandler(first, pattern='^' + str('rock') + '$'),
                CallbackQueryHandler(first, pattern='^' + str('scissor') + '$'),
                CallbackQueryHandler(first, pattern='^' + str('paper') + '$')
            ],
            TWO: [
                CallbackQueryHandler(res, pattern='^' + str('rock') + '$'),
                CallbackQueryHandler(res, pattern='^' + str('scissor') + '$'),
                CallbackQueryHandler(res, pattern='^' + str('paper') + '$')

            ],
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=False,
    run_async=True
    )

dispatcher.add_handler(janken_handler)

