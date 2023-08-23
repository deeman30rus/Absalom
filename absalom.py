from enum import Enum

from telegram import Update
from telegram.ext import ContextTypes

from records import parse_message, save_table

AUTHORIZED_USERS = [228490718, 5173382089]

class State(Enum):
    IDLE = 1,
    INPUT = 2, 
    CONFIRM = 3

class Event(Enum):
    COMMAND_START = 1,
    COMMAND_STOP = 2,
    COMMAND_CONFIRM = 3,
    COMMAND_CANCEL = 4,
    PARSE_MESSAGE = 5

__state = State.IDLE
__records = []

################################# API ##################################

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await __check_auth(update):
        return

    cur = __state

    if not __check_step(cur, Event.COMMAND_START):
        return


    await __do_start(update, context)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await __check_auth(update):
        return

    cur = __state

    if not __check_step(cur, Event.COMMAND_STOP):
        return

    await __do_stop(update, context)

async def confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
    if not await __check_auth(update):
        return 

    cur = __state

    if not __check_step(cur, Event.COMMAND_CONFIRM):
        return

    await __do_confirm(update, context)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await __check_auth(update):
        return

    cur = __state

    if not __check_step(cur, Event.COMMAND_CANCEL):
        return

    await __do_cancel(update, context)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO implement me
    pass

async def status(update: Update, contetx: ContextTypes.DEFAULT_TYPE) -> None: 
    # TODO implement me
    pass

async def message_parser(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await __check_auth(update): 
        return 

    cur = __state

    if not __check_step(cur, Event.PARSE_MESSAGE):
        return 

    await __do_parse_message(update, context)

################################# END API ##################################

async def __check_auth(update: Update) -> bool: 
    if not __authorize(update): 
        await update.message.reply_text("Я с незнакомцами не разговариваю")

        return False
    
    return True

def __authorize(update: Update) -> bool: 
    user_id = update.message.from_user.id
    return user_id in AUTHORIZED_USERS

def __check_step(cur: State, event: Event) -> bool:
    if event == Event.COMMAND_START:
        return __check_if_can_perform_start(cur) # продолжить отсюда

    if event == Event.COMMAND_STOP:
        return __check_if_can_perform_stop(cur)
    
    if event == Event.COMMAND_CONFIRM:
        return __check_if_can_perform_confirm(cur)

    if event == Event.PARSE_MESSAGE:
        return __check_if_can_parse_message(cur)

    if event == Event.COMMAND_CANCEL:
        return True


def __check_if_can_perform_start(state: State) -> bool: 
    return state == State.IDLE

def __check_if_can_perform_stop(state: State) -> bool:
    return state == State.INPUT

def __check_if_can_perform_confirm(state: State) -> bool:
    return state == State.CONFIRM

def __check_if_can_parse_message(state: State) -> bool:
    return state == State.INPUT

async def __do_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global __state

    await update.message.reply_text("Помедленней, пожалуйста, я записываю!")

    __state = State.INPUT

async def __do_stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global __state

    await update.message.reply_text("Ушёл искать пиксели для картинок.")

    filename = save_table(__records)

    await update.message.reply_photo(filename, caption="Ля какая красота получилась! Подтверждаем?")

    __state = State.CONFIRM


async def __do_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global __state, __records
    # await update.message.reply_photo 
    # todo fwd message to group

    await update.message.reply_text("представь что это картинка")

    __to_idle()

async def __do_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global __state

    await update.message.reply_text("Галя, у нас отмена!")

    __to_idle()

async def __do_parse_message(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    global __records

    record = parse_message(update.message.text)
    __records.append(record)

    await update.message.reply_text("ara, записал {p}".format(p=record.person()))


def __to_idle(): 
    global __state, __records

    __state = State.IDLE
    __records = []