import os
import pytz
import time
import json
import openai
import random
import telebot
import logging
import requests
import urllib.request
from datetime import datetime
from dotenv import load_dotenv


# ===| Variables Setup |===
load_dotenv()

TOKEN_TELEGRAM = os.getenv("TOKEN_TELEGRAM")
TOKEN_OPENAI = os.getenv("TOKEN_OPENAI")
URL_IMAGES = os.getenv("URL_IMAGES")
URL_FUMOS = os.getenv("URL_FUMOS")


# =========================


bot = telebot.TeleBot(TOKEN_TELEGRAM)
openai.api_key = TOKEN_OPENAI


# ===| Log Setup |===
logging.basicConfig(level=logging.INFO, filename="log.txt")


def send_to_log(message, answer):
    tz = pytz.timezone("America/Sao_Paulo")
    brazil_time_now = datetime.now(tz)

    user = getattr(message, "from_user", None)

    data = {
        "data_time": f'{brazil_time_now.strftime("%d-%m-%Y %H:%M:%S")}',
        "user_info": {
            "id": getattr(user, "id", None),
            "username": getattr(user, "username", None),
            "first_name": getattr(user, "first_name", None),
            "last_name": getattr(user, "last_name", None),
        },
        "message_info": {"received": getattr(message, "text", None), "sent": answer},
    }

    data_json = json.dumps(data)
    print("New entry: ", data_json)
    logging.info(data_json)


# ====================

# ===| Functions Setup |===
@bot.message_handler(commands=["help", "start"])
def send_message_welcome(message):

    answer = "Olá! Eu sou a Rem.\nPau no cu da Emilia e do Subaru, agora eu sou a esposa do Loy!\nMeus atuais comandos são:\n  /ai 'mensagem'\n  [Para conversar com uma AI]\n  Ex: /ai quem inventou a teoria da relatividade?\n\n  /imagem 'tag'\n  [Para retornar uma imagem com as tags mencionadas]\n  Ex: /imagem rem_(re_zero) feet\n  *Utilize tags válidas do yande.re, separadas por um espaço\n\n  /nhentai 'código'\n  [Para retornar um link do nhentai contendo o código enviado]\n  Ex: /nhentai 192327\n\n /fumo\n [Para retornar a imagem de uma boneca fumo aleatória!]\n Ex: /fumo"
    send_to_log(message, answer)
    bot.reply_to(message, answer)


@bot.message_handler(commands=["ai"])
def send_message_ai(message):
    question = message.text[4:]

    if len(question) > 0:
        try:
            answer = openai.Completion.create(
                engine="text-davinci-002", prompt=question, max_tokens=1024
            )["choices"][0]["text"]
        except:
            answer = "Minha cota do chatGPT acabou. O comando está temporariamente desabilitado."
    else:
        answer = "Você precisa digitar algo após o '/ai'"

    send_to_log(message, answer)
    bot.reply_to(message, answer)


tries = 0


@bot.message_handler(commands=["imagem"])
def send_message_image(message):
    global tries
    tag_list = "+".join(message.text[8:].split(" "))
    response = requests.get(f"{URL_IMAGES}{tag_list}")

    if response.status_code != 200:
        send_to_log(message, f"{response}")
        bot.reply_to(message, f"{response}")
        return

    else:

        data = json.loads(response.content)
        if not data:
            answer = "O culto da bruxa me impediu de conseguir uma imagem :c"
            send_to_log(message, answer)
            bot.reply_to(message, answer)
        else:
            try:
                answer = random.choice(data).get("file_url")
                send_to_log(message, answer)
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=answer,
                    reply_to_message_id=message.message_id,
                )
                tries = 0
            except:
                if tries >= 5:
                    answer = (
                        f"Tentei conseguir uma imagem {tries} vezes mas não consegui."
                    )
                    send_to_log(message, answer)
                    bot.reply_to(message, answer)
                else:
                    tries = tries + 1
                    send_message_image(message)


@bot.message_handler(commands=["nhentai"])
def send_message_nhentai(message):
    magical_numbers = message.text[9:]

    if magical_numbers.isdigit():
        answer = f"https://nhentai.net/g/{magical_numbers}/"
    else:
        answer = "O Subaru me disse que esse código não existe!"

    send_to_log(message, answer)
    bot.reply_to(message, answer)


@bot.message_handler(commands=["fumo"])
def send_fumo(message):
    global tries
    response = requests.get(f"{URL_FUMOS}/random")

    if response.status_code != 200:
        send_to_log(message, f"{response}")
        bot.reply_to(
            message, "A url foi destruída por uma das Grandes Bestas da bruxa!"
        )
        return

    else:

        data = json.loads(response.content)
        if not data:
            answer = "O culto da bruxa me impediu de conseguir uma imagem :c"
            send_to_log(message, answer)
            bot.reply_to(message, answer)
        else:
            try:
                answer = data.get("URL")
                send_to_log(message, answer)
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=answer,
                    reply_to_message_id=message.message_id,
                )
                tries = 0
            except:
                if tries >= 5:
                    answer = (
                        f"Tentei conseguir uma imagem {tries} vezes mas não consegui."
                    )
                    send_to_log(message, answer)
                    bot.reply_to(message, answer)
                else:
                    tries = tries + 1
                    send_fumo(message)


@bot.message_handler(commands=["teste"])
def send_test(message):
    bot.reply_to(message, "Estou no meu momento íntimo com o Loy, cai fora.")


# ===========================


# ===| Run Bot |===
print("Bom dia, Loy!")
bot.infinity_polling()


# =================
