import logging
import random
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)

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
            InlineKeyboardButton("accept", callback_data=str('yes')),
            InlineKeyboardButton("reject", callback_data=str('no')),
        ],
        [InlineKeyboardButton("rules", callback_data=str('rules'))],
        [InlineKeyboardButton("cancel", callback_data=str('cancel'))]
    ]
   reply_markup = InlineKeyboardMarkup(keyboard)
    
   if toid == context.bot.id:
     update.message.reply_text('cant challenge bot')
   if toid == id:
     update.message.reply_text('cant challenge yourself')
   if toid != id:
     update.message.reply_text(f'{name} challenged {to} to a pet 🌟talent show🌟\n\nClick accept to begin', parse_mode = ParseMode.HTML, reply_markup = reply_markup)
      
   return ONE
   
  
   
  
def reject(update , context):
  cd = context.bot_data
  query = update.callback_query
  query.answer()
  p2id = cd['p2id']
  p2 = cd[p2]
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
  if update.callback_query.from_user.id != p1id:
        query.answer('Cannot use')
        return None
    query.edit_message_text(f'{p1} cancelled the challenge')
    return ConversationHandler.END
  

def rules(update , context):
  cd = context.bot_data
  query = update.callback_query
  query.answer('pet that reach 0 confident loses')
  return 0
  
def accept(update, context):
  cd = context.bot_data
  query = update.callback_query
  query.answer()
  p1 = cd['p1']
  p1id = cd['p1id']
  p2 = cd['p2']
  p2id = cd['p2id']
  
  cd['round'] =  round = 1
  
  empty = ▒
  full = █
  
  pet_id1 = DB.get_user_value(p1id , 'mainpet_id')
  pet_id2 = DB.get_user_value(p2id , 'mainpet_id')
  
  talent1 = DB.get_user_pet_value(pet_id1 , 'talent')
  distract1 = DB.get_user_pet_value(pet_id1 , 'distract')
  confident1 = DB.get_user_pet_value(pet_id1 , 'confident')
  special1 = DB.get_user_pet_value(pet_id1 , 'special')
  type1 = DB.get_user_pet_value(pet_id1 , 'type')
  age1 = DB.get_user_pet_value(pet_id1 , 'growth')
  
  #Game stats
  attack1 = talent1 + round(((age1+1)*talent1/4),0)
  defense1 = distract1 + round(((age1+1)*distract1/4),0)
  hp1 = confident1 + round(((age1+1)*confident1/4),0)
  current1 = hp1
  
  talent2 = DB.get_user_pet_value(pet_id2, 'talent')
  distract2 = DB.get_user_pet_value(pet_id2 , 'distract')
  confident2 = DB.get_user_pet_value(pet_id2 , 'confident')
  special2 = DB.get_user_pet_value(pet_id2 , 'special')
  type2 = DB.get_user_pet_value(pet_id2 , 'type')
  age2 = DB.get_user_pet_value(pet_id2 , 'growth')
  
  #Game stats
  attack2 = talent2 + round(((age2+1)*talent2/4),0)
  defense2 = distract2 + round(((age2+1)*distract2/4),0)
  hp2 = confident2 + round(((age2+1)*confident2/4),0)
  current2 = hp2
  
  remain1 = current1*100/hp1
  remain2 = current1*100/hp1
  
  p1r1 = int((remain1+10)/10)
  p1r2 = int(11-p1r1)
  
  p2r1 = int((remain1+10)/10)
  p2r2 = int(11-p2r1)
  
  bar1 = p1r1*full+p1r2*empty
  bar2 = p2r1*full+p2r2*empty
  
  
  keyboard = [
           [InlineKeyboardButton("Shake\n💟0", callback_data='shake'),
            InlineKeyboardButton("Distract\n💟60", callback_data='distract'),],
            [InlineKeyboardButton("Jump\n💟45", callback_data='jump'),
           InlineKeyboardButton("Dance\n💟110", callback_data='dance'),],
         [InlineKeyboardButton(f"{special1}\n💟", callback_data=f'{special1}')],
    [InlineKeyboardButton("Resign", callback_data='wood'),InlineKeyboardButton("Draw", callback_data='wood')]
  ]
  
  reply_markup = InlineKeyboardMarkup(keyboard)
  query.edit_message_text(
    text = f'Round {round}\n'
    f'{p1}\n{type1}\n {bar1}\n\n{p2}\n{type2}\n{bar2}'
    f'{p1} pick a move', parse_mode = ParseMode.HTML, reply_markup = reply_markup)
  
  
def resign(update , context):
  cd = context.bot_data
  query = update.callback_query
  query.answer()
  p1id = cd['p1id']
  keyboard = [
  [InlineKeyboardButton("Yes", callback_data='shake',InlineKeyboardButton("No", callback_data='shake']
  ]
  reply_markup = InlineKeyboardMarkup(keyboard)                                                                        
  if update.callback_query.from_user.id != p1id:
        query.answer('Cannot use')
        return None
    query.edit_message_text(f'{p1} are you sure to resisgn the match?', reply_markup = reply_markup)

  
def resign2(update ,context):
  cd = context.bot_data
  query = update.callback_query
                                                                          
                                                                        
                                                                          
                                                                          
  
def draw(update , context):
  
  
  
  
  
  
  
  
  
  
  










PETGAME_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('challenge', challenge)],
        states={
            ONE: [CallbackQueryHandler(accpet, pattern='^' + str("accept") + '$'),
                  CallbackQueryHandler(reject, pattern='^' + str("reject") + '$'),
                  CallbackQueryHandler(cancel, pattern='^' + str("cancel") + '$'),
                   CallbackQueryHandler(rules, pattern='^' + str("rules") + '$')
            ],
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=True
    )



dispatcher.add_handler(PETGAME_HANDLER)
