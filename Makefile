.PHONY: all
all: install example

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: bot
bot:
	python examples/ding-dong-bot.py
