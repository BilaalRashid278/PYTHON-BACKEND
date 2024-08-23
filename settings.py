from starlette.config import Config
from starlette.datastructures import Secret


try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DEBUG = config('DEBUG',cast=bool,default=False)
DATABASE_URL = config("DATABASE_URL",cast=Secret)