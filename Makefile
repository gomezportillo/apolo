PYTHON  := python3
PIP 	  := pip3
ANSIBLE := ansible-playbook
PYTEST  := pytest

all: run

run:
	$(PYTHON) apolo/server.py

test:
	$(PYTEST) apolo/test/test_daouser.py
	$(PYTEST) apolo/test/test_server.py

install:
	$(PIP) install -r requirements.txt

install-ansible:
	sudo apt-get install software-properties-common
	sudo apt-add-repository --yes --update ppa:ansible/ansible
	sudo apt-get install ansible

install-azure:
	sudo apt-get install apt-transport-https lsb-release software-properties-common -y
	AZ_REPO=$(lsb_release -cs)
	echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" | sudo tee /etc/apt/sources.list.d/azure-cli.list
	sudo apt-key --keyring /etc/apt/trusted.gpg.d/Microsoft.gpg adv --keyserver packages.microsoft.com --recv-keys BC528686B50D79E339D3721CEB3E94ADBE1229CF
	sudo apt-get update
	sudo apt-get install azure-cli

install-milestone4-tools:
	sudo apt-get install jq httperf -y

ansible:
	cd provision/ansible/ && $(ANSIBLE) playbook.yml

connect-azure:
	echo "Outdated"
	# ssh -i ~/SSH_APOLO/key pedroma@23.96.18.95

.PHONY: acopio

acopio:
	cd acopio/ &&	chmod +x acopio.sh && bash acopio.sh

vagrant:
	cd orquestacion/ && vagrant up --provider=azure
