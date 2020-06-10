# -*- coding: utf-8 -*-

import os
import logging

from telegram.ext import Updater, MessageHandler, Filters
from config import *

import warnings
from telegram.vendor.ptb_urllib3.urllib3.exceptions import InsecureRequestWarning

warnings.simplefilter('ignore', InsecureRequestWarning)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

cwd = os.getcwd()


def check_site(site):
    bad_letters = list(" !@#$%^&*(){}[]+/|\\?,\"'")

    site_is_good = True

    if "." not in site:
        return False

    if site[:2] == "10" or site[:3] == "196" or site[:3] == "172":
        return False

    for letter in bad_letters:
        if letter in site:
            site_is_good = False
            break
    return site_is_good


def echo(update, context):
    site_is_good = check_site(update.message.text)
    if site_is_good:
        chat_id_str = str(update.message.chat_id)
        os.system("nmap -F {} 1> ./users_output/output_{}.txt 2> users_output/errors_{}.txt".format(update.message.text,
                                                                                                    chat_id_str,
                                                                                                    chat_id_str))
        text = "Output: \n\n"
        with open("./users_output/output_{}.txt".format(chat_id_str)) as file:
            text += file.read()
        text += "\n\nErrors: \n\n"
        with open("./users_output/errors_{}.txt".format(chat_id_str)) as file:
            user_errors = file.read()
            if len(user_errors) != 0:
                text += user_errors
            else:
                text += "<no errors>"
        update.message.reply_text(text)

        os.remove(cwd + "/users_output/output_{}.txt".format(chat_id_str))
        os.remove(cwd + "/users_output/errors_{}.txt".format(chat_id_str))
    else:
        update.message.reply_text('Send correct domain or IP')


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(token=TELEGRAM_TOKEN,
                      use_context=True,
                      request_kwargs=REQUEST_KWARGS
                      )
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    try:
        os.mkdir("users_output")
    except FileExistsError:
        pass

    main()
