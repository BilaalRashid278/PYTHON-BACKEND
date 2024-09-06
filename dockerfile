FROM python:3.12
RUN pip install --upgrade pip
WORKDIR .
RUN  python -m venv .venv
# COPY requirements.txt .
RUN pip install uvicorn fastapi sqlmodel psycopg2 passlib[bcrypt]
COPY . .
EXPOSE 4400
CMD ['uvicorn','main:app','--reload']