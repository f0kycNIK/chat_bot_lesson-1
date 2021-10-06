# Programming vacancies compare
This program automatical sends out notifications in Telegram  about cheking 
work  with [devman.org](https://devman.org)

## How to install

For the program to work, you need to get a `DEVMAN_TOKEN` by registering on
[devman.org](https://devman.org) and get a `TELEGRAM_TOKEN` `TELEGRAM_CHAT_ID`
which is taken from the `.env` file.

```python
devman_token = os.getenv('DEVMAN_TOKEN')
telegram_token = os.getenv('TELEGRAM_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
```

The `.env` file is located in the root directory
```
├── .env
└── main.py
```

In the `.env` file, the keys are written as follows:

```python
DEVMAN_TOKEN=[]
TELEGRAM_TOKEN=[] 
TELEGRAM_CHAT_ID=[]
```
   
Python3 must already be installed. Then use pip (or pip3 if you have
conflict with Python3) to install dependencies:

```python
pip install -r requirements.txt
```

The program is started by the command:

```python
python main.py
```


## Project Goals
The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org).