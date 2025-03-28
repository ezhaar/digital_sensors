.PHONY: help
.DEFAULT_GOAL = help
VERSION ?= latest
APP_NAME ?= digital_sensors
GIT_COMMIT := $(shell git rev-parse HEAD)
VENV := $(shell echo $${VIRTUAL_ENV-.venv})
PYTHON := $(VENV)/bin/python3
RUFF := $(VENV)/bin/ruff
POETRY := $(VENV)/bin/poetry
SRC_DIR := $(CURDIR)/digital_sensors
TEST_DIR := $(SRC_DIR)/tests

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo "  init                   clean builds, envs and (re)initialize project"
	@echo "  lint                   check for PEP8 compliance"
	@echo "  format                 automatically format linting issues"
	@echo "  test                   run tests"
	@echo "  clean                  clean out previous build files"
	@echo "  build_docker           build docker container"

init: clean clean_venv create_venv install_req

create_venv:
	test -d $(VENV) || python3.12 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip setuptools wheel poetry

install_req:
	$(POETRY) install


lint:
	$(RUFF) check $(CURDIR)

format:
	$(RUFF) check --fix
	$(RUFF) format $(CURDIR)


clean_venv:
	rm -rf $(VENV)

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf junit
	rm -rf coverage*
	rm -rf .coverage
	rm -rf reports
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -rf {} +

build:
	$(POETRY) build

test:
	$(PYTHON) -m unittest discover


all: init lint format test
