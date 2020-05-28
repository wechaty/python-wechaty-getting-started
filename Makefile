.PHONY: all
all: install example

.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: bot
bot:
	python3 examples/ding-dong-bot.py
