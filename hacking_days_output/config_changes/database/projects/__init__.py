from .FinanceCategory import FinanceCategory
from .FinanceModel import FinanceModel
from .FinanceTypeModel import FinanceTypeModel
from .MilestoneLinkModel import MilestoneLinkModel
from .MilestoneModel import MilestoneModel
from .ProjectCategoryModel import ProjectCategoryModel
from .ProjectTypeModel import ProjectTypeModel
from .ProjectModel import ProjectModel
from .StatementOfWorkModel import StatementOfWorkModel
from .BaseModel import BaseModel
import sqlalchemy

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine






async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker"""
    asyncEngine = create_async_engine(connectionstring)

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print("BaseModel.metadata.drop_all finished")
        if makeUp:
            try:
                await conn.run_sync(BaseModel.metadata.create_all)
                print("BaseModel.metadata.create_all finished")
            except sqlalchemy.exc.NoReferencedTableError as e:
                print("Caught NoReferencedTableError:", e)
                print("Unable automatically to create tables")
                return None
    
    if not makeUp:
        return None  # Ensure to return None when makeUp=False
    
    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker



def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
    Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database = os.environ.get("POSTGRES_DB", "data")
    # hostWithPort = os.environ.get("POSTGRES_HOST", "localhost:5432")
    hostWithPort = os.environ.get("POSTGRES_HOST", "host.docker.internal:5437")

    driver = "postgresql+asyncpg"  # "postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring