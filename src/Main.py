#Add the IGDB-PythonWrapper to the path to be able to import it
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "IGDB-PythonWrapper"))

from common.ConfigLoader import ConfigLoader
from listbot.Bot import Bot

def main():
    ConfigLoader.set_config_path("../resources/config.yaml")
    bot = Bot()
    bot.run_bot()

if __name__ == "__main__":
    main()