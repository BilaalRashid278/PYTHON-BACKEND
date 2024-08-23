FROM python:latest
WORKDIR .
COPY . .
RUN apt-get update && apt-get install -y
RUN pip --version
RUN pip install uvicorn fastapi sqlmodel
ENTRYPOINT ['uvicorn','main:app','--reload']