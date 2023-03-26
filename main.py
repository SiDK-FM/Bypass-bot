import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import bypasser
import os
import ddl
import requests
import threading
from texts import HELP_TEXT
from ddl import ddllist
import re


# bot
bot_token = os.environ.get("TOKEN", "")
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  


# handle ineex
def handleIndex(ele,message,msg):
    result = bypasser.scrapeIndex(ele)
    try: app.delete_messages(message.chat.id, msg.id)
    except: pass
    for page in result: app.send_message(message.chat.id, page, reply_to_message_id=message.id, disable_web_page_preview=True)


# loop thread
def loopthread(message):

    urls = []
    for ele in message.text.split():
        if "http://" in ele or "https://" in ele:
            urls.append(ele)
    if len(urls) == 0: return

    if bypasser.ispresent(ddllist,urls[0]):
        msg = app.send_message(message.chat.id, "⚡ __generating...\n\nᴊᴏɪɴ ғᴏʀ ᴍᴏʀᴇ ʙᴏᴛs :- @MensBotZ__", reply_to_message_id=message.id)
    else:
        if urls[0] in "https://olamovies" or urls[0] in "https://psa.pm/":
            msg = app.send_message(message.chat.id, "🔎 __ᴛʜɪs ᴍɪɢʜᴛ ᴛᴀᴋᴇ sᴏᴍᴇ ᴛɪᴍᴇ...__", reply_to_message_id=message.id)
        else:
            msg = app.send_message(message.chat.id, "🔎 __ʙʏᴘᴀssɪɴɢ...__", reply_to_message_id=message.id)

    link = ""
    for ele in urls:
        if re.search(r"https?:\/\/(?:[\w.-]+)?\.\w+\/\d+:", ele):
            handleIndex(ele,message,msg)
            return
        elif bypasser.ispresent(ddllist,ele):
            try: temp = ddl.direct_link_generator(ele)
            except Exception as e: temp = "**Error**: " + str(e)
        else:    
            try: temp = bypasser.shortners(ele)
            except Exception as e: temp = "**Error**: " + str(e)
        print("ʙʏᴘᴀssᴇᴅ:",temp)
        link = link + temp + "\n\n"
        
    try: app.edit_message_text(message.chat.id, msg.id, f"__ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴅᴇsᴛɪɴᴀᴛɪᴏɴ ʟɪɴᴋ \n\n__{link}__\n\n©️ᴅᴇᴠ :- @MensBotZ", disable_web_page_preview=True)
    except:
        try: app.edit_message_text(message.chat.id, msg.id, "__Failed to Bypass__")
        except:
            try: app.delete_messages(message.chat.id, msg.id)
            except: pass
            app.send_message(message.chat.id, "__Failed to Bypass__")


# start command
@app.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, f"__👋 ʜɪ **{message.from_user.mention}**, ɪ ᴀᴍ ʟɪɴᴋ ʙʏᴘᴀssᴇʀ ʙᴏᴛ, ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴀɴʏ sᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋs ᴀɴᴅ ɪ ᴡɪʟʟ ʏᴏᴜ ɢᴇᴛ ʏᴏᴜ ᴏʀɪɢɪɴᴀʟ ʟɪɴᴋ.\nᴄʜᴇᴄᴋᴏᴜᴛ /help ᴛᴏ ʀᴇᴀᴅ ᴍᴏʀᴇ\n\nᴀɴʏ ɪssᴜᴇ sᴏ ᴄᴏɴᴛᴀᴄᴛ ʜᴇʀᴇ\n©️ᴅᴇᴠ :- @Fm_Onr 🕊",
    reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("📯υρ∂αтє ¢нαηηєℓ 🦋 ", url="https://t.me/MensBotZ")]]), reply_to_message_id=message.id)


# help command
@app.on_message(filters.command(["help"])
def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message)
    app.send_message(message.chat.id, HELP_TEXT, reply_to_message_id=message.id, disable_web_page_preview=True)


# links
@app.on_message(filters.text)
def receive(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bypass = threading.Thread(target=lambda:loopthread(message),daemon=True)
    bypass.start()


# doc thread
def docthread(message):
    if message.document.file_name.endswith("dlc"):
        msg = app.send_message(message.chat.id, "🔍 __bypassing\n\nᴊᴏɪɴ ғᴏʀ ᴍᴏʀᴇ ᴀᴍᴀᴢɪɴɢ ʙᴏᴛs :- @MensBotZ...__", reply_to_message_id=message.id)
        print("sent DLC file")
        sess = requests.session()
        file = app.download_media(message)
        dlccont = open(file,"r").read()
        link = bypasser.getlinks(dlccont,sess)
        app.edit_message_text(message.chat.id, msg.id, f' ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴅᴇsᴛɪɴᴀᴛɪᴏɴ ʟɪɴᴋ 🔗\n\n__{link}__\n\©️ᴅᴇᴠ :- @Fm_Onr')
        os.remove(file)


# doc
@app.on_message(filters.document)
def docfile(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bypass = threading.Thread(target=lambda:docthread(message),daemon=True)
    bypass.start()


# server loop
print("Bot Starting")
app.run()
