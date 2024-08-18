from core import database
from models import models_service
import asyncio


async def main():
    async for db in database.get_db():
        await models_service.ParamType.create_all(db, [{"cd": 1, "descr": "input"}, {"cd": 2, "descr": "output"}])
        await models_service.ParamLoc.create_all(db, [{"cd": 1, "descr": "header"}, {"cd": 2, "descr": "body"}, {"cd": 3, "descr": "query"}, {"cd": 4, "descr": "xml namespace"}])
        await models_service.Currency.create_all(db, [{"id": 1, "name": "EGP", "code": "EGP", "rate": 1}, {"id": 2, "name": "USD", "code": "USD", "rate": 50}])
        await db.commit()
        print("Initial data created")


if __name__=="__main__":
    asyncio.run(main())
