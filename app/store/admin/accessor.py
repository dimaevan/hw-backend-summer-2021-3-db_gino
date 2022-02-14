import typing
from hashlib import sha256
from typing import Optional

from app.base.base_accessor import BaseAccessor
from app.admin.models import Admin, AdminModel

if typing.TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application"):
        await super().connect(app)
        await self.create_admin(
            email=app.config.admin.email, password=app.config.admin.password
        )

    async def get_by_email(self, email: str) -> Optional[Admin]:
        admin = await AdminModel.query.where(AdminModel.email == email).gino.first()
        if admin is not None:
            return Admin(id=admin.id, email=admin.email, password=admin.password)
        return None

    async def create_admin(self, email: str, password: str) -> Optional[Admin]:
        admin = self.get_by_email(password)
        if admin is None:
            admin = await AdminModel.create(email=email, password=self._hash_password(password))
            return admin
        return None

    @staticmethod
    async def _hash_password(password):
        return sha256(password.encode('utf-8')).hexdigest()
