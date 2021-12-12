import logging
from main import dispatcher 
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
from main import database as DB
ONE , TWO , THREE , FOUR , FIRST , SECOND,  *_ = range(50)

dict = {'white': 1, 'red': 5, 'orange': 25, 'yellow': 100, 'blue': 500, 'purple': 2000, 'black': 15000}
colours = ["white", "red", "orange", "yellow", "blue", "purple", "black"]

MIN_CHIP_AMOUNT = 1
MAX_CHIP_AMOUNT = 10

logger = logging.getLogger(__name__)

def wheel(update , context):
    '''Chat = update.effective_chat
        if update.effective_chat.type != Chat.PRIVATE:
            update.message.reply_text("play in pm")
            return -1'''
    cd = context.chat_data
    id = update.message.from_user.id
    name = update.message.from_user.first_name
    username = update.message.from_user.name
    VIP = DB.get_user_value(id, "vip")
    cd["worth"] = worth = DB.get_user_value(id, "worth")
    cd["white"] = white = DB.get_user_value(id, "white")
    cd["red"] = red = DB.get_user_value(id, "red")
    cd["orange"] = orange = DB.get_user_value(id, "orange")
    cd["yellow"] = yellow = DB.get_user_value(id, "yellow")
    cd["blue"] = blue = DB.get_user_value(id, "blue")
    cd["purple"] = purple = DB.get_user_value(id, "purple")
    cd["black"] = black = DB.get_user_value(id, "black")

    cd['amount'] = amount = 1

    value = (cd['white'] * 1) + (cd['red'] * 5) + (cd['orange'] * 25) + (cd['yellow'] * 100) + (cd['blue'] * 500) + (
                cd['purple'] * 2500) + (cd['black'] * 15000)

    cd["using"] = using = "white"

    keyboard = [
        [InlineKeyboardButton("Check Odd", callback_data="check"),
         InlineKeyboardButton("change chip", callback_data="chip")],
        [InlineKeyboardButton(" - ", callback_data="minus"), InlineKeyboardButton(f"{amount}", callback_data="amount"),
         InlineKeyboardButton(" + ", callback_data="add")],
        [InlineKeyboardButton("Play", callback_data="play")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if cd.get('wheel_main_message', False):
        cd['wheel_main_message'].delete()
        del cd['wheel_main_message']

    cd['wheel_main_message'] = update.message.reply_text(f"<b><u>Wheel</u></b>\n"
                              f"<i>Net Worth</i> : {value}$\n\n"
                              f"<b>⚪️White Chip</b> : {white}\n"
                              f"<b>🔴Red Chip</b> : {red}\n"
                              f"<b>🟠Orange Chip</b> : {orange}\n"
                              f"<b>🟡Yellow Chip</b> : {yellow}\n"
                              f"<b>🔵Blue Chip</b> : {blue}\n"
                              f"<b>🟣Purple Chip</b> : {purple}\n"
                              f"<b>⚫Black Chip</b> : {black}\n\n"
                              f"Chip in use : {using} chip\nBet amount : {amount}\nBet size : {dict['white'] * amount}$\n\n"
                              , reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    if cd.get('display', False):
        cd['display'].delete()
        del cd['display']

    cd['display'] = context.bot.send_photo(chat_id=update.message.chat.id,
                                           photo="https://telegra.ph/file/735959f85badb6b405033.jpg",
                                           caption=
                                           "<b>Spin the Wheel and make some gains!</b>",
                                           parse_mode=ParseMode.HTML)

    return TWO

def wheelback(update , context):
    cd = context.chat_data
    query = update.callback_query
    query.answer()
    white = cd['white']
    red = cd['red']
    orange = cd['orange']
    yellow = cd['yellow']
    blue = cd['blue']
    purple = cd['purple']
    black = cd['black']
    print("back")
    dict = {'white': 1, 'red': 5, 'orange': 25, 'yellow': 100, 'blue': 500, 'purple': 2000, 'black': 15000}


    cd["amount"] = amount = 1
    using = cd["using"]

    value = (cd['white'] * 1) + (cd['red'] * 5) + (cd['orange'] * 25) + (cd['yellow'] * 100) + (cd['blue'] * 500) + (
                cd['purple'] * 2500) + (cd['black'] * 15000)
    '''Chat = update.effective_chat
    if update.effective_chat.type != Chat.PRIVATE:
        update.message.reply_text("play in pm")
        return -1'''
    keyboard = [
        [InlineKeyboardButton("check odd", callback_data="check"),
         InlineKeyboardButton("change chip", callback_data="chip")],
        [InlineKeyboardButton(" - ", callback_data="minus"), InlineKeyboardButton(f"{amount}", callback_data="amount"),
         InlineKeyboardButton(" + ", callback_data="add")],
        [InlineKeyboardButton("Play", callback_data="play")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"<b><u>Wheel</u></b>\n"
                            f"<i>Net Worth</i> : {value}$\n\n"
                            f"<b>⚪️White Chip</b> : {white}\n"
                            f"<b>🔴Red Chip</b> : {red}\n"
                            f"<b>🟠Orange Chip</b> : {orange}\n"
                            f"<b>🟡Yellow Chip</b> : {yellow}\n"
                            f"<b>🔵Blue Chip</b> : {blue}\n"
                            f"<b>🟣Purple Chip</b> : {purple}\n"
                            f"<b>⚫Black Chip</b> : {black}\n\n"
                            f"Chip in use : {using} chip\nBet amount : {amount}\nBet size : {dict['white'] * amount}$\n\n"
                           , reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    return TWO

def wheelcheckodd(update , context):
    cd = context.chat_data
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Back", callback_data="back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Here are the odd of the wheel game\n\n"
                            "<b>Grey</b> -       0x -      (15/30)\n"
                            "<b>Green</b> -     1.5x -   (6/30)\n"
                            "<b>White</b> -      1.7x -   (1/30)\n"
                            "<b>Yellow</b> -     2x -      (6/30)\n"
                            "<b>Purple</b> -     3x -      (1/30)\n"
                            "<b>Orange</b> -   4x -      (1/30)\n", reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return TWO
def wheelselectchip(update , context):
    print("select")
    cd = context.chat_data
    query = update.callback_query
    query.answer()
    text = "<b><u>Values of each chips</u></b>\n\n⚪️ white chip : 1$\n" \
           "🔴 red chip : 5$\n🟠 orange chip : 25$\n🟡 yellow chip : 100$\n🔵 blue chip : 500$" \
           "\n🟣 purple chip : 2000$\n⚫️ black chip : 15000$\n\n click below to switch out chips"
    keyboard = [
        [InlineKeyboardButton("⚪ white", callback_data="white"),
         InlineKeyboardButton("🔴red", callback_data="red")
         ],
        [InlineKeyboardButton("🟠orange", callback_data="orange"),
         InlineKeyboardButton("🟡yellow", callback_data="yellow")
         ],
        [InlineKeyboardButton("🔵blue", callback_data="blue"),
         InlineKeyboardButton("🟣purple", callback_data="purple"),
         InlineKeyboardButton("⚫️Black", callback_data="black")],
        [InlineKeyboardButton("Back", callback_data="back")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    return THREE


def wheelchangechip(update, context):
    query = update.callback_query
    query.answer()
    cd = context.chat_data

    # TODO: return to last page
    if query.data == "back":
        return

    cd["using"] = query.data if query.data in colours else cd["using"]
    query.message = query.message.reply_to_message
    return wheel(query, context)

def wheelinc(update, context):
    query = update.callback_query
    cd = context.chat_data
    if cd['amount'] >= MAX_CHIP_AMOUNT:
        query.answer("max chip reached, try change to other chip", show_alert=True)
        return

    query.answer()
    cd["amount"] += 1
    query.message = query.message.reply_to_message
    return wheel(query, context)


def wheeldec(update, context):
    update.callback_query.answer()
    cd = context.chat_data
    cd["amount"] -= 1 if cd["amount"] > MIN_CHIP_AMOUNT else 0
    query.message = query.message.reply_to_message
    return wheel(query, context)


def wheelplay(update, context):
    cd = context.chat_data
    print('play')
    query = update.callback_query
    query.answer()
    msg = cd['display']
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

    req = query.data.split(':')
    logger.info(str(req))
    # check if enough chips
    if cd[cd['using']] <= 0:
        query.edit_message_text("not enough chips")
        return

    aa = random.choices(wheely)
    cd['bb'] = bb = aa[0]['mult']
    cd['pic'] = pic = aa[0]['pic']

    dict = {'white': 1, 'red': 5, 'orange': 25, 'yellow': 100, 'blue': 500, 'purple': 2000, 'black': 15000}
    cd['amount'] = amount = 1
    using = cd['using']

    value = (cd['white'] * 1) + (cd['red'] * 5) + (cd['orange'] * 25) + (cd['yellow'] * 100) + (cd['blue'] * 500) + (
            cd['purple'] * 2500) + (cd['black'] * 15000)
    '''Chat = update.effective_chat
    if update.effective_chat.type != Chat.PRIVATE:
        update.message.reply_text("play in pm")
        return -1'''
    cd["using"] = using = "⚪️ white chip"

    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=msg.message_id)

    keyboard = [
        [InlineKeyboardButton("Check Odd", callback_data="check"),
         InlineKeyboardButton("change chip", callback_data="chip")],
        [InlineKeyboardButton(" - ", callback_data="minus"), InlineKeyboardButton(f"{amount}", callback_data="amount"),
         InlineKeyboardButton(" + ", callback_data="add")],
        [InlineKeyboardButton("Play", callback_data="play")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # u can replace this if else with the suggestion u mentioned in tg

    reply = "<b>Wheel result : {}x\n\n" \
            "You bet {}$ and {} {}$!!\n{}</b>" \
        .format(bb, dict['white'] * amount,
                "won" if bb else "loss",
                dict['white'] * amount * bb,
                "Congrats" if bb else "._____.")

    cd['display'] = context.bot.send_photo(chat_id=update.effective_chat.id,
                                           photo=pic,
                                           caption=reply,
                                           parse_mode=ParseMode.HTML)

    query.edit_message_text(f"<b><u>Wheel</u></b>\n"
                            f"<i>Net Worth</i> : {value}$\n\n"
                            f"<b>⚪️White Chip</b> : {white}\n"
                            f"<b>🔴Red Chip</b> : {red}\n"
                            f"<b>🟠Orange Chip</b> : {orange}\n"
                            f"<b>🟡Yellow Chip</b> : {yellow}\n"
                            f"<b>🔵Blue Chip</b> : {blue}\n"
                            f"<b>🟣Purple Chip</b> : {purple}\n"
                            f"<b>⚫Black Chip</b> : {black}\n\n"
                            f"Chip in use : {using} chip\nBet amount : {amount}\nBet size : {dict['white'] * amount}$\n\n"
                            , reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    del cd['display']
    return TWO



WHEEL_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('wheel', wheel, pass_user_data=True)],
        states={
            TWO: [CallbackQueryHandler(wheelback, pattern="^back$", pass_user_data=True),
                  CallbackQueryHandler(wheelcheckodd, pattern="^check$", pass_user_data=True),
                  CallbackQueryHandler(wheelplay, pattern="^play$", pass_user_data=True),
                  CallbackQueryHandler(wheelselectchip, pattern="^chip$", pass_user_data=True),
                  CallbackQueryHandler(wheelinc, pattern="^inc$", pass_user_data=True),
                  CallbackQueryHandler(wheeldec, pattern="^dec$", pass_user_data=True)
            ],
            THREE: [CallbackQueryHandler(wheelchangechip, pattern="^.+$")]
        },
        fallbacks=[],
        allow_reentry=True,
        per_user=True
    )

dispatcher.add_handler(WHEEL_HANDLER)
