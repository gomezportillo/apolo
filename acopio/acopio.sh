# REF. https://docs.microsoft.com/en-us/azure/cloud-shell/quickstart

read -p "Continue will delete all resources without prompting. Continue?(y/n) " -n 1 -r

if [[ $REPLY =~ ^[Yy]$ ]]
then

  RES_GROUP=apolo_resource_group
  NS_GROUP=apolo_network_security_group
  VM_NAME=apoloVM1
  VM_USER=pedroma
  LOCATION=northeurope

  echo -e "\n==== Deleting all VM previously created in resource group"
  az vm delete --ids $(az vm list --resource-group $RES_GROUP --query "[].id" -o tsv) --yes >/dev/null


  echo -e "=== Generating SSH keys"
  ssh-keygen -t rsa -b 2048 -f ~/SSH_APOLO/key -q -N "" -y


  echo -e "=== Creating resource group"
  az group create --location $LOCATION --name $RES_GROUP


  echo -e "==== Creating virtual machine on Azure"
  az_output=$(az vm create --resource-group $RES_GROUP --name $VM_NAME --image UbuntuLTS --size Standard_B1s)


  echo -e "==== Obtaining publish IP address"
  IP=$(echo $az_output | jq -r '.publicIpAddress')
  echo "$IP"


  echo -e "==== Uploading public key"
  az vm user update --resource-group $RES_GROUP --name $VM_NAME --user $VM_USER --ssh-key-value "$(cat ~/SSH_APOLO/key.pub)"


  echo -e "==== Creating network security group"
  az network nsg create --resource-group $RES_GROUP --name $NS_GROUP  >/dev/null


  echo -e "==== Defining rule for opening SSH port"
  az network nsg rule create --resource-group $RES_GROUP --nsg-name $NS_GROUP --name SSH_rule \
      --protocol tcp \
      --priority 320 \
      --destination-port-range 22 \
      --access allow  >/dev/null


  echo -e "==== Defining rule for opening HTTP port"
  az network nsg rule create --resource-group $RES_GROUP --nsg-name $NS_GROUP --name HTTP_rule \
      --protocol tcp \
      --priority 300 \
      --destination-port-range 80 \
      --access allow  >/dev/null


  echo -e "=== Executing Ansible script"
  ansible-playbook --inventory "$IP," --user $VM_USER playbook.yml


  read -p "Do you want to access using SSH to the created VM?(y/n) " -n 1 -r
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
    echo -e "Connecting, wait..."
    ssh -i ~/SSH_APOLO/key $VM_USER@$IP
  fi

else

  echo -e "\nOperation aborted. Exiting..."

fi
