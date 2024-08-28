FROM python:3.7-slim
WORKDIR .
RUN apt-get update && apt-get install -y
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 4400
CMD ['uvicorn','main:app','--reload']