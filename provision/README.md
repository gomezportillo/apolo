# Provisionamiento con Ansible

[Ansible](https://www.ansible.com/) es un sistema que permite el provisionamiento de máquinas remotas fácilmente. La imagen inferior muestra un croquis de cómo funciona.

![Ansible](img/ansible.jpg)

Para poder completar este hito se han seguido los siguientes pasos.

## Testing

El usuario [xenahort](https://github.com/xenahort) ha comprobado el provisionamiento en una máquina virtual del proyecto [Apolo](https://github.com/gomezportillo/apolo). Para ello se han seguido los pasos indicados [aquí](https://github.com/gomezportillo/apolo/blob/master/provision/README.md) con la única modificación de los datos referentes a la máquina virtual como usuario y dirección ip.

![Provisionamiento](https://github.com/xenahort/proyectoCloudComputing/blob/master/img/apolo2.png)
![Prueba](https://github.com/xenahort/proyectoCloudComputing/blob/master/img/apolo1.png)


## Tabla de contenidos

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Provisionamiento con Ansible](#provisionamiento-con-ansible)
	- [Testing][#testing]
	- [Tabla de contenidos](#tabla-de-contenidos)
	- [Configuración de la máquina de Azure](#configuracin-de-la-mquina-de-azure)
	- [Provisionamiento de la máquina de Azure](#provisionamiento-de-la-mquina-de-azure)
	- [Despliegue de Apolo](#despliegue-de-apolo)
	- [Proyecto en ejecución en la máquina Azure](#proyecto-en-ejecucin-en-la-mquina-azure)

<!-- /TOC -->

## Configuración de la máquina de Azure

Lo primero fue seleccioanr el sistema operativo que correría en la máquina de Azure. A la vista de los resultados del [siguiente artículo](https://www.premper.com/por-que-usamos-servidores-ubuntu), y siendo un sistema que ya conocía, elegí usar **Ubuntu Server 18.04 LTS**, o por su nombre en clave, **Bionic Beaver**. Es importante que sea una LTS ya que necesitamos soporto a largo plazo.

Una vez decidido el sistema operativo, se eligió la máquina más barata de Azure (6,59€/mes) y creó con los siguientes parámetros.

* **Nombre**: bionic
* **Region**: Europa
* **S.O**: Ubuntu Server 18.04 LTS
* **Nombre de usuario**: pedroma
* **IP**: Estática
* **Puertos de entrada**: HTTP, HTTPS, RDR, SSH

Para el tipo de autentificación se eligió **SSH**, así que tras crear un par pública/privada de claves (`key.pub` y `key`, respectivamente) con el comando `ssh-keygen` y almacenarlas en la máquina local en `~/SSH_APOLO`, se indicó la clave pública en Azure a la hora de configurar la máquina.

Una vez configurada y creada podemos obtener su IP, que en este caso ha sido `23.96.18.95`. Ahora, acceder a ella en cualquier momento es tan fácil como ejecutar en local,

```
ssh -i ~/SSH_APOLO/key pedroma@23.96.18.95
```

con el siguiente resutado.

![SSH output](img/ssh_output.jpg)

## Provisionamiento de la máquina de Azure

Para instalar Ansible con pip basta ejecutar `pip3 install ansible` en local.

Para instalar automáticamente los programas necesarios en la máquina de Azure con Ansible se han escrito tres archivos, `ansible_hosts`, `ansible.cfg` y `playbook.yml`. Se usa el comando `apt` para instalar los paquetes, por lo que estos scripts deberían funcionar en cualquier sistema que soporte dicho comando.

* `ansible_hosts` indica la dirección, el puerto y la clave privada que usaremos para acceder a las máquinas remotas. Si quisiéramos provisionar más máquinas bastaría con indicarlas en la sección `[azure]`, aunque todas deban compartir el mismo usuario y clave pública.

```
[azure]
bionic ansible_ssh_port=22 ansible_ssh_host=23.96.18.95

[azure:vars]
ansible_ssh_user=pedroma
ansible_ssh_private_key_file=~/SSH_APOLO/key
```

* `ansible.cfg` sirve para configurar Ansible indicándole dónde estará el fichero de hosts así como que no compruebe la clave del host.

```
[defaults]
host_key_checking = False
inventory = ./ansible_hosts
```

* Por último, en `playbook.yml` indicamos a Ansible los pasos que tiene que seguir, en este caso comprobar que git, python3 y pip3 existen (y si no crearlos), clonar el repositorio en `~/apolo` y ejecutar pip3 sobre el archivo `requirements.txt` que se encuentra en su raíz.

```yml
---
- hosts: all
  become: yes
  vars:
    project_path: ~/apolo
  tasks:
    - name: Updating repositories
      apt: update_cache=yes

    - name: Installing git
      apt: name=git state=present

    - name: Installing python3
      apt: name=python3 state=present

    - name: Installing pip3
      apt: name=python3-pip state=present

    - name: Cloning Apolo repository
      git:
        repo: https://github.com/gomezportillo/apolo
        dest: "{{ project_path }}"

    - name: Installing Python dependecies
      shell: "pip3 install -r {{ project_path }}/requirements.txt"
```

Tras situarnos en esta carpeta y ejecutar `ansible-playbook playbook.yml` en local el resultado de la consola es el siguiente.

![SSH output](img/ansible_output.jpg)

Con ésto, la máquina de Azure quedaría provisionada.

## Despliegue de Apolo

Inicialmente se intentó incluir el despliegue de Apolo en la máquina de Azure con Ansible, pero cuando Ansible termina de ejecutarse borra todos los archivos que haya creado, incluyendo el reposotiro descargado. Esto se intentó evitar ejecutando `export ANSIBLE_KEEP_REMOTE_FILES=1` en la máquina remota como indicaban algunos hilos deforos como [Stackoverflow](https://stackoverflow.com/questions/30060164/save-temporary-ansible-shell-scripts-instead-of-deleting), pero sin resultado.

Los comandos para clonar el resositorio se dejaron en Ansible, ya que necesita el repositorio para poder  ejecutar pip3, pero finalmente se ha hecho el despliegue del proyecto en Azure de forma manual con la ejecución de los siguientes comandos en la máquina local.

```bash
ssh -i ~/SSH_APOLO/key pedroma@23.96.18.95
git clone https://github.com/gomezportillo/apolo
cd apolo
python3 apolo/server.py&
exit
```

De este modo el proceso de Apolo quedaría ejecutándose indefinidamente. Para pararlo podríamos o bien reiniciar la máquina desde el portal de Azure o ejecutar lo siguiente en local,

```bash
ssh -i ~/SSH_APOLO/key pedroma@23.96.18.95
top | grep python3 #para obtener el PID del proceso
^C # para parar top
kill $(PID)
exit
```

## Proyecto en ejecución en la máquina Azure

Para comprobar que el proyecto está en ejecución, basta con acceder a http://23.96.18.95 y comprobar que el resultado es parecido a la imagen inferior.

![Proyecto en Azure](img/project_on_azure.jpg)
