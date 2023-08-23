import logging

from bot import Bot, BotConfig
from absalom import start, stop, confirm, cancel, message_parser

TOKEN = "6058068516:AAFqOMCHELD97B9rRGUp09LsF0QuQcLf2Aw"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def main(): 
    config = BotConfig()
    config.set_token(TOKEN)
    config.set_commands({
        "start": start,
        "stop": stop,
        "yes": confirm,
        "cancel": cancel
    })

    config.add_message_handler(message_parser)

    bot = Bot()
    bot.configure(config)

    bot.start()

if __name__ == '__main__':
    main()