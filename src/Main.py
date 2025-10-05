from common.ConfigLoader import ConfigLoader
from listbot.Bot import Bot

def main():
    ConfigLoader.set_config_path("../resources/config.yaml")
    bot = Bot()
    bot.run_bot()

if __name__ == "__main__":
    main()