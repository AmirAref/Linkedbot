from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from config import *
from Linkedin import Linkedin
import re

# configuration
app = Client("linkedbot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, proxy=proxy)


# check validition url
def validition_url(url):
    check = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    #out
    if check.match(url):
        return True
    else:
        return False


# message handler
# get only text messages from private chats
@app.on_message(filters.text & filters.private)
async def message_handler(client : Client, message : Message):
    # progrss message
    msg = await message.reply("Processing ...", reply_to_message_id=message.id) 
    # check the url pattern
    text = message.text
    if not validition_url(text):
        return await msg.edit("Invalid Url !")
    
    # get the video links of video
    try:
        linkedin = Linkedin(text)
        links = linkedin.get_post_data()
    except Exception as e:
        print(e)
        return await msg.edit("an error occurred !")
    # create inline url keyboard
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton(f'link {indx+1}', url=link)] for indx, link in enumerate(links)]
    )
    # make hyperlinks
    links = [f'[link {indx+1}]({link})' for indx, link in enumerate(links)]
    # output
    await msg.edit(", ".join(links), reply_markup=keyboard)


if __name__ == "__main__":
    # setup the bot
    app.run()