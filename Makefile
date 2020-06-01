.PHONY: all
all: install example

.PHONY: install
install:
	pip3 install -r requirements.txt

.PHONY: bot
bot:
	python3 examples/ding-dong-bot.py

.PHONY: test
test: pytest

.PHONY: pytest
pytest:
	python3 -m pytest

.PHONY: version
version:
	@newVersion=$$(awk -F. '{print $$1"."$$2"."$$3+1}' < VERSION) \
		&& echo $${newVersion} > VERSION \
		&& git add VERSION \
		&& git commit -m "$${newVersion}" > /dev/null \
		&& git tag "v$${newVersion}" \
		&& echo "Bumped version to $${newVersion}"
