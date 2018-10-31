---
layout: page
title: Acerca de
permalink: /about/
---

Esta sección contiene información técnica acerca del proyecto **Apolo**.

## Breve descripción del proyecto

Plataforma para encontrar compañeros con los que tocar música.

## Definición del proyecto

Cada vez es más común que la gente aprenda a tocar instrumentos y toque en bandas. Por eso, **Apolo** nace como una plataforma para poner en contacto a personas que busquen compareños para compartir su afición a la música.

Los usuarios de **Apolo** se registrarán facilitando datos como intrumento que tocan, nivel de educación musical, intereses musicales y distancia que están dispuestos a recorrer para quedar con gente, y podrán buscar otras personas según estos mismos parámetros.

Además, los usuarios podrán programar alertas para ser notificado cuando un nuevo usuario correspondiente a sus necesidades se registre.


## Arquitectura

Apolo está desarrollado en [Python3](https://www.python.org/) y utiliza una arquitectura basada en microservicios para facilitar su escalabilidad y aumentar su mantenibilidad.

* Un microservicio para registrar nuevos usuarios.
* Un microservicio para atender las búsquedas de los usuarios.
* Un miocroservicio para gestionar las alertas que los usuarios creen.

Además, se plantea la posibilidad de crear nuevos microservicios según avance el proyecto que atiendan nuevas necesidades.

# Despliegue

Este proyecto se desplegará en [Heroku](https://www.heroku.com) y [Azure](https://azure.microsoft.com).

## Licencia

Este proyecto y todos sus archivos se comparten bajo la [MIT License](https://github.com/gomezportillo/apolo/blob/master/LICENSE)

****

Puede que a lo largo del desarrollo del proyecto las características de **Apolo** cambien.
