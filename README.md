# Proyecto de Cloud Computing

* [Página web del proyecto](https://gomezportillo.github.io/apolo/).
* [Aplicación desplegada en Heroku](https://apolo-cc.herokuapp.com/).

## Tabla de contenidos

<!-- TOC depthFrom:1 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Proyecto de Cloud Computing](#proyecto-de-cloud-computing)
	- [Tabla de contenidos](#tabla-de-contenidos)
- [Build status](#build-status)
- [Descripción del problema](#descripcin-del-problema)
- [Solución propuesta](#solucin-propuesta)
- [Definición del proyecto](#definicin-del-proyecto)
- [Arquitectura](#arquitectura)
	- [Comunicación de microservicios](#comunicacin-de-microservicios)
- [Planificación](#planificacin)
- [Despliegue](#despliegue)
	- [Despliegue en Travis-CI](#despliegue-en-travis-ci)
	- [Despliegue en Heroku](#despliegue-en-heroku)
- [Funcionalidad implementada hasta la fecha](#funcionalidad-implementada-hasta-la-fecha)
	- [Ejemplo de ejecución prático](#ejemplo-de-ejecucin-prtico)

<!-- /TOC -->

# Build status
[![Build Status](https://travis-ci.org/gomezportillo/apolo.svg?branch=master)](https://travis-ci.org/gomezportillo/apolo)



# Descripción del problema

Hoy en día cada vez es más común que las personas aprendan a tocar instrumentos y ensayen en bandas, pero es dificil encontrar personas con tu misma educación musical y gustos con los que poder quedar para ensayar.

# Solución propuesta

**Apolo** nace como una plataforma para poner en contacto a personas que busquen compañeros con intereses similares para compartir su afición a la música.

# Definición del proyecto

Este proyecto es el back-end un servicio que almacenará los datos de sus usuarios, como los instrumento que tocan, su nivel de educación musical, sus intereses musicales y la distancia que están dispuestos a recorrer para quedar con gente.

Para conseguir enviar infirmación, **Apolo** implementará una [API REST](https://bbvaopen4u.com/es/actualidad/api-rest-que-es-y-cuales-son-sus-ventajas-en-el-desarrollo-de-proyectos) propia, es decir, una API que utiliza verbos HTTP para comunicar al cliente y al servidor.

![API REST](assets/readme/api-rest.jpg)

Esta API REST trabajará sobre una base de datos no relacional [MongoDB](https://www.mongodb.com/es) que estará almacenada en el servicio de DBaaS [mLab](https://mlab.com).

# Arquitectura

**Apolo** está desarrollado en [Python3](https://www.python.org/) y el objetivo es que utilice una arquitectura basada en microservicios para facilitar su escalabilidad y aumentar su mantenibilidad.

* Un microservicio para registrar nuevos usuarios.
* Un microservicio para encontrar usuarios en la base de datos.
* Un microservicio para actualizar la información de los usuarios.
* Un microservicio para borrar a sus usuarios del sistema.

## Comunicación de microservicios

Lo principal en una arquitectura de microservicios es que se trata de unidades que se van a desplegar de forma independiente; diferentes servicios que trabajarán de forma totalmente independiente unos de otros.

Tras esta definición es fácil ver que surge la necesidad de comunicar unos microservicios con otros. Para conseguirlo se hará uso de un broker o cola de mensajería. Concretamente se usará [pika](https://pypi.org/project/pika/), la implementación en Python de [RabbitMQ](https://www.rabbitmq.com/).

# Planificación

* [x] [Hito 0](https://github.com/gomezportillo/apolo/milestone/4): Crear el repositorio del proyecto y hacer fork del repositorio de la asignatura.
* [x] [Hito 1](https://github.com/gomezportillo/apolo/milestone/1): Crear página web con la definición de la arquitectura.
* [x] [Hito 2](https://github.com/gomezportillo/apolo/milestone/2): Crear un microservicio y desplegarlo en Travis y Heroku automáticamente tras pasar los tests.
* [ ] [Hito 3](https://github.com/gomezportillo/apolo/milestone/3): Provisionamiento con Ansible.
* [ ] [Hito 4](https://github.com/gomezportillo/apolo/milestone/5): Orquestación
* [ ] [Hito 5](https://github.com/gomezportillo/apolo/milestone/6): Composición.

# Despliegue

## Despliegue en Travis-CI

El archivo de configuración de Travis-CI puede verse [aquí](.travis.yml) y los tests del DAO del usuario [aquí](apolo/test_daouser.py) y los de servior [aquí](apolo/test_server.py).

## Despliegue en Heroku

Aplicación desplegada en Heroku: [https://apolo-cc.herokuapp.com/](https://apolo-cc.herokuapp.com/).


# Funcionalidad implementada hasta la fecha

Actualmente atiende las siguientes peticiones HTTP con los parámetros {'email': $NOMBRE, 'instrument': $INSTRUMENT} y devuelve las respuestas en formato JSON. Además, ofrece un manejo de las excepciones 404 y 405  de HTTP e indica a través del código 200 que todo ha ido correctamente.

* **PUT** en _/users_ guarda en la base de datos el usuario especificado en parámetros.
* **POST** en _/users_ actualiza el usuario indicado.
* **GET** en _/users_ obtiene el usuario indicado.
* **DELETE** en _/users_ borra el usuario indicado.
* **GET** en _/readAll_ devuelve todos los usuario del sistema.
* **DELETE** en _/deleteAll_ elimina todos los usuarios del sistema.

Esto puede verse más claramente en los [test al servidor](apolo/test_server.py) o en el [propio servidor](apolo/server.py).

## Ejemplo de ejecución prático

La orden HTTP,

      PUT/ {'email':'jhon@doe', 'insturment', 'guitar'} en https://apolo-cc.herokuapp.com/users

Devolverá la cadena JSON,

      {'status': 'SUCCESS', 'message': 'On inserting usser with email jhon@doe'}

siempre y cuando dicho email no exista previamente, ya que es la clave primaria o _index_ en MongoDB. En ese caso devolvería,

      {'status': 'EMAIL_ALREADY_EXISTS', 'message': 'On inserting usser with email jhon@doe'}
