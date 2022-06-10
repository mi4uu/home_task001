from typing import List
from backend.db.database import AsyncSession
from backend.db import models
from backend.schemas import schemas
from sqlalchemy import select


async def create_csv_file(
    db: AsyncSession, csv_file: schemas.CSVFileSchemaIn
) -> schemas.CSVFileSchema:

    db_user = models.CSVFileModel(**csv_file.dict())
    db.add(db_user)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    await db.refresh(db_user)
    return schemas.CSVFileSchema(**db_user.__dict__)


async def get_csv_file(db: AsyncSession, csv_file_id: int) -> schemas.CSVFileSchema:
    stmt = select(models.CSVFileModel).where(models.CSVFileModel.id == csv_file_id)
    results = await db.execute(stmt)
    result = results.scalars().first()

    csv_file = schemas.CSVFileSchema(**result.__dict__)
    return csv_file


async def get_leatest_csv_files(
    db: AsyncSession, limit: int = 50
) -> List[schemas.CSVFileSchema]:
    stmt = (
        select(models.CSVFileModel).order_by(models.CSVFileModel.id.desc()).limit(limit)
    )
    results = await db.execute(stmt)
    results = results.scalars().all()

    csv_files = [schemas.CSVFileSchema(**result.__dict__) for result in results]
    return csv_files


async def create_api_file(
    db: AsyncSession, api_file: schemas.APIDataSchemaIn
) -> schemas.APIDataSchema:

    db_user = models.APIDataModel(
        **api_file.dict(),
    )
    db.add(db_user)

    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

    await db.refresh(db_user)
    return schemas.APIDataSchema(**db_user.__dict__)


async def get_api_file(db: AsyncSession, url: str) -> schemas.APIDataSchema:
    stmt = (
        select(models.APIDataModel)
        .where(models.APIDataModel.url == url)
        .order_by(models.APIDataModel.id.desc())
    )
    results = await db.execute(stmt)
    result = results.scalars().first()

    api_file = schemas.APIDataSchema(**result.__dict__)
    return api_file
