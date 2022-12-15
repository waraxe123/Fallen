from telegram import TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler
from telegram.ext.dispatcher import CallbackContext

from FallenRobot import LOGGER, dispatcher
from FallenRobot.modules.helper_funcs.filters import CustomFilters


def snipe(update: Update, context: CallbackContext):
    args = context.args
    bot = context.bot
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError:
        update.effective_message.reply_text("Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text(
                "Couldn't send the message. Perhaps I'm not part of that group?"
            )


__help__ = """
*Dev  only:* 
• /snipe <chatid> <string>
Make me send a message to a specific chat.
"""

__mod_name__ = "Sɴɪᴘᴇ"

SNIPE_HANDLER = CommandHandler(
    "snipe", snipe, pass_args=True, filters=CustomFilters.dev_filter
)

dispatcher.add_handler(SNIPE_HANDLER)
