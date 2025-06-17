from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


class PostgressDal:
    def __init__(self):
        self.engine = self._db_connect()
        print(f"Connected to {self.engine}")
        self.create_session()

    def _db_connect(self):
        connection_string = (
            "postgresql+psycopg2://postgres:yourStrongPassword@127.0.0.1:5432/localdb"
        )
        return create_engine(connection_string)

    def create_session(self):
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def db_query(self):
        with self.engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            print(result.fetchone())