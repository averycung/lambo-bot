from dotenv import load_dotenv  # For guarding API token
from bot.db import *
import os
import telebot    # Telegram API
import base58     # For decrypting Solana CA
import mysql.connector 
from telebot import types 

# Retrieve API token
load_dotenv()  
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

#---Helper Methods

# Determine whether a string is a valid CA or not
def isValidCA(address):
    try:
        decoded = base58.b58decode(address) # Decode CA
        return len(decoded) == 32 # Valid if 32 bytes
    except Exception:
        return False

# Return CA in a given message block
def findCA(msg):
    x = msg.text
    words = x.split()
    for word in words:
        word = word.strip()
        if isValidCA(word): 
            return word
    return False

#---Bot Filters

# Create custom validCA filter to filter for valid CAs in chat messages
class IsValidCA(telebot.custom_filters.SimpleCustomFilter):
    key ='is_CA'
    @staticmethod
    def check(message:telebot.types.Message):
        x = message.text
        words = x.split()
        for word in words:
            word = word.strip()
            if isValidCA(word):
                return True
        return False
        
# Add bot filter
bot.add_custom_filter(IsValidCA())

#---Message Handlers

# START COMMAND
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "*I\\'m Lambo\\.* If you are new to Lambo, please see /instructions\n \nIf you want to shill your referral links in chat, I\\'m your guy\\.  \n \nYou can control me by"\
                 " sending these commands: \n \n*Codes:* \n/setcode \\- set your referral link\n/viewcode \\- view your code\n/deletecode \\- delete your code", parse_mode="MarkdownV2")
    
# HELP COMMAND
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "*Commands:* \n/instructions \n/setcode \n/viewcode \n/deletecode", parse_mode="MarkdownV2")

# INSTRUCTIONS COMMAND
@bot.message_handler(commands=['instructions'])
def instructions(message):
    bot.reply_to(message, "*Instructions:* \n*1\\.* Set your referral codes with */setcode*\\. Your referral code will be stored in my database"\
                 " \n\n*2\\.* Use the */claim* command in a groupchat you would like your referrals to be shilled in\\. Once you claim a group chat, "\
                 "I will respond to every CA posted in that group chat with your referral links\\. *note* you must be an admin to use */claim* in a chat"\
                 "\n\n*3\\.* Update, view or delete your links with */setcode* , */viewcode* , or */deletecode*", parse_mode="MarkdownV2")

# SET CODE COMMAND
user_codes = {}  
@bot.message_handler(commands=['setcode'])
def set_link(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("BullX")
    btn2 = types.KeyboardButton("Axiom")
    markup.add(btn1, btn2)

    msg = bot.reply_to(
        message,
        "Which platform would you like to set a code for?\n\nChoose an option:",
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, paste_ref_code)

def paste_ref_code(message):
    if message.text.lower() == "bullx":
        msg1 = bot.reply_to(message, "Please paste your BullX referral code")
        bot.register_next_step_handler(msg1, save_ref_code_bull)
    elif message.text.lower() == "axiom":
        msg2 = bot.reply_to(message, "Please paste your Axiom referral code")
        bot.register_next_step_handler(msg2, save_ref_code_axiom)

def save_ref_code_bull(message):
    code = message.text
    add_bull(message.from_user.id, code)
    add_username_usercodes(message.from_user.id, message.from_user.username)
    bot.reply_to(message, "Your code has been updated!")

def save_ref_code_axiom(message):
    code = message.text
    add_axiom(message.from_user.id, code) 
    add_username_usercodes(message.from_user.id, message.from_user.username)
    bot.reply_to(message, "Your code has been updated!")

# VIEW CODE COMMAND
@bot.message_handler(commands=['viewcode'])
def view_link(message):
    id = message.from_user.id
    result = view(id)
    if result:
        bull, axiom = result
        reply = f"🐂 *BullX:* `{bull}`\n🧪 *Axiom:* `{axiom}`"
    else:
        reply = "❌ You haven't set a referral code yet. Use /setcode to get started."
    
    bot.reply_to(message, reply, parse_mode="MarkdownV2")

# DELETE CODE COMMAND
@bot.message_handler(commands=['deletecode'])
def del_code(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("BullX")
    btn2 = types.KeyboardButton("Axiom")
    markup.add(btn1, btn2)

    msg = bot.reply_to(
        message,
        "Which code would you like to delete?\n\nChoose an option:",
        reply_markup=markup
    )
    bot.register_next_step_handler(msg, delete)


def delete(message):
    id = message.from_user.id
    if message.text.lower() == "bullx":
        delcode(id, "bull_ref_code")
        bot.reply_to(message, "Your BullX code has been deleted.")
    elif message.text.lower() == "axiom":
        delcode(id, "axiom_ref_code")
        bot.reply_to(message, "Your Axiom code has been deleted.")

# CLAIM CHAT COMMAND
@bot.message_handler(commands=['claim'])
def claim(message):
    id = message.from_user.id
    chatid = message.chat.id 
    admin_ids = [admin.user.id for admin in bot.get_chat_administrators(chatid)]

    if id in admin_ids:
        claim_chat(chatid, id)
        add_username_chatowners(message.from_user.id, message.from_user.username)
        bot.reply_to(message, "You have become the master of this chat!")
    else:
        bot.reply_to(message, "You are not an admin")

#---Main
# MAIN MESSAGE HANDLER FOR CA
@bot.message_handler(is_CA=True)
def caMsg(message):
    chat_id = message.chat.id
    owner_id = find_owner(chat_id)
    ca = findCA(message)

    if view(owner_id)[0] != None:
        # Build the bullx referral link
        startString = "https://neo.bullx.io/terminal?chainId=1399811149&address="
        endString = "&r" + find_bull(chat_id) + "=en"
        bull_link = f"{startString}{ca}{endString}"
        escaped_bull_link = bull_link.replace("-", "\\-").replace("_", "\\_").replace(".", "\\.").replace(":", "\\:").replace("?", "\\?").replace("=", "\\=").replace("&", "\\&")

    if view(owner_id)[1] != None:
        # Build the Axiom referral link 
        a_startString = "https://axiom.trade/t/"
        a_endString = "/" + find_ax(chat_id)
        axiom_link = f"{a_startString}{ca}{a_endString}"
        escaped_axiom_link = axiom_link.replace("-", "\\-").replace("_", "\\_").replace(".", "\\.").replace(":", "\\:").replace("?", "\\?").replace("=", "\\=").replace("&", "\\&")
    
    if view(owner_id)[0] != None and view(owner_id)[1] != None:
        bot.reply_to(
            message,
            f"Here's the token you're looking for: \n \n 🏎*[BullX]({escaped_bull_link})*  \\|  *[Axiom]({escaped_axiom_link})*🏎\n\n`{ca}`",
            parse_mode="MarkdownV2"
        )

    elif view(owner_id)[0] != None and view(owner_id)[1] == None:
        bot.reply_to(
            message,
            f"Here's the token you're looking for: \n \n 🏎*[BullX]({escaped_bull_link})*🏎\n\n`{ca}`",
            parse_mode="MarkdownV2"
        )

    elif view(owner_id)[0] == None and view(owner_id)[1] != None:
        bot.reply_to(
            message,
            f"Here's the token you're looking for: \n \n 🏎*[Axiom]({escaped_axiom_link})*🏎\n\n`{ca}`",
            parse_mode="MarkdownV2"
        )


bot.infinity_polling()
