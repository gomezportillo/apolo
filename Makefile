PYTHON  := python3
PIP 	  := pip3
ANSIBLE := ansible-playbook
PYTEST  := pytest

all: run

run:
	$(PYTHON) apolo/server.py

test:
	$(PYTEST) apolo/test_daouser.py
	$(PYTEST) apolo/test_server.py

install:
	$(PIP) install -r requirements.txt

install-ansible:
	$(PIP) install ansible

ansible:
	cd provision/ansible/ && $(ANSIBLE) playbook.yml

connect-azure:
	ssh -i ~/SSH_APOLO/key pedroma@23.96.18.95
