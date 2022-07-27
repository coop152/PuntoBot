# PuntoBot
A discord bot for odd people. Features include:
- e621/e926 image search
- r34 search
- character ship generator
- Probably over-the-top use of extensions and Cogs
- Deploys to heroku

### Dependencies
Requires Python 3.7 minimum (This is the minimum requirement of discord.py 2.0).

Required modules are:
- **Discord.py 2.0** - Discord bot API
- **python-dotenv** - Used to allow bot token storage in both environment variables (for Heroku) and in a file (for local development)
- **rule34** - Search for posts on rule34
- **requests** - Make requests to the e621 api and pokeAPI

A `requirements.txt` file is included, so you can install everything with
```sh
pip3 install -r requirements.txt
```