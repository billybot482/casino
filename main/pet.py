import logging
import enum
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
ONE , TWO , THREE , FOUR , FIVE , SIX , FIRST , SECOND,  *_ = range(50)
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
    cats = DB.get_cat(id)
    dogs =  DB.get_dog(id)
    fish =  DB.get_fish(id)
    slot = DB.get_user_value(id , 'slots')
    pets = len(DB.get_pet(id))
   
    text = '<b>My pet collection</b>\n\n'
    catlist = ''
    doglist = ''
    fishlist = ''
    for i in cats:
     for k in i:    
      catlist +='Cat  '+ '#'+str(k)+'\n'
    
    for i in dogs:
     for k in i:    
      doglist +='Dog  '+ '#'+str(k)+'\n'
      
    for i in fish:
     for k in i:    
      fishlist +='Fish  '+ '#'+str(k)+'\n'
       
    update.message.reply_text(f'{text}{catlist}{doglist}{fishlist}\nPet: {pets}/{slots}', parse_mode = ParseMode.HTML)


   

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
     if len(keyboard)>0:
      update.message.reply_text(f'Which of this {type} would you like to inspect:', reply_markup =  reply_markup)
     else:
      update.message.reply_text("You dont have this type of pet yet")
   
    elif type == "dog":
     keyboard = []
     for i in dogs:
      for k in i:    
       keyboard.append([InlineKeyboardButton(f'Dog #{str(k).zfill(3)}', callback_data=f'{k}')])
   
     reply_markup = InlineKeyboardMarkup(keyboard)
     if len(keyboard)>0:
      update.message.reply_text(f'Which of this {type} would you like to inspect:', reply_markup =  reply_markup)
     else:
      update.message.reply_text("You dont have this type of pet yet")
   
    elif type == "fish":
     keyboard = []
     for i in fish:
      for k in i:    
       keyboard.append([InlineKeyboardButton(f'Fish #{str(k).zfill(3)}', callback_data=f'{k}')])
   
     reply_markup = InlineKeyboardMarkup(keyboard)
     if len(keyboard)>0:
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
   cd['pet_id'] = pet_id
   query.answer()
   img = ''
   cd['age'] = age = DB.get_user_pet_value(id, pet_id , 'growth')
   cd['talent'] = talent = DB.get_user_pet_value(id, pet_id , 'talent')
   cd['distract'] = distract = DB.get_user_pet_value(id, pet_id , 'distract')
   cd['confident'] = confident = DB.get_user_pet_value(id, pet_id , 'confident')
   cd['rarity'] = rarity = DB.get_user_pet_value(id, pet_id , 'rarity')
   cd['baby'] = baby = DB.get_user_pet_value(id, pet_id , 'baby')
   cd['teen'] = teen = DB.get_user_pet_value(id, pet_id , 'teen')
   cd['adult'] = adult = DB.get_user_pet_value(id, pet_id , 'adult')
   cd['special'] = special = DB.get_user_pet_value(id, pet_id , 'special')
   
   max_talent = DB.get_user_pet_value(id, pet_id , 'max_talent')
   max_distract = DB.get_user_pet_value(id, pet_id , 'max_distract')
   max_confident = DB.get_user_pet_value(id, pet_id , 'max_confident')
   
   if age >= 0 and age <=4:
      img+= DB.get_user_pet_value(id, pet_id , 'baby')
   elif age >4 and age <8:
      img+=DB.get_user_pet_value(id, pet_id , 'teen')
   elif age >=8:
      img +=DB.get_user_pet_value(id, pet_id , 'adult')

   keyboard = [
        [InlineKeyboardButton('set as main', callback_data='main'),InlineKeyboardButton('close', callback_data='close') ]
    ]
   reply_markup = InlineKeyboardMarkup(keyboard)
   
   text1 = f"\n<b>Base stats</b>\n🔆 <b>Talent :</b> <code>{talent}/{max_talent}</code>\n♨️ <b>Distract :</b> <code>{distract}/{max_distract}</code>\n❤‍🔥 <b>Confident : </b><code>{confident}/{max_confident}</code>\n\n<b>Rarity : <u>{rarity}</u></b>"
   text2 = f'<b>{type} #{str(query.data).zfill(3)}</b>\n\n<b>Growth level : {age}</b>\n🔆 <b>Talent :</b> <code>{talent}</code>\n♨️ <b>Distract :</b> <code>{distract}</code>\n❤‍🔥 <b>Confident : </b><code>{confident}</code>\n'
   cd['a'] = a = context.bot.send_photo(chat_id = update.effective_chat.id , photo = img, caption = text2 + text1 ,parse_mode = ParseMode.HTML, reply_markup = reply_markup)
   return SIX
   
def checkclose(update , context):
   cd = context.chat_data
   query = update.callback_query
   context.bot.delete_message(chat_id = update.effective_chat.id , message_id = cd['a'].message_id)
   return ConversationHandler.END
   
def mainpet(update , context):
   cd = context.chat_data
   query = update.callback_query
   id = cd['id']
   type = cd['type']
   pet_id = cd['pet_id']
   age =cd['age']
   talent = cd['talent']
   distract = cd['distract']
   confident = cd['confident']
   baby = cd['baby']
   teen = cd['teen']
   adult = cd['adult']
   special =cd['special']
   rarity = cd['rarity']
   
   try:
    check = DB.get_user_mainpet(id , 'pet_id')
   except TypeError:
    DB.add_main_pet(type , id , pet_id , baby , teen , adult , age , talent , distract , confident , rarity , special)
    query.answer(f'{type} #{pet_id} is now your main pet')
    return -1
   
   DB.main_pet(type, pet_id , baby , teen , adult , age , talent , distract , confident , rarity , special)
   query.answer(f'{type} #{pet_id} is now your main pet')
   return None 
  
def mymainpet(update , context):
   id = update.effective_user.id
   pet_id = DB.get_user_mainpet(id , 'pet_id')
   tag = str(pet_id).zfill(3)
   talent = DB.get_user_mainpet(id , 'talent')
   distract = DB.get_user_mainpet(id , 'distract')
   confident = DB.get_user_mainpet(id , 'confident')
   special = DB.get_user_mainpet(id , 'special')
   rarity = DB.get_user_mainpet(id , 'rarity')
   age = DB.get_user_mainpet(id , 'growth')
   type = DB.get_user_mainpet(id , 'type')
   img = ''
   if age >= 0 and age <=4:
      img+=DB.get_user_mainpet(id , 'baby')
   elif age >4 and age <8:
      img+=DB.get_user_mainpet(id , 'teen')
   elif age >=8:
      img +=DB.get_user_mainpet(id , 'adult')
  
   text2 = f'<b>{type} #{tag}</b>\n\n<b>Growth level : {age}</b>\n🔆 <b>Talent :</b> <code>{talent}</code>\n♨️ <b>Distract :</b> <code>{distract}</code>\n❤‍🔥 <b>Confident : </b><code>{confident}</code>\n'
   
   context.bot.send_photo(chat_id = update.effective_chat.id , photo = img, caption = text2 ,parse_mode = ParseMode.HTML)

   

 
   
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
            FIVE: [CallbackQueryHandler(check2, pattern=".", pass_user_data=True)
                  ],
                  
           
            SIX: [CallbackQueryHandler(mainpet, pattern="main", pass_user_data=True),
                  CallbackQueryHandler(checkclose, pattern="close", pass_user_data=True)
            ]
                  
        },
        fallbacks=[],
        allow_reentry=True,
        per_user=True
    )



MYPET_HANDLER = CommandHandler('mypet', mypet)
PETCONTROL_HANDLER = CommandHandler('petcontrol', petcontrol)
MINT_HANDLER = CommandHandler('mint', mint)
MAINPET_HANDLER = CommandHandler('mainpet', mymainpet)


dispatcher.add_handler(MINT_HANDLER)
dispatcher.add_handler(MYPET_HANDLER)
dispatcher.add_handler(PETCONTROL_HANDLER)
dispatcher.add_handler(BUYSLOT_HANDLER)
dispatcher.add_handler(CHECK_HANDLER)
dispatcher.add_handler(MAINPET_HANDLER)





