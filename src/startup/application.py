from fastapi import FastAPI
from startup.container import Container
from core.middlewares import ResponseWrapper
from fastapi.middleware.cors import CORSMiddleware

class SolomindeApi:
    @staticmethod
    def create_app():
        container = Container()
        db=container.db()
        db.create_database()
        solomind_logger = container.logger()
        solomind_logger.create_logger()
        
        app = FastAPI(title="Solomind AI Api")
        app.container = container
        app.add_middleware(
            CORSMiddleware,
            allow_origins=container.config.cors.allowed_origins(),
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        app.add_middleware(ResponseWrapper)
        logger = solomind_logger.get_logger(__name__)
        app.logger = logger.info(f"{app.title} application is starting...")
        return app