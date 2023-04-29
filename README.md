# If I Were a (discord) Bot

**This is a work in progress.** Current objective is to have a all-in-one administration bot connected to a databse and an application for administration and data visualisation purpose.
Techs are: 
- Python for the bot.
- React.JS for the app.
- Couchbase for the database.

## Getting Started 

create your .env file
```
cp .env.sample .env
```
Fill up or change information as you need. You must also have a [discord bot token](https://discordpy.readthedocs.io/en/stable/discord.html). Once you have your token, fill up `BOT_TOKEN=` in the .env file.

If you don't change `COUCHBASE_DATA_PATH`, then:
```
mkdir volumes/db/data
```
Install docker and docker compose and build the application:
```
docker compose build
```
Launch the application
```
docker compose up
```

For now, dockerfiles are only configured for development.

## TODO 
### Bot
- Hot Reloading of Python and/or discord.py cogs 
- XP distribution and xp curve for messaging and vocal time
- Clear message function
- Connection to Database
### App
- XP visualisation
- Connection to Database
- Oauth2 with discord (by default, only member should be able to see the website)
### DB
- Automatic setup