PYTHON := python3
PIP 	 := pip3

all: run

run:
	$(PYTHON) apolo/server.py

install:
	$(PIP) install -r requirements.txt
