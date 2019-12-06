#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'zappyk'
########################################################################################################################
import sys, time, re
import telepot
########################################################################################################################
def on_chat_message(msg):
    try:
        content_type, chat_type, chat_id = telepot.glance(msg)
        sendMessage = 'Ciao %s, sono un bot molto stupido!' % msg["from"]["first_name"]
        if content_type == 'text':
            sendMessage = "%s\n...ho ricevuto questo messaggio: \"%s\"" % (sendMessage, msg['text'])
            print('· %s say: %s' % (msg["from"]["first_name"], msg['text']))
        else:
            sendMessage = "%s\n...non so cosa fare con il tipo \"%s\"!\nSorry 😐😁" % (sendMessage, content_type)
        bot.sendMessage(chat_id, sendMessage)
    except:
        pass
#=======================================================================================================================
print('Init:')
#=======================================================================================================================
#
# Choose a name for bot = ASI_Affari_Su_Internet
# Choose a username bot = ZappykBot
# Will find bot at link = t.me/ZappykBot
#
# Use this token to access the HTTP API:
TOKEN = '908228321:AAEVInfeQzdJtmn2FoccfMD5U40E5BOlBRc'
# Keep your token secure and store it safely, it can be used by anyone to control your bot.
#
try:
    bot = telepot.Bot(TOKEN)
    bot.message_loop(on_chat_message)
    #
    print('Listening...')
    #
    while True:
        time.sleep(60)
    #
except KeyboardInterrupt:
    print('...exit...')
except Exception as e:
    print('...error detect: %s' % str(e))
#
#=======================================================================================================================
print('Done!')
########################################################################################################################
sys.exit()
'''
Cosa può fare questo bot?
BotFather is the one bot to rule them all. Use it to create new bot accounts and manage your existing bots.

About Telegram bots:
https://core.telegram.org/bots
Bot API manual:
https://core.telegram.org/bots/api

Contact @BotSupport if you have questions about the Bot API.

Carlo
/start

BotFather
I can help you create and manage Telegram bots. If you're new to the Bot API, please see the manual.

You can control me by sending these commands:

/newbot - create a new bot
/mybots - edit your bots [beta]

Edit Bots
/setname - change a bot's name
/setdescription - change bot description
/setabouttext - change bot about info
/setuserpic - change bot profile photo
/setcommands - change the list of commands
/deletebot - delete a bot

Bot Settings
/token - generate authorization token
/revoke - revoke bot access token
/setinline - toggle inline mode
/setinlinegeo - toggle inline location requests
/setinlinefeedback - change inline feedback settings
/setjoingroups - can your bot be added to groups?
/setprivacy - toggle privacy mode in groups

Games
/mygames - edit your games [beta]
/newgame - create a new game
/listgames - get a list of your games
/editgame - edit a game
/deletegame - delete an existing game

Carlo
/newbot

BotFather
Alright, a new bot. How are we going to call it? Please choose a name for your bot.

Carlo
ASI_Affari_Su_Internet

BotFather
Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.

Carlo
ZappykBot

BotFather
Done! Congratulations on your new bot. You will find it at t.me/ZappykBot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands. By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API:
908228321:AAEVInfeQzdJtmn2FoccfMD5U40E5BOlBRc
Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
'''