from sqlalchemy import create_engine, text
import urllib.parse

class MssqlDal:
    def __init__(self):
        self.engine = self._db_connect()
        print(f"Connected to {self.engine}")

    def _db_connect(self):
        params = urllib.parse.quote_plus(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=127.0.0.1,1433;"
            "DATABASE=master;"
            "UID=sa;"
            "PWD=YourStrong!Passw0rd;"
            "Connection Timeout=30;"
        )
        connection_string = f"mssql+pyodbc:///?odbc_connect={params}"

        return create_engine(connection_string)

    def db_query(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT @@VERSION"))
            print(result.fetchone())
