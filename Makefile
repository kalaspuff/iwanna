.SILENT:

PACKAGENAME := $(shell poetry version | awk {'print $$1'})

THIS_FILE := $(lastword $(MAKEFILE_LIST))

define shell-functions
: BEGIN
runcmd() {
	_cmd=$@;

	script_cmd="script -q /dev/null ${_cmd[@]} >&1";
	script -q /dev/null -c echo 2> /dev/null > /dev/null && script_cmd="script -q /dev/null -c \"${_cmd[@]}\" >&1";

	printf "\e[90;1m[\e[90;1mmake: \e[0;90;1mcmd\e[0;90;1m]\e[0m \e[0;93;1m➔ \e[97;1m$_cmd\e[0m\n" \
		&& ( \
			cmd_output=$(eval "$script_cmd" | tee /dev/tty; exit ${PIPESTATUS[0]}); cmd_exit_code=$?; \
			[ -z "$cmd_output" ] || ([ -z "$(tr -d '[:space:]' <<< $cmd_output)" ] && printf "\e[1A"); \
			[[ "$cmd_exit_code" -eq 0 ]] || return $cmd_exit_code \
		) \
		&& printf "\e[032;1m[✔︎] success\e[0m\n\n" \
			|| (_test_exit=$? \
				&& printf "\e[031;1m[✖︎] fail (exit code: $_test_exit)\e[0m\n\n" \
				&& return $_test_exit) \
			&& [ $? -eq 0 ] \
				|| return $?
}
: END
endef

$(shell sed -n '/^: BEGIN/,/^: END/p' $(THIS_FILE) > .make.functions.sh)
SHELL := /bin/bash --init-file .make.functions.sh -i

default:
	printf """\e[37musage:\e[0m\n \
		  \e[90m$$ \e[0;97;1mmake \e[0;92;1mrun           \e[0;90m➔ \e[32;3mrun \e[0m\n \
		  \e[90m$$ \e[0;97;1mmake \e[0;92;1minstall       \e[0;90m➔ \e[32;3minstall dependencies locally (requires poetry) \e[0m\n \
		  \e[90m$$ \e[0;97;1mmake \e[0;92;1mtest          \e[0;90m➔ \e[32;3mrun test cases locally (requires poetry) \e[0m\n \
		  \e[90m$$ \e[0;97;1mmake \e[0;92;1mlint          \e[0;90m➔ \e[32;3mlint code locally (requires poetry) \e[0m\n \
	""" | sed -e 's/^[ \t	]\{1,\}\(.\)/  \1/'

.PHONY: run-app
run-app:
	@runcmd python -m iwanna.app

.PHONY: poetry-install
poetry-install:
	@runcmd poetry install

.PHONY: poetry-pytest
poetry-pytest:
	@runcmd poetry run pytest tests/

.PHONY: poetry-flake8
poetry-flake8:
	@runcmd poetry run flake8

.PHONY: poetry-mypy
poetry-mypy:
	@runcmd poetry run mypy

.PHONY: release
release: poetry-install poetry-pytest poetry-flake8 poetry-mypy
	poetry version `python ${PACKAGENAME}/__version__.py`
	rm -rf dist/
	poetry build
	twine upload dist/${PACKAGENAME}-`python ${PACKAGENAME}/__version__.py`*
	git add pyproject.toml ${PACKAGENAME}/__version__.py
	git commit -m "Bumped version" --allow-empty
	git tag -a `python ${PACKAGENAME}/__version__.py` -m `python ${PACKAGENAME}/__version__.py`
	git push
	git push --tags

run: run-app
start: run
go: run
up: run

test: poetry-pytest
tests: test
pytest: poetry-pytest

lint: poetry-flake8 poetry-mypy
linting: lint
linter: lint
flake8: poetry-flake8
mypy: poetry-mypy

install: poetry-install
