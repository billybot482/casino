import logging
import random
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
PETONE , PETTWO , PETTHREE , PETFOUR , FIRST , SECOND,  *_ = range(50)

ingame = []

def challenge(update , context):
  cd = context.bot_data
  query = update.callback_query
  if not update.message.reply_to_message:
             update.message.reply_text('reply someone')
             return -1
  cd['p1id'] = id = update.effective_user.id
  cd['p1'] = name = update.effective_user.first_name
  cd['p2'] = to = update.message.reply_to_message.from_user.first_name
  cd['p2id'] = toid = update.message.reply_to_message.from_user.id
  
  if id in ingame:
    update.message.reply_text('finish your game first')
    return -1
  if toid in ingame:
    update.message.reply_text('this person is already in a match , wait for it to end')
    return -1
  
  pet_id = DB.get_user_value(id , 'mainpet_id')
  if pet_id ==0:
      update.message.reply_text('You dont have mainpet yet')
      return -1
  pet_id2 = DB.get_user_value(toid , 'mainpet_id')
  if pet_id2 ==0:
      update.message.reply_text('The person dont have mainpet yet')
      return -1
    
  keyboard = [
        [
            InlineKeyboardButton("accept", callback_data=str('accept')),
            InlineKeyboardButton("reject", callback_data=str('reject')),
        ],
        [InlineKeyboardButton("rules", callback_data=str('rules')),InlineKeyboardButton("cancel", callback_data=str('cancel'))],
 
    ]
  reply_markup = InlineKeyboardMarkup(keyboard)
    
  if toid == context.bot.id:
     update.message.reply_text('cant challenge bot')
     return -1
  if toid == id:
     update.message.reply_text('cant challenge yourself')
     return -1
  if toid != id:
     update.message.reply_text(f'{name} challenged {to} to a pet 🌟talent show🌟\n\nClick accept to begin', parse_mode = ParseMode.HTML, reply_markup = reply_markup)
     print('end 1')    
  return PETONE
  
def reject(update , context):
  cd = context.bot_data
  query = update.callback_query
  query.answer()
  print('reject enter')
  p2id = cd['p2id']
  p2 = cd['p2']
  if update.callback_query.from_user.id != p2id:
        query.answer('Cannot use')
        return None
  query.edit_message_text(f'{p2} Rejected the challenge')
  return ConversationHandler.END
    
    
def cancel(update , context):
  cd = context.bot_data
  query = update.callback_query
  query.answer()
  p1id = cd['p1id']
  p1 = cd['p1']
  if update.callback_query.from_user.id != p1id:
        query.answer('Cannot use')
        return None
  query.edit_message_text(f'{p1} cancelled the challenge')
  return ConversationHandler.END
  

def rules(update , context):
  cd = context.bot_data
  query = update.callback_query
  query.answer('pet that reach 0 confident loses', show_alert = True)
  return 0
  
def accept(update, context):
  cd = context.bot_data
  query = update.callback_query
  query.answer()
  print('accept enter')
  p1 = cd['p1']
  p1id = cd['p1id']
  p2 = cd['p2']
  p2id = cd['p2id']
  ingame.append(p1id)
  ingame.append(p2id)
  cd['round'] =  rd = 1
  
  empty = '▒'
  full = '█'
  
  pet_id1 = DB.get_user_value(p1id , 'mainpet_id')
  pet_id2 = DB.get_user_value(p2id , 'mainpet_id')
  
  pet1 = str(pet_id1).zfill(3)
  pet2 = str(pet_id2).zfill(3)
  
  talent1 = DB.get_user_pet_value(p1id , pet_id1 , 'talent')
  distract1 = DB.get_user_pet_value(p1id ,pet_id1 , 'distract')
  confident1 = DB.get_user_pet_value(p1id , pet_id1 , 'confident')
  special1 = DB.get_user_pet_value(p1id ,pet_id1 , 'special')
  cd['type1'] = type1 = DB.get_user_pet_value(p1id ,pet_id1 , 'type')
  age1 = DB.get_user_pet_value(p1id ,pet_id1 , 'growth')
  
  #Game stats
  attack1 = talent1 + round(((age1+1)*talent1/4),0)
  defense1 = distract1 + round(((age1+1)*distract1/4),0)
  cd['max1'] = hp1 = confident1 + int(round(((age1+1)*confident1/4),0))
  cd['hp1'] = current1 = hp1
  
  talent2 = DB.get_user_pet_value(p2id ,pet_id2, 'talent')
  distract2 = DB.get_user_pet_value(p2id ,pet_id2 , 'distract')
  confident2 = DB.get_user_pet_value(p2id ,pet_id2 , 'confident')
  special2 = DB.get_user_pet_value(p2id ,pet_id2 , 'special')
  cd['type2'] = type2 = DB.get_user_pet_value(p2id ,pet_id2 , 'type')
  age2 = DB.get_user_pet_value(p2id ,pet_id2 , 'growth')
  
  #Game stats
  attack2 = talent2 + round(((age2+1)*talent2/4),0)
  defense2 = distract2 + round(((age2+1)*distract2/4),0)
  cd['max2'] = hp2 = confident2 + int(round(((age2+1)*confident2/4),0))
  cd['hp2'] = current2 = hp2
  
  remain1 = current1*100/hp1
  remain2 = current2*100/hp2
  
  p1r1 = int((remain1+10)/10)
  p1r2 = int(11-p1r1)
  
  p2r1 = int((remain1+10)/10)
  p2r2 = int(11-p2r1)
  
  bar1 = p1r1*full+p1r2*empty
  bar2 = p2r1*full+p2r2*empty
  
  cd['mana1'] = mana1 = 50
  cd['mana2'] = mana2 = 50
  
  
  keyboard = [
           [InlineKeyboardButton("Shake\n💟0", callback_data='shake'),
            InlineKeyboardButton("Distract\n💟60", callback_data='distract'),],
            [InlineKeyboardButton("Jump\n💟45", callback_data='jump'),
           InlineKeyboardButton("Dance\n💟110", callback_data='dance'),],
         [InlineKeyboardButton(f"Special : {special1}\n💟", callback_data=f'{special1}')],
    [InlineKeyboardButton("Resign", callback_data='wood'),InlineKeyboardButton("Draw", callback_data='wood')]
  ]
  
  reply_markup = InlineKeyboardMarkup(keyboard)
  query.edit_message_text(
    text = f'<i><b>Round {rd}</b></i>\n\n'
    f'{p1}|{type1} #{pet1}\n💟Mana : {mana1}\n{bar1} {current1}/{hp1}\n\n{p2}|{type2} #{pet2}\n💟Mana : {mana1}\n{bar2} {current2}/{hp2}\n\n'
    f'<b>{p1} pick a move</b>', parse_mode = ParseMode.HTML, reply_markup = reply_markup)
  return PETONE

def first(update , context):
   cd = context.bot_data
   query = update.callback_query
   query.answer()
   p1 = cd['p1']
   p1id = cd['p1id']
   p2 = cd['p2']
   p2id = cd['p2id']
   rd = cd['round']
  
   current1 = cd['hp1']
   current2 = cd['hp2']
   hp1 = cd['max1']
   hp2 = cd['max2']
  
   empty = '▒'
   full = '█'
   pet_id1 = DB.get_user_value(p1id , 'mainpet_id')
   pet_id2 = DB.get_user_value(p2id , 'mainpet_id')
  
   special1 = DB.get_user_pet_value(p1id ,pet_id1 , 'special')
   special2 = DB.get_user_pet_value(p2id ,pet_id2 , 'special')
  
   remain1 = current1*100/hp1
   remain2 = current2*100/hp2
  
   p1r1 = int((remain1+10)/10)
   p1r2 = int(11-p1r1)
  
   p2r1 = int((remain1+10)/10)
   p2r2 = int(11-p2r1)
  
   bar1 = p1r1*full+p1r2*empty
   bar2 = p2r1*full+p2r2*empty 
  
   type1 = cd['type1']
   type2 = cd['type2']
  
   mana1 = cd['mana1']
   mana2 = cd['mana2']
  
   keyboard = [
           [InlineKeyboardButton("Shake\n💟0", callback_data='shake'),
            InlineKeyboardButton("Distract\n💟60", callback_data='distract'),],
            [InlineKeyboardButton("Jump\n💟45", callback_data='jump'),
           InlineKeyboardButton("Dance\n💟110", callback_data='dance'),],
         [InlineKeyboardButton(f"{special2}\n💟", callback_data=f'{special2}')],
    [InlineKeyboardButton("Resign", callback_data='wood'),InlineKeyboardButton("Draw", callback_data='wood')]
  ]
  
   reply_markup = InlineKeyboardMarkup(keyboard)
   if update.callback_query.from_user.id != p1id:
        query.answer('player 2 not ur turn')
        return None
   query.edit_message_text(
    text = f'<i><b>Round {rd}</b></i>\n'
    f'{p1}|{type1}\n💟Mana : {mana1}\n{bar1} {current1}/{hp1}\n\n{p2}|{type2}\n💟Mana : {mana1}\n{bar2} {current2}/{hp2}\n\n'
    f'<b>{p2} pick a move</b>', parse_mode = ParseMode.HTML, reply_markup = reply_markup)
   cd['round']+=1
   cd['choice1'] = query.data
   return PETTHREE
  
def resign(update , context):
  cd = context.bot_data
  query = update.callback_query
  query.answer()
  p1id = cd['p1id']
  keyboard = [
  [InlineKeyboardButton("Yes", callback_data='resignyes'),InlineKeyboardButton("No", callback_data='resignno')]
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)                                                                        
  if update.callback_query.from_user.id != p1id:
        query.answer('Cannot use')
        return None
  query.edit_message_text(f'{p1} are you sure to resisgn the match?', reply_markup = reply_markup)
  return PETTWO

  
def resign2(update ,context):
  cd = context.bot_data
  query = update.callback_query
  p1id = cd['p1id']
  p1 = cd['p1']
  p2 = cd['p2']
  p2id = cd['p2id']
  type1 = cd['type1'] 
  type2 = cd['type2']                                                                            
  if update.callback_query.from_user.id == p1id:
   if query.data == 'resignyes':
    query.edit_message_text(f'{p1} resign , {p2} and his/her {type2} won , congrats')
    return ConversationHandler.END 
  if update.callback_query.from_user.id == p1id:
   if query.data == 'resignno':
    return PETONE                                                                         
                                                                              
                                                                              
  if update.callback_query.from_user.id == p2id:
   if query.data == 'resignyes':
    query.edit_message_text(f'{p2} resign , {p1} and his/her {type1} won , congrats')
    return ConversationHandler.END                                                                               
  if update.callback_query.from_user.id == p2id:
   if query.data == 'resignno':
    return PETONE                                                                             
                                                                 
def draw(update , context):
  pass
  
def res(update , context):
  cd = context.bot_data
  query = update.callback_query
  query.answer()
  p1 = cd['p1']
  p1id = cd['p1id']
  p2 = cd['p2']
  p2id = cd['p2id']
  pet_id1 = DB.get_user_value(p1id , 'mainpet_id')
  pet_id2 = DB.get_user_value(p2id , 'mainpet_id')
  empty = '▒'
  full = '█'
  rd = cd['round']                                                                            
  cd['choice2']=query.data
  current1 = cd['hp1']
  current2 = cd['hp2']
  hp1 = cd['max1']
  hp2 = cd['max2']
                                                                              
  c1 = cd['choice1']
  c2 = cd['choice2'] 
  
  special1 = DB.get_user_pet_value(p1id ,pet_id1 , 'special')
  special2 = DB.get_user_pet_value(p2id ,pet_id2 , 'special')
  
  remain1 = current1*100/hp1
  remain2 = current2*100/hp2
 
  p1r1 = int((remain1+10)/10)
  p1r2 = int(11-p1r1)
  
  p2r1 = int((remain1+10)/10)
  p2r2 = int(11-p2r1)
  
  bar1 = p1r1*full+p1r2*empty
  bar2 = p2r1*full+p2r2*empty 
  
  type1 = cd['type1']
  type2 = cd['type2']
  
  mana1 = cd['mana1']
  mana2 = cd['mana2']
                                                                              
  pet_id1 = DB.get_user_value(p1id , 'mainpet_id')
  pet_id2 = DB.get_user_value(p2id , 'mainpet_id')
  
  talent1 = DB.get_user_pet_value(p1id , pet_id1 , 'talent')
  distract1 = DB.get_user_pet_value(p1id ,pet_id1 , 'distract')
  confident1 = DB.get_user_pet_value(p1id ,pet_id1 , 'confident')
  special1 = DB.get_user_pet_value(p1id ,pet_id1 , 'special')
  cd['type1'] = type1 = DB.get_user_pet_value(p1id ,pet_id1 , 'type')
  age1 = DB.get_user_pet_value(p1id ,pet_id1 , 'growth')
  
  #Game stats
  attack1 = talent1 + round(((age1+1)*talent1/4),0)
  defense1 = distract1 + round(((age1+1)*distract1/4),0)
  hp1 = confident1 + round(((age1+1)*confident1/4),0)
  
  talent2 = DB.get_user_pet_value(p2id, pet_id2, 'talent')
  distract2 = DB.get_user_pet_value(p2id, pet_id2 , 'distract')
  confident2 = DB.get_user_pet_value(p2id, pet_id2 , 'confident')
  special2 = DB.get_user_pet_value(p2id, pet_id2 , 'special')
  cd['type2'] = type2 = DB.get_user_pet_value(p2id, pet_id2 , 'type')
  age2 = DB.get_user_pet_value(p2id, pet_id2 , 'growth')
  
  #Game stats
  attack2 = talent2 + round(((age2+1)*talent2/4),0)
  defense2 = distract2 + round(((age2+1)*distract2/4),0)
  hp2 = confident2 + round(((age2+1)*confident2/4),0)                                                                         
 
  keyboard = [
           [InlineKeyboardButton("Shake\n💟0", callback_data='shake'),
            InlineKeyboardButton("Distract\n💟60", callback_data='distract'),],
            [InlineKeyboardButton("Jump\n💟45", callback_data='jump'),
           InlineKeyboardButton("Dance\n💟110", callback_data='dance'),],
         [InlineKeyboardButton(f"{special1}\n💟", callback_data=f'{special1}')],
    [InlineKeyboardButton("Resign", callback_data='wood'),InlineKeyboardButton("Draw", callback_data='wood')]
  ]
  
  reply_markup = InlineKeyboardMarkup(keyboard)                                                                            
  if update.callback_query.from_user.id != p2id:
     query.answer('player 2 not ur turn')
     return None
                                                                              
     
                                                                              
  pair = {'shake':{'attack':10, 'distract':0, 'energy':0},
         'distract':{'attack':0, 'distract':80, 'energy':60},
         'jump':{'attack':40, 'distract':0, 'energy':45},
         'dance':{'attack':110, 'distract':0, 'energy':90},}
                                                                              
                                                                              
  if c1 != 'distract' and c2 == 'distract':                                                                            
   result1 = (talent1*pair[c1]['attack']/100)-(distract2*pair['distract']['distract']/100)                                                                        
   if result1 >1:
      current2-=result1
      mana1-=pair[c1]['energy'] 
      mana2-=pair['distract']['energy']
                                                                              
      remain1 = current1*100/hp1
      remain2 = current2*100/hp2
  
      p1r1 = int((remain1+10)/10)
      p1r2 = int(11-p1r1)
  
      p2r1 = int((remain1+10)/10)
      p2r2 = int(11-p2r1)
  
      bar1 = p1r1*full+p1r2*empty
      bar2 = p2r1*full+p2r2*empty
      query.edit_message_text(f"<u>Round {rd}</u>\n\n{p1}'s <b>{type1} #{pet_id1}</b> performance of {c1} caused {p2}'s <b>{type2} #{pet_id2}</b> to lose <b>{result1}</b> confidence"
                              f"\n{p1}|{type1}\n{bar1} {current1}/{hp1}\n{p2}|{type2}\n{bar1} {current1}/{hp1}\n{p1} pick your move"
                               ,reply_markup=reply_markup, parse_mode = ParseMode.HTML)   
      if current1 or current2 <= 0:
         if current1 > current2:
           query.edit_message_text(f'{p1} win')
           ingame.remove(p1id)
           ingame.remove(p2id)
         elif current2 > current1:
           query.edit_message_text(f'{p2} win') 
           ingame.remove(p1id)
           ingame.remove(p2id)
                                                                              
         return ConversationHandler.END
      return PETONE                                                                       
                                                                              
   if result1 <=0:
      current2-=0                                                                        
      mana1-=pair[c1]['energy'] 
      mana2-=pair['distract']['energy']
      remain1 = current1*100/hp1
      remain2 = current2*100/hp2
  
      p1r1 = int((remain1+10)/10)
      p1r2 = int(11-p1r1)
  
      p2r1 = int((remain1+10)/10)
      p2r2 = int(11-p2r1)
  
      bar1 = p1r1*full+p1r2*empty
      bar2 = p2r1*full+p2r2*empty
      query.edit_message_text(f"<u>Round {rd}</u>\n\n{p1}'s <b>{type1} #{pet_id1}</b> performed {c1} and {p2}'s <b>{type2} #{pet_id2}</b> performed {c2} no stats affected this round"
                              f"\n{p1}|{type1}\n{bar1} {current1}/{hp1}\n{p2}|{type2}\n{bar1} {current1}/{hp1}\n{p1} pick your move"
                               ,reply_markup=reply_markup, parse_mode = ParseMode.HTML)   
      if current1 or current2 <= 0:
         if current1 > current2:
           query.edit_message_text(f'{p1} win')
           ingame.remove(p1id)
           ingame.remove(p2id)
         elif current2 > current1:
           query.edit_message_text(f'{p2} win')
           ingame.remove(p1id)
           ingame.remove(p2id)
                                                                              
         return ConversationHandler.END                                                                        
      return PETONE                                                                       
  
  if c1 == 'distract' and c2 == 'distract':
     mana1-=pair[c1]['energy'] 
     mana2-=pair[c2]['energy']   
  
  if c1 != 'distract' and c2 != 'distract':
     mana1-=pair[c1]['energy'] 
     mana2-=pair[c2]['energy']
     result2 = (talent1*pair[c1]['attack']/100)-(talent2*pair[c2]['attack']/100)
     result3 = (talent2*pair[c2]['attack']/100)-(talent1*pair[c1]['attack']/100)
     current1 -= result3
     current2 -= result2                                                                         
                                                                              










PETGAME_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('challenge', challenge)],
        states={
            PETONE: [CallbackQueryHandler(accept, pattern='^' + str("accept") + '$'),
                     CallbackQueryHandler(reject, pattern='^' + str("reject") + '$'),
                     CallbackQueryHandler(cancel, pattern='^' + str("cancel") + '$'),
                     CallbackQueryHandler(rules, pattern='^' + str("rules") + '$'),
                     CallbackQueryHandler(first, pattern='^' + str("shake") + '$'),
                     CallbackQueryHandler(first, pattern='^' + str("distract") + '$'),
                     CallbackQueryHandler(first, pattern='^' + str("dance") + '$'),
                     CallbackQueryHandler(first, pattern='^' + str("jump") + '$'),
                     CallbackQueryHandler(first, pattern='^' + str(".") + '$')
            ],
            PETTWO: [CallbackQueryHandler(resign2, pattern='^' + str("resignyes") + '$'),
                     CallbackQueryHandler(resign2, pattern='^' + str("resignno") + '$')],
                  
            PETTHREE: [CallbackQueryHandler(res, pattern='^' + str("shake") + '$'),
                       CallbackQueryHandler(res, pattern='^' + str("distract") + '$'),
                       CallbackQueryHandler(res, pattern='^' + str("dance") + '$'),
                       CallbackQueryHandler(res, pattern='^' + str("jump") + '$'),
                       CallbackQueryHandler(res, pattern='^' + str(".") + '$')
            ],
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=False
    )



dispatcher.add_handler(PETGAME_HANDLER)
