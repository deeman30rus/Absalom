
from typing import TypedDict
from telegram.ext import Application, CommandHandler, MessageHandler, filters

class BotConfig:
    __token = ""
    __handler = None
    __commands = {}

    def token(self) -> str: 
        return self.__token

    def set_token(self, token: str) -> None: 
        self.__token = token

    def commands(self) -> TypedDict: 
        return self.__commands

    def set_commands(self, commands: TypedDict) -> None:
        self.__commands = commands

    def add_message_handler(self, handler) -> None:
        self.__handler = handler

    def message_handler(self): 
        return self.__handler



class Bot: 

    __application = None

    def configure(self, config: BotConfig):
        self.__apply_config(config)

    def start(self):
        self.__application.run_polling()

    def __apply_config(self, config: BotConfig): 
        builder = Application.builder()

        self.__application = builder.token(config.token()).build()

        for name, handler in config.commands().items(): 
            self.__application.add_handler(CommandHandler(name, handler))

        self.__application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, config.message_handler()))
