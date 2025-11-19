# Discord_Listbot_V3.0
## Description
This is a Discord bot I wrote. Its main functionality is to allow users to add Video games they played into a list so you can keep track of all the games you have played.
This includes giving them rankings or reviews. You can then view your or your friends lists and see what games they have played and what they thought of them. The bot uses the IGDB Database for getting more detailed information about a game like its cover over genres.
For this I use my own IGDB wrapper that you can find [here](https://github.com/KingOfPossum/IGDB-PythonWrapper)

Other functionalities of the bot include:
 - Time tracking:
    - Tracks the time you spend on specific applications (As long as they are visible in Discord)
 - A token system:
    - Users can earn tokens by adding games to their list if they want (This feature was meant for a friend of mine but as for now it has no real use)
    - After earning a specific amount of tokens you get coins (As said before they have no real use)
 - Specific bot replies:
    - The bot will reply to messages that contain specific keywords with a message. These can be customized by changing the `replies.yaml` file that is automatically generated in the `\resources` folder
 - Creating emojis for consoles:
    - The bot will automatically create emojis in your server for consoles after adding a game with that console. You can disable this feature in the `config.yaml` file located in the `\resources` folder
 - A Backlog system:
    - You can add games to your backlog that you want to play in the future to keep track of them
    - You can also recommend games to other users. This will add the game to their backlog  
    - Also you can get a random recommendation from your backlog if you can't decide what to play next
 - Automatic Updates:
    - The bot will automatically check for updates once every minute. If there is a new version available the bot will wait until all actions are finished and then restart itself to update to the newest version
 - Playing Music from YouTube:
    - You can play audio from YouTube videos and playlists.
    - The audio is being downloaded to cache them for repeating usage to speed up the initialisation of playing a new song

Functionality that I plan for the future:
 - Playlists for the Music feature
 - Playing songs from Spotify
 - A website for better list management and more detailed statistics
 - A guessing game where the bot gives you information about a game from the database like release year, genre or reviews of users, and you have to guess the game

## Dependencies
In order to run the bot you will need to have some libraries installed. These are also listed in the `requirements.txt` file.  
- `discord.py` : The main library for the bot to interact with Discord
- `PyYAML` : For reading and writing the config and replies yaml files
- `requests` : For making requests to the IGDB API
- `pynacl` : Needed for using Discords voice utilities
- `yt-dlp` : Used for playing audio from YouTube

## Bot Commands
The bot will listen to all commands that start with a specific prefix. The default one is `%` but you can change it into whatever you want in the `config.yaml` file that is located in the `\resources` folder.

The bot will also have a help command that will list all commands, the way to use them, and a short description of what they do but for documentation purposes, I will list all commands here as well.

### General Commands
- `%help` : Lists all commands with the way to use them and a short description
- `%randomize` `item1`, `item2`,... : Randomly select one of the provided items
- `%randomizeNum` `min` `max` : Randomly select a number between the provided min and max values (inclusive). If only one value is provided a number between `0` and `max`is randomized
- `%activateBotReplies` : Activates bot replies completely
- `%deactivateBotReplies` : Deactivates bot replies completely
- `%toggleBotReplies` : This will toggle the bot replies on or off for a specific channel if you would like to have the bot only reply in specific channel

### List Commands
- `%add` : This will show up a button that opens a Discord modal where you can add all information about the game that you want to add to your list
- `%update` `gameName` : This lets you update a game that is already in your list if you wish to change something about it. Works similarly to the `!add` command
- `%remove` `gameName` : This will remove a specific game from your list
- `%replayed` `gameName` : This will change the replay status (Showing if you have already played this game before) of a game
- `%completed` `gameName` : This will change the completion status (Showing if you have 100% this game) of a game
- `%view` `gameName` `Optional(user)` : This will show you all the information about a game from the database. If you provide a user it will show you the game entry from that users list
- `%list` `Optional(user)` : This will show you the list of all games added by you or if provided by another user. If there were games added in another year you can swap the list to that year by using a button on the list's embed
- `%consoles` : This will list up all consoles that have been played on together with its emojis if the feature is activated in the `config.yaml` file
- `%stats` : This will show you some statistics about the server. Like who has played the most games this year, the most active month/console
- `%info` `gameName` : This will show you more general information about a game from the IGDB database. These include a summary, genres,available consoles and release date

### Token Commands
- `%addToken` : This will add one token to your account. After a specific amount of tokens (default is 3), you will be rewarded with a coin
- `%removeCoin` : This will remove one coin from your account
- `%setNeededTokens` `amount` : This will set the amount of tokens needed to get a coin to `amount`
- `%viewTokens` : This will show you how many tokens and coins you currently have and how many tokens you need to get the next coin

### Time Tracking Commands
- `%timeStats` : This will show you all the time you or other users have spent on different applications that are visible in Discord

### Backlog Commands
- `%backlogAdd` `gameName`: This will add a game to your backlog
- `%backlogRemove` `gameName`: This will remove a game from your backlog
- `%recommend` `gameName` `user`: This will recommend a game to another user by adding it to their backlog
- `%getRecommendation` : This will give you a random recommendation from your backlog
- `%viewBacklog` : This will show you all games in your backlog. Can also show you backlogs of other users

### Voice Commands
- `%join` : This will make the bot join your current voice channel. Either joining directly or moving to it if the bot is in another channel
- `%leave` : This will let the bot leave from his current voice channel
- `%play` `(url | searchquery)` : This will make the bot play the audio from  a YouTube video or playlist. You can either provide a `url` directly to that video or a `searchquery` which will result in the bot searching YouTube for a video.
- `%pause` : Will pause the currently played song
- `%resume` : Will resume the currently played song
- `%stop` : Will stop the currently played song

## Setup
1. Clone the repository
2. Install the dependencies by running `pip install -r requirements.txt`
3. Create a Discord bot and get its api token
4. Invite the bot to your server with the following permissions:
    - Read Messages
    - Send Messages
    - Manage Emojis and Stickers
    - Use External Emojis
    - View Channel
5. Create an account on IGDB and get a client ID and client secret
6. Run the bot by executing `python main.py` in your terminal. The first time this will fail, but it will create the `\resources` folder with all needed files like the databases and `config.yaml`
7. Open the `config.yaml` file located in the `\resources` folder and fill in your Discord bot token, IGDB client ID and client secret
8. (Optional) Change other settings in the `config.yaml` file to your liking
9. Restart the bot and enjoy