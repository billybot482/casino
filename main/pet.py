import logging
import enum
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
ONE , TWO , THREE , FOUR , FIVE , FIRST , SECOND,  *_ = range(50)
owners = [163494588]


def mint(update , context):
   id = update.effective_user.id
   type = update.message.text.split()[1]
   amount = int(update.message.text.split()[2])
   if id in owners:
      DB.mint_pet(type , amount)
      update.message.reply_text(f'minted extra {amount} {type}')
   else:
      update.message.reply_text(f'not authorised')
      
def petcontrol(update , context):
   id = update.effective_user.id
   check = len(DB.quantity_cat())
   if check ==1:
      update.message.reply_text('pet control already initiated')
      return -1
   if id in owners:
      DB.pet_control()
      update.message.reply_text(f'added pet control system')
   else:
      update.message.reply_text(f'not authorised')
      
      
def buyslot(update , context):
   cd = context.chat_data
   query = update.callback_query
   cd['id'] = id = update.effective_user.id
   name = update.effective_user.first_name
   username = update.effective_user.name
   slot = DB.get_user_value(id , 'slots')
   cd['purple'] = purple = round(DB.get_user_value(id, "purple"),4)
   cd['cost'] = cost =slot*slot
   keyboard = [
        [InlineKeyboardButton('Confirm', callback_data='confirm'), InlineKeyboardButton('cancel', callback_data='cancel')]
    ]
   reply_markup = InlineKeyboardMarkup(keyboard)
      
   update.message.reply_text(f'Are you sure to spend {cost}🟣 to increase slot by 1 ? \n\n'
                              f'current slot : <b>{slot}</b>\nNew slot : {slot+1}', parse_mode = ParseMode.HTML, reply_markup = reply_markup)  
    
   return TWO

def buy_res(update , context): 
   cd = context.chat_data
   query = update.callback_query
   purple = cd['purple']
   cost = cd['cost']
   id = cd['id']
   if query.data == 'cancel':
      query.edit_message_text('cancelled')
      return -1
   if query.data == 'confirm':
      if purple>=cost:
         query.edit_message_text('successfully purchased additional slot')
         DB.add_slot(id, 1)
         DB.sub_chip(id , 'purple', cost)
         return -1
      if purple < cost:
         query.edit_message_text('Balance not enough')
         return -1
   

def mypet(update , context):
   cd = context.chat_data
   query = update.callback_query
   id = update.effective_user.id
   name = update.effective_user.first_name
   username = update.effective_user.name
   n = 1
   text = '' 
   cat_id = DB.get_cat(id)
   for i in cat_id:
    text += str(n)+'.'+ ' Cat #'+str(i).zfill(3)+'\n'
    n+=1
   update.message.reply_text('Pet collection\n\n{text}')
   

def check(update , context):
    cd = context.chat_data
    query = update.callback_query
    cd['id'] = id = update.effective_user.id
    try:  
     cd['type'] = type = update.message.text.split()[1]
    except IndexError:
      update.message.reply_text('check info of your pet by typing \n\n/check <type of pet>\n\ncat , dog , etc')
      return -1
    cats = DB.get_cat(id)
    dogs =  DB.get_dog(id)
    fish =  DB.get_fish(id)

    if type == "cat":
     keyboard = []
     for i in cats:
      for k in i:    
       keyboard.append([InlineKeyboardButton(f'cat #{str(k).zfill(3)}', callback_data=f'{k}')])
   
     reply_markup = InlineKeyboardMarkup(keyboard)
     if len(keyboard)>0
      update.message.reply_text(f'Which of this {type} would you like to inspect:', reply_markup =  reply_markup)
     else:
      update.message.reply_text("You dont have this type of pet yet")
   
    elif type == "dog":
     keyboard = []
     for i in dogs:
      for k in i:    
       keyboard.append([InlineKeyboardButton(f'Dog #{str(k).zfill(3)}', callback_data=f'{k}')])
   
     reply_markup = InlineKeyboardMarkup(keyboard)
     if len(keyboard)>0
      update.message.reply_text(f'Which of this {type} would you like to inspect:', reply_markup =  reply_markup)
     else:
      update.message.reply_text("You dont have this type of pet yet")
   
    elif type == "fish":
     keyboard = []
     for i in fish:
      for k in i:    
       keyboard.append([InlineKeyboardButton(f'Fish #{str(k).zfill(3)}', callback_data=f'{k}')])
   
     reply_markup = InlineKeyboardMarkup(keyboard)
     if len(keyboard)>0
      update.message.reply_text(f'Which of this {type} would you like to inspect:', reply_markup =  reply_markup)
     else:
      update.message.reply_text("You dont have this type of pet yet")
   
   
    else:
     update.message.reply_text("Wrong input") 
    return FIVE

def check2(update ,context):
   cd = context.chat_data
   query = update.callback_query
   id = cd['id']
   type = cd['type']
   pet_id = query.data
   query.answer()
   img = ''
   age = DB.get_user_pet_value(id, pet_id , 'growth')
   talent = DB.get_user_pet_value(id, pet_id , 'talent')
   distract = DB.get_user_pet_value(id, pet_id , 'distract')
   confident = DB.get_user_pet_value(id, pet_id , 'confident')
   rarity = DB.get_user_pet_value(id, pet_id , 'rarity')
   
   max_talent = DB.get_user_pet_value(id, pet_id , 'max_talent')
   max_distract = DB.get_user_pet_value(id, pet_id , 'max_distract')
   max_confident = DB.get_user_pet_value(id, pet_id , 'max_confident')
   
   if age >= 0 and age <=4:
      img+= DB.get_user_pet_value(id, pet_id , 'baby')
   elif age >4 and age <8:
      img+=DB.get_user_pet_value(id, pet_id , 'teen')
   elif age >=8:
      img +=DB.get_user_pet_value(id, pet_id , 'adult')

      
   text1 = f"\n<b>Base stats</b>\n🔆 <b>Talent :</b> <code>{talent}/{max_talent}</code>\n♨️ <b>Distract :</b> <code>{distract}/{max_distract}</code>\n❤‍🔥 <b>Confident : </b><code>{confident}/{max_confident}</code>\n\n<b>Rarity : <u>{rarity}</u></b>"
   text2 = f'<b>{type} #{str(query.data).zfill(3)}</b>\n\n<b>Growth level : {age}</b>\n🔆 <b>Talent :</b> <code>{talent}</code>\n♨️ <b>Distract :</b> <code>{distract}</code>\n❤‍🔥 <b>Confident : </b><code>{confident}</code>\n'
   
   context.bot.send_photo(chat_id = update.effective_chat.id, photo = img, caption = text2 + text1 ,parse_mode = ParseMode.HTML)
   return ConversationHandler.END
   

BUYSLOT_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('buyslot', buyslot, pass_user_data=True)],
        states={
            TWO: [CallbackQueryHandler(buy_res, pattern="^confirm$", pass_user_data=True),
                  CallbackQueryHandler(buy_res, pattern="^cancel$", pass_user_data=True)],
        },
        fallbacks=[],
        allow_reentry=True,
        per_user=True
    )

CHECK_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('check', check, pass_user_data=True)],
        states={
            FIVE: [CallbackQueryHandler(check2, pattern=".", pass_user_data=True)],
        },
        fallbacks=[],
        allow_reentry=True,
        per_user=True
    )



MYPET_HANDLER = CommandHandler('mypet', mypet)
PETCONTROL_HANDLER = CommandHandler('petcontrol', petcontrol)
MINT_HANDLER = CommandHandler('mint', mint)


dispatcher.add_handler(MINT_HANDLER)
dispatcher.add_handler(MYPET_HANDLER)
dispatcher.add_handler(PETCONTROL_HANDLER)
dispatcher.add_handler(BUYSLOT_HANDLER)
dispatcher.add_handler(CHECK_HANDLER)





