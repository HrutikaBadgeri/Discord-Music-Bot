# Vanilla Discord Music Bot 🎶

### Highlights 
  - Simple & easy to use
  - YouTube support 
  - Personalized server access
  
### Commands

Here are all the available commands in the bot!
prefix used: >

|      Name                   |            Description                                              | 
|:----------------------------|:------------------------------------------------------------------: |
| **help/h**                  |Displays all the available commands                                  |  
| **join/j**                  |The bot will join the respective voice channel                       | 
| **play/p**                  |Finds the song on youtube and plays it in your current channel       |
| **queue/q**                 |Displays the current music queue                                     |    
| **skip/s**                  |Skips the current song being played                                  | 
| **clear/c**                 |Stops the music and clears the queue                                 |  
| **stop/st**                 |Stops the bot from playing music                                     |           
| **disconnect/dc/leave/d**   |Disconnects the bot from the voice channel                           |            
| **pause/ps**                |Pauses the current song being played                                 |
| **resume/r**                |Resume the current song                                              | 
| **lyrics**                  |Gets the lyrics of the current playing song                          |  
| **remove/rem**              |Removes the song from the queue according to the position specified  | 
| **loop/l**                  |Loops the current song                                               |           
| **loop_off/lo**             |Turns off the loop                                                   |   
| **current/curr**            |Returns the name of the current song being played                    |           

## About

The project uses the following libraries:

* **[YoutubeDL](https://github.com/ytdl-org/youtube-dl)** package for fetching the music from youtube servers.
* **[FFMPEG](https://ffmpeg.org)** to encode and decode the stream.
* **[Discord.py](https://github.com/Rapptz/discord.py)** interacts with the discord client API.

## Installation

### Manual
* Install [FFMPEG](https://ffmpeg.org).
* Create a .env file to store these stuff
   - `TOKEN` is your discord bot token
   - `LYRICS_API_KEY` gives the API key to obtain the lyrics. 
   - `GCS_ENGINE_ID` used for lyrics. 

### ➔ Project setup
`Fork` the repository, this will make a copy of this project in your account.

1. Clone the repository  by running below command -
```
git clone https://github.com/<username>/Discord-Music-Bot.git
```

2. Open the folder by running below command -
```
cd Discord-Music-Bot
```

3.  Install all the requirements by running below command -
```
pip install -r requirements.txt
```
This will install all the required libraries to run this project.

4. Run python main.py to run this app.
```
python main.py
```
Note:- You must be on python version 3 or later.

