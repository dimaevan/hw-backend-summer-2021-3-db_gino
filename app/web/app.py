from typing import Optional

from aiohttp.web import (
    Application as AiohttpApplication,
    View as AiohttpView,
    Request as AiohttpRequest,
)
from aiohttp_apispec import setup_aiohttp_apispec
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage

from app.admin.models import Admin
from app.store import setup_store, Store
from app.store.database.database import Database
from app.web.config import Config, setup_config
from app.web.logger import setup_logging
from app.web.middlewares import setup_middlewares
from app.web.routes import setup_routes
from dotenv import load_dotenv


class Application(AiohttpApplication):
    config: Optional[Config] = None
    store: Optional[Store] = None
    database: Optional[Database] = None


class Request(AiohttpRequest):
    admin: Optional[Admin] = None

    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})


app = Application()


def setup_app(config_path: str) -> Application:
    load_dotenv()
    setup_logging(app)
    setup_config(app, config_path)
    session_setup(app, EncryptedCookieStorage(app.config.session.key))
    setup_routes(app)
    setup_aiohttp_apispec(
        app, title="Vk Quiz Bot", url="/docs/json", swagger_path="/docs"
    )
    setup_middlewares(app)
    setup_store(app)
    return app
