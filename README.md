# PuntoBot
My degenerate discord bot! Features may include:
- e621 search
    - And e926 search (you know, as a bonus)
- rule34 search
- zorn and ship generators (wowza!)
- Error reporting features
- Extremely over-the-top use of extensions and Cogs
    - THERE ISN'T EVEN A COMMAND TO RELOAD THEM, THERE IS NO POINT!!!!!! LMAO!!!
- Deploys to heroku
    - (so I can scav off of their free dyno)

### Dependencies
Requires Python 3.7 minimum (i think? thats the requirement for discord.py 2.0.)
Required modules are all in `requirements.txt`, so you can install everything you need with
```sh
pip3 install -r requirements.txt
```
These modules are:
- **Discord.py 2.0** - Discord bot API
- **python-dotenv** - Used to allow bot token storage in both environment variables (for Heroku) and in a file (for local development)
- **rule34** - Search for posts on rule34
- **requests** - Make requests to the e621 api
- **pokebase** - Make requests to PokeAPI, for the pokesmash or pass game