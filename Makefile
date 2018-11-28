PYTHON  := python3
PIP 	  := pip3
ANSIBLE := ansible-playbook

all: run

run:
	$(PYTHON) apolo/server.py

install:
	$(PIP) install -r requirements.txt

install-ansible:
	$(PIP) install ansible

ansible:
	cd provision/ansible/ && $(ANSIBLE) playbook.yml

connect-azure:
	ssh -i ~/SSH_APOLO/key pedroma@23.96.18.95
