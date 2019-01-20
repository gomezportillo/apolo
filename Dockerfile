FROM python:3.6-alpine
MAINTAINER Pedro Manuel Gómez-Portillo López <gomezportillo@correo.ugr.es>

WORKDIR app/

COPY requirements-deploy.txt .
COPY apolo ./apolo

RUN pip install -r requirements-deploy.txt

EXPOSE 80

CMD ["python3", "apolo/server.py"]
