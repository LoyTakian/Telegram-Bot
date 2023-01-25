# Telegram Bot

This is a simple Telegram Bot made for learning purposes. It main focus are the weebs from Telegram, as it's main features were made based on them.

## Features
- `/ai {message}` Using this command you can chat with chatGPT.\
For example: /ai Tell me a joke

- `/imagem {tags}` Using this command you can request an image from the site [yande.re](https://yande.re).\
For example: /imagem rem_(re_zero) feet\
***Remember to use valid tags and separate them by 'space'**

- `/nhentai {code}` Using this command you can get a formatted link of a gallery from [nhentai](https://nhentai.net).\
For example: /nhentai 192327

- `/fumo` Using this command you can request an image of a random fumo doll.
## Installation

***Make sure to have [pip](https://pip.pypa.io/en/stable/) and [venv](https://docs.python.org/3/library/venv.html) working**.

1. Clone this repository:
```bash
git clone $repo_link
```

2. Go to the repository folder:
```bash
cd $repo_name
```

3. Create a venv and install the dependencies:
```bash
python3 -m venv venv &&
source venv/bin/activate &&
pip install -r requirements.txt
```

4. Done !


## Usage

- Run the start.sh file by double-clicking it or using bash `sh start.sh`
- If it doesn't work, use python in a terminal window `python main.py`
### Pre requisites
- Have created a bot in [Telegram](https://t.me/botfather).
- Have created an account in [OPENAI](https://beta.openai.com)
- Have created a .env file based on the .env.example and configured your tokens from Telegram and Openai
