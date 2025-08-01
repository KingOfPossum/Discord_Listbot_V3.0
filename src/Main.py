from listbot.Bot import Bot

if __name__ == "__main__":
    bot = Bot(command_prefix="%",config_path="../ressources/config.yaml")
    bot.run()