# Proyecto de Cloud Computing

[Página web del proyecto](https://gomezportillo.github.io/apolo/).

## Build status
[![Build Status](https://travis-ci.org/gomezportillo/apolo.svg?branch=master)](https://travis-ci.org/gomezportillo/apolo)

## Descripción del problema

Hoy en día cada vez es más común que las personas aprendan a tocar instrumentos y ensayen en bandas, pero es dificil encontrar personas con tu misma educación musical y gustos con los que poder quedar para ensayar.

## Solución propuesta

**Apolo** nace como una plataforma para poner en contacto a personas que busquen compañeros con intereses similares para compartir su afición a la música.

## Definición del proyecto

Este proyecto es el back-end un servicio que almacenará los datos de sus usuarios, como los instrumento que tocan, su nivel de educación musical, sus intereses musicales y la distancia que están dispuestos a recorrer para quedar con gente.

Para conseguir enviar infirmación, **Apolo** usará una [API REST](https://bbvaopen4u.com/es/actualidad/api-rest-que-es-y-cuales-son-sus-ventajas-en-el-desarrollo-de-proyectos), es decir, una API que utiliza verbos HTTP para comunicar al cliente y al servidor.

![API REST](assets/readme/api-rest.jpg)

Esta API REST trabajará sobre una base de datos no relacional [MongoDB](https://www.mongodb.com/es) que estará almacenada en el servicio [mongoLab](https://mlab.com).

## Arquitectura

Apolo está desarrollado en [Python3](https://www.python.org/) y utiliza una arquitectura basada en microservicios para facilitar su escalabilidad y aumentar su mantenibilidad.

* Un microservicio para registrar nuevos usuarios.
* Un microservicio para comprobar que un usuario existe.
* Un microservicio para atender las búsquedas de los usuarios.
* Un microservicio para borrar un usuario de la base de datos.

### Comunicación

Para comunicar estos microservicios se hará uso de un broker o cola de mensajería. Concretamente se usará [pika](https://pypi.org/project/pika/), la implementación en Python de [RabbitMQ](https://www.rabbitmq.com/).

## Planificación

* [x] [Hito 0](https://github.com/gomezportillo/apolo/milestone/4): Crear el repositorio del proyecto y hacer fork del repositorio de la asignatura
* [x] [Hito 1](https://github.com/gomezportillo/apolo/milestone/1): Crear página web con la definición de la arquitectura
* [x] [Hito 2](https://github.com/gomezportillo/apolo/milestone/2): Crear un microservicio y desplegarlo en Heroku
* [ ] [Hito 3](https://github.com/gomezportillo/apolo/milestone/3): Provisionamiento con Ansible
* [ ] [Hito 4](https://github.com/gomezportillo/apolo/milestone/5): Orquestación
* [ ] [Hito 5](https://github.com/gomezportillo/apolo/milestone/6): Composición

## Despliegue

Aplicación desplegada en Heroku: [https://apolo-cc.herokuapp.com/](https://apolo-cc.herokuapp.com/).
