from asyncio import subprocess
from turtle import update
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
import os
import asyncio

#########
# VARIABLES     
#########
load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
SCRIPT = '../../runners/textbroker.py'

############
# FUNCTIONS
############

async def run_script(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    print(f'[{cmd!r} exited with {proc.returncode}')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

def text_commands(update, context):
    update.message.reply_text('Let\'s wait for the data... BE PATIENT !!!!!')
    asyncio.run(run_script('python ' + SCRIPT))
    

def not_handled(update, context):
    update.message.reply_text('I DONT UNDERSTAND !!!!')

def start(update, context):
    update.message.reply_text("""
    BIENVENUE SUR MON SUPER BOT !!!
    ALLEZ ON VA BIEN RIGOLER
    """)

############
# COMMANDS
############
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('text_commands', text_commands))
    dp.add_handler(MessageHandler(Filters.text, not_handled))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
