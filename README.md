# Discord_Listbot_V3.0

## Description
This is a Discord bot I wrote. Its main functionality is to allow users to add video games they’ve played into a list so they can keep track of all the games they’ve completed.  
This includes giving them rankings or reviews. You can then view your own or your friends’ lists to see what games they’ve played and what they thought of them. The bot uses the IGDB database to fetch detailed information about a game, such as its cover art or genres.  
For this, I use my own IGDB wrapper, which you can find [here](https://github.com/KingOfPossum/IGDB-PythonWrapper).

Other functionalities of the bot include:
- Time tracking:  
  - Tracks the time you spend on specific applications (as long as they are visible in Discord).
- A token system:  
  - Users can earn tokens by adding games to their list (this feature was meant for a friend of mine, but currently has no real use).  
  - After earning a specific number of tokens, you receive coins (again, these currently have no real use).
- Specific bot replies:  
  - The bot will reply to messages containing specific keywords with a message. These can be customized by changing the `replies.yaml` file that is automatically generated in the `\resources` folder.
- Creating emojis for consoles:  
  - The bot will automatically create emojis in your server for consoles after adding a game with that console. You can disable this feature in the `config.yaml` file located in the `\resources` folder.
- A backlog system:  
  - You can add games to your backlog that you want to play in the future to keep track of them.  
  - You can also recommend games to other users. This will add the game to their backlog.  
  - You can get a random recommendation from your backlog if you can’t decide what to play next.
- Automatic updates:  
  - The bot will automatically check for updates once every minute. If there is a new version available, the bot will wait until all actions are finished and then restart itself to update to the newest version.
- Playing music from YouTube:  
  - You can play audio from YouTube videos and playlists.  
  - The audio is downloaded and cached for repeated usage to speed up the initialization of playing a new song.

Functionality that is planned for the future:
- Playlists for the music feature  
- Playing songs from Spotify  
- A website for better list management and more detailed statistics  
- A guessing game where the bot gives you information about a game from the database, like release year, genre, or user reviews, and you have to guess the game  

## Dependencies
In order to run the bot you will need to have some libraries installed. These are also listed in the `requirements.txt` file.  
- `discord.py`: The main library for the bot to interact with Discord  
- `PyYAML`: For reading and writing the config and replies YAML files  
- `requests`: For making requests to the IGDB API  
- `pynacl`: Needed for using Discord’s voice utilities  
- `yt-dlp`: Used for playing audio from YouTube  

## Bot Commands
The bot will listen to all commands that start with a specific prefix. The default one is `%`, but you can change it to whatever you want in the `config.yaml` file that is located in the `\resources` folder.

The bot will also have a help command that will list all commands, the way to use them, and a short description of what they do, but for documentation purposes, all commands are listed here as well.

### General Commands
- `%help`: Lists all commands with the way to use them and a short description.  
- `%randomize` `item1`, `item2`,...: Randomly selects one of the provided items.  
- `%randomizeNum` `min` `max`: Randomly selects a number between the provided min and max values (inclusive). If only one value is provided, a number between `0` and `max` is randomized.  
- `%activateBotReplies`: Activates bot replies completely.  
- `%deactivateBotReplies`: Deactivates bot replies completely.  
- `%toggleBotReplies`: Toggles the bot replies on or off for a specific channel if you would like to have the bot only reply in a specific channel.  

### List Commands
- `%add`: Shows a button that opens a Discord modal where you can add all information about the game that you want to add to your list.  
- `%update` `gameName`: Lets you update a game that is already in your list if you wish to change something about it. Works similarly to the `%add` command.  
- `%remove` `gameName`: Removes a specific game from your list.  
- `%replayed` `gameName`: Changes the replay status (showing if you have already played this game before) of a game.  
- `%completed` `gameName`: Changes the completion status (showing if you have 100% completed this game) of a game.  
- `%view` `gameName` `Optional(user)`: Shows all the information about a game from the database. If you provide a user, it will show the game entry from that user’s list.  
- `%list` `Optional(user)`: Shows the list of all games added by you or, if provided, by another user. If there were games added in another year, you can swap the list to that year by using a button on the list’s embed.  
- `%consoles`: Lists all consoles that have been played on together with their emojis if the feature is activated in the `config.yaml` file.  
- `%stats`: Shows some statistics about the server, like who has played the most games this year and the most active month/console.  
- `%info` `gameName`: Shows more general information about a game from the IGDB database. This includes a summary, genres, available consoles, and release date.  

### Token Commands
- `%addToken`: Adds one token to your account. After a specific number of tokens (default is 3), you will be rewarded with a coin.  
- `%removeCoin`: Removes one coin from your account.  
- `%setNeededTokens` `amount`: Sets the number of tokens needed to get a coin to `amount`.  
- `%viewTokens`: Shows how many tokens and coins you currently have and how many tokens you need to get the next coin.  

### Time Tracking Commands
- `%timeStats`: Shows all the time you or other users have spent on different applications that are visible in Discord.  

### Backlog Commands
- `%backlogAdd` `gameName`: Adds a game to your backlog.  
- `%backlogRemove` `gameName`: Removes a game from your backlog.  
- `%recommend` `gameName` `user`: Recommends a game to another user by adding it to their backlog.  
- `%getRecommendation`: Gives you a random recommendation from your backlog.  
- `%viewBacklog`: Shows all games in your backlog. It can also show the backlogs of other users.  

### Voice Commands
- `%join`: Makes the bot join your current voice channel, either joining directly or moving to it if the bot is in another channel.  
- `%leave`: Makes the bot leave its current voice channel.  
- `%play` `(url | searchquery)`: Makes the bot play the audio from a YouTube video or playlist. You can either provide a `url` directly to that video or a `searchquery`, which will result in the bot searching YouTube for a video.  
- `%pause`: Pauses the currently playing song.  
- `%resume`: Resumes the currently playing song.  
- `%stop`: Stops the currently playing song.  

## Setup
1. Clone the repository.  
2. Install the dependencies by running `pip install -r requirements.txt`.  
3. Create a Discord bot and get its API token.  
4. Invite the bot to your server with the following permissions:  
   - Read Messages  
   - Send Messages  
   - Manage Emojis and Stickers  
   - Use External Emojis  
   - View Channel  
5. Create an account on IGDB and get a Client ID and Client Secret.  
6. Run the bot by executing `python main.py` in your terminal. The first time this will fail, but it will create the `\resources` folder with all needed files like the databases and `config.yaml`.  
7. Open the `config.yaml` file located in the `\resources` folder and fill in your Discord bot token, IGDB Client ID, and Client Secret.  
8. (Optional) Change other settings in the `config.yaml` file to your liking.  
9. Restart the bot and enjoy.  
