# Contenedores

![Logo de docker](img/docker-logo.png)

El Proyecto Docker ofrece una plataforma completa de código abierto para construir, enviar y ejecutar cualquier aplicación, en cualquier lugar, utilizando contenedores. ([Referencia](https://hoplasoftware.com/por-que-elegir-docker-ee-frente-a-ce/))

A diferencia de las máquinas virtuales, un contenedor se ejecuta de forma nativa en Linux y comparte su kernel con otros contenedores. Además, no ocupa más memoria que cualquier otro ejecutable, lo que lo hace muy liviano.

![Docker vs VM](img/docker-vs-vm.png)[Referencia](https://docs.docker.com/get-started/)

Actualmente, Docker tiene dos versiones,

* **CE**, o *Community Edition*, que incluye la funcionalidad de Docker orientada a personas. Es la que nosotros usaremos.
* **EE**, o *Enterprise Edition*, que incluye una serie de características adicionales orientadas a compañías más grandes.

## Instalar Docker

Para instalar Docker en el entorno de desarrollo local se han seguido los pasos indicados en su [página oficial](https://docs.docker.com/install/linux/docker-ce/ubuntu/) y en el [tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04) de DigitalOcean.

```
sudo apt-get install apt-transport-https ca-certificates curl gnupg2 software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce
```

Podemos comprobar que Docker ha sido instalado correctamente y el daemon se ha inizializado podemos

* Ejecutar `sudo systemctl status docker` para comprobar que el servicio está activo.
* Descargar y ejecutar un proyecto de prueba con `sudo docker run hello-world`. Docker, al no encontrar el proyecto localmente, se conectará a los repositorios oficiales, descargará la imagen, creará el contenedor y lo ejecutará, informándonos de que todo ha ido correctamente.

## Iniciar sesión

Para iniciar sesión en Docker, primero deberemos registrarnos en [DockerHub](https://hub.docker.com/). Tras crear un usuario y una contraseña, ejecutamos `docker login` e introducimos los datos para conectarnos a nuestra cuenta.

## Dockerfile
