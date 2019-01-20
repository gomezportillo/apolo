PYTHON  := python3
PIP 	  := pip3
ANSIBLE := ansible-playbook
PYTEST  := pytest

DOCKERNAME=pedroma1/apolo:1.0


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


install-docker:
	sudo apt-get remove docker docker-engine docker.io containerd runc
	sudo apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common -y
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
	sudo apt-get update
	sudo apt-get install docker-ce


install-milestone4-tools:
	sudo apt-get install jq httperf -y


install-heroku:
	sudo snap install --classic heroku


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


build-docker:
	docker build --tag=pedroma1/apolo:1.0 .
	docker image ls


run-docker-local:
		docker run -it -p 80:80 $DOCKERNAME


run-docker-local-bg:
	docker run -d -p 80:80 $DOCKERNAME


run-docker-repository:
	sudo apt-get install docker.io
	docker pull $DOCKERNAME
	sudo service docker start
	sudo docker run $DOCKERNAME


push-image-dockerhub:
	docker push $DOCKERNAME


push-container-heroku:
	heroku container:push web --app apolo-docker
	heroku container:release web --app apolo-docker
