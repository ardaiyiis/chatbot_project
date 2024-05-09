
from contextlib import contextmanager, AbstractContextManager
from typing import Callable
from core.logging.solomind_logger import SolomindLogger
from sqlalchemy import event, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Query, scoped_session, Session
 
Base = declarative_base()

class DatabaseOptions:
    def __init__(self,db_url:str, echo:bool = False) -> None:
        self.db_url = db_url
        self.echo = echo

class Database:
    def __init__(self, solomind_logger:SolomindLogger, options:DatabaseOptions ={}) -> None:
        self._engine = create_engine(options.db_url(), echo=options.echo())
        self.logger = solomind_logger.get_logger(__name__)
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
                expire_on_commit=False
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self) -> Callable[..., AbstractContextManager[Session]]:
        session: Session = self._session_factory()
        try:
            yield session
        except Exception as ex:
            self.logger.exception(f"Session rollback because of exception: {ex}")
            session.rollback()
            raise
        finally:
            session.close()

    # def __init__(self, db_url:str):
    #     DATABASE_URL = 'postgresql://root:Qwert12#@localhost:5432/Solomind'
    #     engine = create_engine(DATABASE_URL)
    #     self.make_session = sessionmaker(bind=engine)
    #     self.base = declarative_base()
    #     self.session = None

    # def connect(self):
    #     try:
    #         self.session = self.make_session()
    #         return self.session
    #     except Exception as e:
    #         # Handle the exception
    #         raise (f"Failed to create a database session: {str(e)}")

    # def close_connection(self):
    #     try:
    #         if self.session:
    #             self.session.close()
    #     except Exception as e:
    #         # Handle the exception
    #         raise (f"Failed to close the database session: {str(e)}")
        
    @event.listens_for(Query, "before_compile", retval=True)
    def no_deleted(query):
        for desc in query.column_descriptions:
            entity = desc['entity']
            if entity:
                query = query.limit(None).filter(entity.is_deleted == False)

        return query