from dotenv import load_dotenv
import os

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    dir_descargas: str = f'{basedir}/download'

    dominion: str = os.getenv("DOMINION")
    dominion_user: str = os.getenv("DOMINION_USER")
    dominion_pass: str = os.getenv("DOMINION_PASS")
    dominion_hostname: str = os.getenv("DOMINION_HOSTNAME")
    dominion_default_schema: str = os.getenv("DOMINION_DEFAULT_SCHEMA", "dbo")

config = Config() 