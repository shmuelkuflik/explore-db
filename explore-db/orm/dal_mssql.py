from sqlalchemy import create_engine, text
import urllib.parse

from sqlalchemy.orm import sessionmaker


class MssqlDal:
    def __init__(self):
        self.engine = self._db_connect()
        print(f"Connected to {self.engine}")
        self.create_session()

    def _db_connect(self):
        params = urllib.parse.quote_plus(
            "DRIVER=/opt/homebrew/lib/libmsodbcsql.17.dylib;"
            "SERVER=127.0.0.1,1433;"
            "DATABASE=master;"
            "UID=sa;"
            "PWD=YourStrong!Passw0rd;"
            "Connection Timeout=30;"
        )
        connection_string = f"mssql+pyodbc:///?odbc_connect={params}"

        return create_engine(connection_string)

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def db_query(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT @@VERSION"))
            print(result.fetchone())
