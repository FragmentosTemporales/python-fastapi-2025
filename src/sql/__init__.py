import pandas as pd
import datetime as dt
from rich import print
from sqlalchemy import create_engine, text
from ..config import config as c


class MyEngine():

    def __init__(self, servidor='DOMINION', esquema=''):
        """Iniciamos conexiones con el servidor"""

        self.servidor = servidor
        self.esquema=esquema
        self.inicio = dt.datetime.now(dt.UTC) - dt.timedelta(hours=4)

        if self.esquema=='':
            self.esquema= c.dominion_default_schema

        DOMINION_USER = c.dominion_user
        DOMINION_PASS = c.dominion_pass
        DOMINION_HOSTNAME = c.dominion_hostname

        connection_string = (
            f'mssql+pyodbc://{DOMINION_USER}:{DOMINION_PASS}@'
            f'{DOMINION_HOSTNAME}/{self.esquema}?driver=ODBC Driver 17 for SQL Server'
        )
        self.engine = create_engine(connection_string, pool_reset_on_return=None)

        print(f'[bold blue]Conectando al servidor {self.servidor} \n{self.engine}[/bold blue]')

    def execute(self, query):
        print(query)
        with self.engine.connect() as conn:
            conn.execute(text(query))
            conn.commit()
            return

    def query(self, query):
        return pd.read_sql_query(query, con=self.engine)
