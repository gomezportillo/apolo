# REF. https://docs.microsoft.com/en-us/azure/cloud-shell/quickstart


echo "=== Generating SSH keys..."
ssh-keygen -t rsa -b 2048 -f ~/SSH_APOLO/key -q -N ""


echo "=== Creating resource group..."
az resource group create -location westeurope -name apolo_res_group


echo "==== Deploying virtual machine on Azure"
az_output = $(az vm create --resource-group apolo_res_group --name apolo_VM1 --image UbuntuLTS  --generate-ssh-keys)


echo "==== Obtaining publish IP address"
ip = $(echo $az_output | jq -r '.publicIpAddress')


echo "==== Uploading public key"
az vm user update --resource-group acopioM --name apolo_VM1 --user pedroma --ssh-key-value "$(cat ~/SSH_APOLO/key.pub)"


echo "==== Opening HTTP, HTTP & HTTPS ports"
az vm open-port --port 80 --resource-group apolo_res_group --name apolo_VM1
az vm open-port --port 443 --resource-group apolo_res_group --name apolo_VM1
az vm open-port --port 22 --resource-group apolo_res_group --name apolo_VM1


echo "=== Executing Ansible script"
ansible-playbook --inventory "$ip," --user pedroma playbook.yml
