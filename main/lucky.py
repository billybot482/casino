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

cc =  {1: 'white', 2: 'red', 3:'orange', 4:'yellow', 5:'blue', 6:'purple', 7:'black'}


def luckydraw(update , context):
    print('debug')
    cd= context.chat_data
    query = update.callback_query
    cd['id'] = id = update.effective_user.id
    cd['vip']= vip = DB.get_user_value(id , 'vip')
    cd['m1'] = mult1 = (((vip+1)/10)+(vip*0.2))/100
    
    cd['name'] = name = update.effective_user.first_name
    cd['white'] = white = round(DB.get_user_value(id, "white"),4)
    cd['red'] =  red = round(DB.get_user_value(id, "red"),4)
    cd['orange'] =orange = round(DB.get_user_value(id, "orange"),4)
    cd['yellow'] = yellow = round(DB.get_user_value(id, "yellow"),4)
    cd['blue'] = blue = round(DB.get_user_value(id, "blue"),4)
    cd['purple'] = purple = round(DB.get_user_value(id, "purple"),4)
    cd['black'] = black = round(DB.get_user_value(id, "black"),4) 
    dd = {1:white, 2:red , 3:orange, 4:yellow , 5:blue , 6:purple , 7:black}
    keyboard = [
         [InlineKeyboardButton('Join', callback_data='join1'),InlineKeyboardButton('rules', callback_data='rules')],
         [InlineKeyboardButton('cancel', callback_data='cancel')]
     ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    n =1 
  
    try:
     cd['type'] = type = update.message.text.split()[1]
     amount = update.message.text.split()[2]
     cd['amount'] = amount = int(amount)
     
    except TypeError:
        return -1
    except IndexError:
        return -1
    except ValueError:
        return -1
    except AttributeError:
        return -1
      
    for i in range(7):
      if type in colour:
       if type  == cc[n] and amount <=dd[n]:
        update.message.reply_text(f'*{name}* created a Luck draw game\n\n'
                              f'*Entry chips :* {type}\n'
                              f'*Amount :* {amount}\n\n'
                              f'*Current Lucky draw list:\n1-{name}*', reply_markup = reply_markup , parse_mode = ParseMode.MARKDOWN_V2)
       n+=1   
    return ONE
      
def rules(update , context):
    cd = context.chat_data
    query = update.callback_query
    query.answer('5 people game , 2 winner , first draw gets 60% of the pot and 2nd draw gets 40% of the pot', show_alert = True)
    return None
  
  
def cancel(update , context):
    cd = context.chat_data
    query = update.callback_query
    id = cd['id']
    if update.callback_query.from_user.id != id:
        query.answer('Only creator can use this')
        return None
    query.edit_message_text('<b>Game terminated!!\n\nAll chips were refunded</b>',parse_mode = ParseMode.HTML)
    return ConversationHandler.END
  
def join1(update , context):
    cd= context.chat_data
    query = update.callback_query
    amount = cd['amount']
    type = cd['type']
    cd['name'] = name 
    cd['u1name'] = user1_name =  update.callback_query.from_user.first_name
    cd['u1id'] = user1_id =  update.callback_query.from_user.id
    cd['vip']= vip = DB.get_user_value(user1_id , 'vip')
    cd['m2'] = (((vip+1)/10)+(vip*0.2))/100
    cd['white'] = white = round(DB.get_user_value(user1_id, "white"),4)
    cd['red'] =  red = round(DB.get_user_value(user1_id, "red"),4)
    cd['orange'] =orange = round(DB.get_user_value(user1_id, "orange"),4)
    cd['yellow'] = yellow = round(DB.get_user_value(user1_id, "yellow"),4)
    cd['blue'] = blue = round(DB.get_user_value(user1_id, "blue"),4)
    cd['purple'] = purple = round(DB.get_user_value(user1_id, "purple"),4)
    cd['black'] = black = round(DB.get_user_value(user1_id, "black"),4) 
    dd = {1:white, 2:red , 3:orange, 4:yellow , 5:blue , 6:purple , 7:black}
    keyboard = [
         [InlineKeyboardButton('Join', callback_data='join2'),InlineKeyboardButton('rules', callback_data='rules')],
         [InlineKeyboardButton('cancel', callback_data='cancel')]
     ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    for i in range(7):
      if type in colour:
       if type  == cc[n] and amount <=dd[n]:
        query.edit_message_text(f'*{name}* created a Luck draw game\n\n'
                              f'*Entry chips :* {type}\n'
                              f'*Amount :* {amount}\n\n'
                              f'*Current Lucky draw list:\n1.{name}\n2.{user1_name}*', reply_markup = reply_markup , parse_mode = ParseMode.MARKDOWN_V2)
       n+=1   
    return ONE
    
def join2(update , context):
    cd= context.chat_data
    query = update.callback_query
    amount = cd['amount']
    type = cd['type']
    cd['u2name'] = user2_name =  update.callback_query.from_user.first_name
    cd['u2id'] = user2_id =  update.callback_query.from_user.id
    name = cd['name']
    user1_name  = cd['u1name']
    user1_id = cd['u1id'] 
    cd['vip']= vip = DB.get_user_value(user2_id , 'vip')
    cd['m3'] =  (((vip+1)/10)+(vip*0.2))/100
    cd['white'] = white = round(DB.get_user_value(user2_id, "white"),4)
    cd['red'] =  red = round(DB.get_user_value(user2_id, "red"),4)
    cd['orange'] =orange = round(DB.get_user_value(user2_id, "orange"),4)
    cd['yellow'] = yellow = round(DB.get_user_value(user2_id, "yellow"),4)
    cd['blue'] = blue = round(DB.get_user_value(user2_id, "blue"),4)
    cd['purple'] = purple = round(DB.get_user_value(user2_id, "purple"),4)
    cd['black'] = black = round(DB.get_user_value(user2_id, "black"),4) 
    dd = {1:white, 2:red , 3:orange, 4:yellow , 5:blue , 6:purple , 7:black}
    keyboard = [
         [InlineKeyboardButton('Join', callback_data='join3'),InlineKeyboardButton('rules', callback_data='rules')],
         [InlineKeyboardButton('cancel', callback_data='cancel')]
     ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    for i in range(7):
      if type in colour:
       if type  == cc[n] and amount <=dd[n]:
        query.edit_message_text(f'*{name}* created a Luck draw game\n\n'
                              f'*Entry chips :* {type}\n'
                              f'*Amount :* {amount}\n\n'
                              f'*Current Lucky draw list:\n1.{name}\n2.{user1_name}\n3.{user2_name}*', reply_markup = reply_markup , parse_mode = ParseMode.MARKDOWN_V2)
       n+=1   
    return ONE  


def join3(update , context):
    cd= context.chat_data
    query = update.callback_query
    amount = cd['amount']
    type = cd['type']
    cd['u3name'] = user3_name =  update.callback_query.from_user.first_name
    cd['u3id'] = user3_id =  update.callback_query.from_user.id
    name = cd['name']
    user1_name  = cd['u1name']
    user1_id = cd['u1id'] 
    user2_name  = cd['u2name']
    user2_id = cd['u2id'] 
    cd['vip']= vip = DB.get_user_value(user3_id , 'vip')
    cd['m4'] = (((vip+1)/10)+(vip*0.2))/100
    cd['white'] = white = round(DB.get_user_value(user3_id, "white"),4)
    cd['red'] =  red = round(DB.get_user_value(user3_id, "red"),4)
    cd['orange'] =orange = round(DB.get_user_value(user3_id, "orange"),4)
    cd['yellow'] = yellow = round(DB.get_user_value(user3_id, "yellow"),4)
    cd['blue'] = blue = round(DB.get_user_value(user3_id, "blue"),4)
    cd['purple'] = purple = round(DB.get_user_value(user3_id, "purple"),4)
    cd['black'] = black = round(DB.get_user_value(user3_id, "black"),4) 
    dd = {1:white, 2:red , 3:orange, 4:yellow , 5:blue , 6:purple , 7:black}
    keyboard = [
         [InlineKeyboardButton('Join', callback_data='join4'),InlineKeyboardButton('rules', callback_data='rules')],
         [InlineKeyboardButton('cancel', callback_data='cancel')]
     ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    for i in range(7):
      if type in colour:
       if type  == cc[n] and amount <=dd[n]:
        query.edit_message_text(f'*{name}* created a Luck draw game\n\n'
                              f'*Entry chips :* {type}\n'
                              f'*Amount :* {amount}\n\n'
                              f'*Current Lucky draw list:\n1.{name}\n2.{user1_name}\n3.{user2_name}\n4.{user3_name}*', reply_markup = reply_markup , parse_mode = ParseMode.MARKDOWN_V2)
       n+=1   
    return ONE
  
def join4(update , context):
    cd= context.chat_data
    query = update.callback_query
    amount = cd['amount']
    type = cd['type']
    cd['u4name'] = user4_name =  update.callback_query.from_user.first_name
    cd['u4id'] = user4_id =  update.callback_query.from_user.id
    name = cd['name']
    user1_name  = cd['u1name']
    user1_id = cd['u1id'] 
    user2_name  = cd['u2name']
    user2_id = cd['u2id'] 
    user3_name  = cd['u3name']
    user3_id = cd['u3id'] 
    cd['vip']= vip = DB.get_user_value(id , 'vip')
    cd['m5'] = (((vip+1)/10)+(vip*0.2))/100
    cd['white'] = white = round(DB.get_user_value(user4_id, "white"),4)
    cd['red'] =  red = round(DB.get_user_value(user4_id, "red"),4)
    cd['orange'] =orange = round(DB.get_user_value(user4_id, "orange"),4)
    cd['yellow'] = yellow = round(DB.get_user_value(user4_id, "yellow"),4)
    cd['blue'] = blue = round(DB.get_user_value(user4_id, "blue"),4)
    cd['purple'] = purple = round(DB.get_user_value(user4_id, "purple"),4)
    cd['black'] = black = round(DB.get_user_value(user4_id, "black"),4) 
    dd = {1:white, 2:red , 3:orange, 4:yellow , 5:blue , 6:purple , 7:black}
    keyboard = [
         [InlineKeyboardButton('Join', callback_data='draw1'),InlineKeyboardButton('rules', callback_data='rules')],
         [InlineKeyboardButton('cancel', callback_data='cancel')]
     ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    for i in range(7):
      if type in colour:
       if type  == cc[n] and amount <=dd[n]:
        query.edit_message_text(f'*{name}* created a Luck draw game\n\n'
                              f'*Entry chips :* {type}\n'
                              f'*Amount :* {amount}\n\n'
                              f'*Current Lucky draw list:\n1.{name}\n2.{user1_name}\n3.{user2_name}\n4.{user3_name}\n5.{user4_name}*', reply_markup = reply_markup , parse_mode = ParseMode.MARKDOWN_V2)
       n+=1   
    return ONE

def draw1(update , context):
    cd= context.chat_data
    query = update.callback_query                              
    name = cd['name']
    id = cd['id']      
    amount = cd['amount']
    type = cd['type']                            
    user1_name  = cd['u1name']
    user1_id = cd['u1id'] 
    user2_name  = cd['u2name']
    user2_id = cd['u2id'] 
    user3_name  = cd['u3name']
    user3_id = cd['u3id'] 
    user4_name  = cd['u4name']
    user4_id = cd['u4id'] 
   
    keyboard = [
         [InlineKeyboardButton('Draw Winner', callback_data='win1')]
     ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f'*Lucky Draw Begin!\n\nCurrent Lucky draw list:\n1.{name}\n2.{user1_name}\n3.{user2_name}\n4.{user3_name}\n5.{user4_name}*\n\nCreator {name} press draw to begin', reply_markup = reply_markup , parse_mode = ParseMode.MARKDOWN_V2)
     
    return ONE
  
def draw2(update , context):
    cd= context.chat_data
    query = update.callback_query                              
    name = cd['name']
    id = cd['id']      
    amount = cd['amount']
    type = cd['type']                            
    user1_name  = cd['u1name']
    user1_id = cd['u1id'] 
    user2_name  = cd['u2name']
    user2_id = cd['u2id'] 
    user3_name  = cd['u3name']
    user3_id = cd['u3id'] 
    user4_name  = cd['u4name']
    user4_id = cd['u4id'] 
    m1 = cd['m1']
    m2 = cd['m2']
    m3 = cd['m3']
    m4 = cd['m4']
    m5 = cd['m5']
    
    if update.callback_query.from_user.id != id:
        query.answer('Only creator can use this')
        return None
      
    pot = [{'name': user1_name, 'id': user1_id, 'm':m2},{'name': user2_name, 'id': user2_id, 'm':m3},{'name': user3_name, 'id': user3_id, 'm':m4},{'name': user4_name, 'id': user4_id, 'm':m5},{'name': name, 'id': id, 'm':m}]
    winner1 = random.choice(pot)
    
    keyboard = [
         [InlineKeyboardButton('Draw Winner', callback_data='win1')]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"*Lucky Draw Begin!\n\nCurrent Lucky draw list:\n1.{name}\n2.{user1_name}\n3.{user2_name}\n4.{user3_name}\n5.{user4_name}*\n\nThe Winner of first draw is {winner1['name']}\nCongrats on winning {(amount*5)*0.6} {type}chip", reply_markup = reply_markup , parse_mode = ParseMode.MARKDOWN_V2)
    DB.add_chip(winner1['id'], type, (amount*5)*0.6)
    DB.add_win(winner1['id'], 1)
    DB.add_rbchip(winner1['id'], type, amount*winner1['m'])
    DB.add_wager(winner1['id'], amount*values['type'])
    return ONE 
                                  
def draw3(update , context):
    cd= context.chat_data
    query = update.callback_query                              
    name = cd['name']
    id = cd['id']      
    amount = cd['amount']
    type = cd['type']                            
    user1_name  = cd['u1name']
    user1_id = cd['u1id'] 
    user2_name  = cd['u2name']
    user2_id = cd['u2id'] 
    user3_name  = cd['u3name']
    user3_id = cd['u3id'] 
    user4_name  = cd['u4name']
    user4_id = cd['u4id'] 
    
    if update.callback_query.from_user.id != id:
        query.answer('Only creator can use this')
        return None
      
    pot = [{'name': user1_name, 'id': user1_id, 'm':m2},{'name': user2_name, 'id': user2_id, 'm':m3},{'name': user3_name, 'id': user3_id, 'm':m4},{'name': user4_name, 'id': user4_id, 'm':m5},{'name': name, 'id': id, 'm':m}]
    winner2 = random.choice(pot)  
      
    keyboard = [
         [InlineKeyboardButton('Draw Winner', callback_data='win1')]
     ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"*Lucky Draw Begin!\n\nCurrent Lucky draw list:\n1.{name}\n2.{user1_name}\n3.{user2_name}\n4.{user3_name}\n5.{user4_name}*\n\nThe Winner of second draw is {winner2['name']}\nCongrats on winning {(amount*5)*0.4} {type}chip", reply_markup = reply_markup , parse_mode = ParseMode.MARKDOWN_V2)
    DB.add_chip(winner2['id'], type, (amount*5)*0.4)
    DB.add_win(winner2['id'], 1)
    DB.add_rbchip(winner2['id'], type, amount*winner2['m'])
    DB.add_wager(winner2['id'], amount*values['type']) 
    return ConversationHandler.END


      
lucky_handler = ConversationHandler(
        entry_points=[CommandHandler('luckydraw', luckydraw)],
        states={
            ONE: [
                CallbackQueryHandler(cancel, pattern='^' + str('cancel') + '$'),
                CallbackQueryHandler(rules, pattern='^' + str('rules') + '$'),
                CallbackQueryHandler(join1, pattern='^' + str('join1') + '$'),
                CallbackQueryHandler(join2, pattern='^' + str('join2') + '$'),
                CallbackQueryHandler(join3, pattern='^' + str('join3') + '$'),
                CallbackQueryHandler(join4, pattern='^' + str('join4') + '$'),
                CallbackQueryHandler(draw1, pattern='^' + str('draw1') + '$'),
                CallbackQueryHandler(draw2, pattern='^' + str('win1') + '$'),
                CallbackQueryHandler(draw3, pattern='^' + str('win2') + '$')
            ],
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=False,
    run_async=True
    )

dispatcher.add_handler(lucky_handler)





































