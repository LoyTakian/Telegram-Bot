import os
import requests
import json
import random
import time

import telebot
import openai

API_TOKEN_TELEGRAM = os.environ['API_TOKEN_TELEGRAM']
API_TOKEN_OPENAI = os.environ['API_TOKEN_OPENAI']
API_TOKEN_IMAGES = os.environ['API_TOKEN_IMAGES']

bot = telebot.TeleBot(API_TOKEN_TELEGRAM)
openai.api_key = API_TOKEN_OPENAI


@bot.message_handler(commands=["help", "start"])
def send_welcome(message):
    sender_username = message.from_user.username
    print(
        "===================================================\n",
        "====| send_message_ai |====\n",
        f"==| Message Sender: {sender_username} |==\n",
        f"==| Message content: {message.text} |==\n",
        f"==| Message answer: [PADRÃO] |==",
    )
    bot.reply_to(
        message,
        """Olá! Eu sou a Rem. \n
Pau no cu da Emilia e do Subaru, agora eu sou a esposa do Loy.\n
Meus atuais comandos são:\n
    /ai 'mensagem'
    [Para conversar com uma AI]
    Ex: /ai quem inventou a teoria da relatividade?

    /imagem 'tag'
    [Para retornar uma imagem com as tags mencionadas]
    ***utilize tags válidas do yande.re separadas por um espaço**
    Ex: /imagem rem_(re_zero) feet
    """,
    )


@bot.message_handler(commands=["ai"])
def send_message_ai(message):
    sender_username = message.from_user.username
    question = message.text[4:]
    response = openai.Completion.create(
        engine="text-davinci-002", prompt=question, max_tokens=1024
    )
    answer = response["choices"][0]["text"]

    print(
        "===================================================\n",
        "====| send_message_ai |====\n",
        f"==| Message Sender: {sender_username} |==\n",
        f"==| Message content: {message.text} |==\n",
        f"==| Message answer: {answer} |==",
    )
    bot.reply_to(message, answer)


@bot.message_handler(commands=["imagem"])
def send_message_imagem(message):
    sender_username = message.from_user.username
    tag_list = "+".join(message.text[8:].split(" "))
    response = requests.get(f"{API_TOKEN_IMAGES}{tag_list}")

    print(
        "===================================================\n",
        "====| send_message_imagem |====\n",
        f"==| Message Sender: {sender_username} |==\n",
        f"==| Message Content: {message.text} |==",
    )
    if response.status_code == 200:
        if len(response.content) != None:
            image_list = json.loads(response.content)
            if image_list:
                random_image = random.choice(image_list)
                random_image = random_image.get("file_url")

                print(f"==| Message Answer: {random_image} |==")
                bot.reply_to(message, f"{random_image}")

            else:
                print(f"==| Message Answer: {response.content} |==")
                bot.reply_to(
                    message,
                    "Não encontrei nenhuma imagem com as tags que você escolheu.",
                )
    else:
        print(
            "==| SOMETHING WENT WRONG |==\n",
            response.__dict__,
            "\n==============================",
        )
        bot.reply_to(message, "O culto da bruxa me impediu de conseguir uma imagem :c")


@bot.message_handler(func=lambda message: True)
def send_message(message):
    sender_username = message.from_user.username
    print(
        "===================================================\n",
        "====| send_message |====\n",
        f"==| Message Sender: {sender_username} |==\n",
        f"==| Message content: {message.text} |==\n",
        f"==| Message answer: {message.text} |==",
    )
    if message.text.lower() == "loyola":
        bot.reply_to(message, "Loyola vose")

    else:

        bot.reply_to(message, message.text)


bot.infinity_polling()
