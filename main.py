from lib.bot import bot
from webserver import keep_alive

VERSION = "0.3.2"
UPDATE = """
Added New Features! Help menu updated! (Check out @NaCl helpembed) 
Will replace the regular help command in the future!
"""


keep_alive()
bot.run(VERSION, UPDATE)
