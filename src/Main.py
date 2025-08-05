
from listbot.Bot import Bot

def main():
    bot = Bot(command_prefix="%", config_path="../resources/config.yaml")
    bot.run()

if __name__ == "__main__":
    main()