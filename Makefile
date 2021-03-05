.PHONY: all
all: install example

.PHONY: install
install:
	pip3 install -r requirements.txt
	pip3 install -r requirements-dev.txt

.PHONY: bot
bot:
	python3 examples/ding-dong-bot.py

.PHONY: lint
lint:
	# stop the build if there are Python syntax errors or undefined names
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

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
