# Azure reference doc. https://docs.microsoft.com/en-us/azure/cloud-shell/quickstart

RES_GROUP=apolo_resource_group
NS_GROUP=apolo_network_security_group
VM_BASENAME=apoloVM
VM_USER=pedroma
LOCATION=northeurope
SSH_KEY_LOCATOIN=~/SSH_APOLO/key

# echo -e "\n=================================================="
# echo -e "==== Welcome to the Azure Virtual Machine Generator  "
# echo -e "\n=================================================="

echo -e "\n"
echo -e "=========================================================================="
echo -e " \ \        / /   | |                                | |"
echo -e "  \ \  /\  / /___ | |  ___  ___   _ __ ___    ___    | |_  ___"
echo -e "   \ \/  \/ // _ \| | / __|/ _ \ | '_ ' _ \  / _ \   | __|/ _ \\"
echo -e "    \  /\  /|  __/| || (__| (_) || | | | | ||  __/   | |_| (_) |"
echo -e "     \/  \/  \___||_| \___|\___/ |_| |_| |_| \___|    \__|\___/"
echo -e "  _    _                                              __      __ __  __ "
echo -e " | |  | |               /\                            \ \    / /|  \/  |"
echo -e " | |_ | |__    ___     /  \    ____ _   _  _ __  ___   \ \  / / | \  / |"
echo -e " | __|| '_ \  / _ \   / /\ \  |_  /| | | || '__|/ _ \   \ \/ /  | |\/| |"
echo -e " | |_ | | | ||  __/  / ____ \  / / | |_| || |  |  __/    \  /   | |  | |"
echo -e "  \__||_| |_| \___| /_/    \_\/___| \__,_||_|   \___|     \/    |_|  |_|"
echo -e "   _____                                 _"
echo -e "  / ____|                               | |"
echo -e " | |  __   ___  _ __    ___  _ __  __ _ | |_  ___   _ __"
echo -e " | | |_ | / _ \| '_ \  / _ \| '__|/ _' || __|/ _ \ | '__|"
echo -e " | |__| ||  __/| | | ||  __/| |  | (_| || |_| (_) || |"
echo -e "  \_____| \___||_| |_| \___||_|   \__,_| \__|\___/ |_|"
echo -e "\n========================================================================="
echo -e "\n"

read -p "==== Do you want to download the Azure CLI? `echo $'\n(y/n)> '` " -n 1 -r


if [[ $REPLY =~ ^[Yy]$ ]]
then

  echo -e "\nInstalling the Azure Client Line Interface..."

  sudo apt-get install apt-transport-https lsb-release software-properties-common jq -y
  AZ_REPO=$(lsb_release -cs)
  echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" | sudo tee /etc/apt/sources.list.d/azure-cli.list
  sudo apt-key --keyring /etc/apt/trusted.gpg.d/Microsoft.gpg adv --keyserver packages.microsoft.com --recv-keys BC528686B50D79E339D3721CEB3E94ADBE1229CF
  sudo apt-get update
  sudo apt-get install azure-cli
  az login
fi

echo -e "" # New line
read -p "==== Is it the first time you execute this script? Azure groups and rules will be created`echo $'\n(y/n)> '` " -n 1 -r

if [[ $REPLY =~ ^[Yy]$ ]]
then

  echo -e "\nCreating resource group..."
  az group create --location $LOCATION --name $RES_GROUP


  echo -e "Creating network security group..."
  az network nsg create --resource-group $RES_GROUP --name $NS_GROUP  >/dev/null


  echo -e "Defining rule for opening SSH port..."
  az network nsg rule create --resource-group $RES_GROUP --nsg-name $NS_GROUP --name SSH_rule \
      --protocol tcp \
      --priority 320 \
      --destination-port-range 22 \
      --access allow >/dev/null


  echo -e "Defining rule for opening HTTP port..."
  az network nsg rule create --resource-group $RES_GROUP --nsg-name $NS_GROUP --name HTTP_rule \
      --protocol tcp \
      --priority 300 \
      --destination-port-range 80 \
      --access allow >/dev/null

else

  echo -e "" # New line
  read -p "==== Delete existing virtual machines, rules and SSH keys? `echo $'\n(y/n)> '` " -n 1 -r
  if [[ $REPLY =~ ^[Yy]$ ]]
  then

      echo -e "\nDeleting all VM previously created in resource group..."
      az vm delete --ids $(az vm list --resource-group $RES_GROUP --query "[].id" -o tsv) --yes >/dev/null


      echo -e "Deleting Network Security Group..."
      az network nsg delete --resource-group $RES_GROUP -n $NS_GROUP


      echo -e "Generating SSH keys..."
      ssh-keygen -t rsa -b 2048 -f $SSH_KEY_LOCATOIN -q -N "" -y

  fi

fi

echo -e "" # New line
read -p "==== How many virtual machines do you want to create? `echo $'\nEnter a number> '` " VM_NUMBER

if [[ $VM_NUMBER -gt 0 ]]
then

  echo -e "Creating $VM_NUMBER virtual machines..."

  for counter in $(seq 1 $VM_NUMBER)
  do

    VM_NAME=$VM_BASENAME$counter

    echo -e "Creating virtual machine $VM_NAME on Azure..."
    az_output=$(az vm create --resource-group $RES_GROUP --name $VM_NAME --nsg $NS_GROUP --image UbuntuLTS --size Standard_B1s)


    echo -e "Obtaining publish IP address..."
    IP=$(echo $az_output | jq -r '.publicIpAddress')
    echo "$IP"


    echo -e "Uploading public key to the VM..."
    az vm user update --resource-group $RES_GROUP --name $VM_NAME --user $VM_USER --ssh-key-value "$(cat $SSH_KEY_LOCATOIN.pub)"



    echo -e "Executing Ansible script..."
    ansible-playbook --inventory "$IP," --user $VM_USER playbook.yml


    read -p "==== Do you want to access using SSH to the $VM_NAME virtual machine? `echo $'\n(y/n)> '` " -n 1 -r
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
      echo -e "\nConnecting $VM_NAME, wait..."
      ssh -i $SSH_KEY_LOCATOIN $VM_USER@$IP
    fi

  done

else

  echo -e "0 selected. No VM will be created. Exiting..."

fi
