from backend.config import AppSettings, get_settings
from fastapi import APIRouter, Depends, HTTPException
import logging
from backend.dask.remote_api_dask import combine_files, get_data_from_api
from backend.schemas import schemas
from backend import dal
from backend.db.database import get_db, AsyncSession

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", status_code=201, response_model=schemas.APIDataSchema)
async def get_from_api(
    url: str,
    db: AsyncSession = Depends(get_db),
    settings: AppSettings = Depends(get_settings),
):

    try:
        result = await get_data_from_api(url, settings)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Cannot get data from API")

    try:
        csv_file = await dal.create_api_file(db, result)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Cannot save data from API")

    return csv_file


@router.post("/extend", status_code=201, response_model=schemas.CSVFileSchema)
async def extend_data(
    url: str,
    csv_id: int,
    csv_column: str | None,
    api_column: str | None,
    db: AsyncSession = Depends(get_db),
    settings: AppSettings = Depends(get_settings),
) -> schemas.CSVFileSchema:

    try:
        csv_file = await dal.get_csv_file(db, csv_id)
        api_file = await dal.get_api_file(db, url)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Cannot get data from DB")

    try:
        result = await combine_files(
            csv_file.file_src, api_file.file_src, csv_column, api_column, settings
        )
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Cannot join data 🧩🤷‍♂️")

    # save to db
    try:

        final_file = await dal.create_csv_file(db, result)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail="Cannot save to DB 🧙‍♀️")

    return final_file
