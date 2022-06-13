from datetime import datetime
import json
import logging
import os
from typing import List, cast
from fastapi import APIRouter, File, HTTPException, Response, UploadFile
from backend.db.database import get_db, AsyncSession
from fastapi import Depends
import pandas as pd
from io import BytesIO
from fastapi.responses import JSONResponse

from backend.dal import create_csv_file, get_csv_file, get_leatest_csv_files

from backend.schemas.schemas import (
    CSVFileSchema,
    CSVFileSchemaIn,
    CSVFileSchemaSimplified,
)

from backend.config import AppSettings, get_settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=List[CSVFileSchemaSimplified])
async def list_files(db: AsyncSession = Depends(get_db)):
    try:
        result = await get_leatest_csv_files(db)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal server error")
    return result


@router.get("/{id}", status_code=200)
async def get_file(
    id: int,
    settings: AppSettings = Depends(get_settings),
    db: AsyncSession = Depends(get_db),
):

    try:
        csv_file = await get_csv_file(db, id)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=404, detail="File not found")

    try:
        df = pd.read_parquet(os.path.join(settings.shared_storage_url, csv_file.file_src))  # type: ignore
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=500,
            detail="Somethings went wrong 😫 We cannot process this file",
        )

    json_response = json.loads( df.to_json(orient="table") )
    response = {
        **json_response,
        **csv_file.dict()
    }
    return response


@router.post("/", status_code=201, response_model=CSVFileSchema)
async def upload_file(
    db: AsyncSession = Depends(get_db),
    settings: AppSettings = Depends(get_settings),
    file: UploadFile = File(...),
):

    file_src = os.path.join(
        datetime.now().strftime("%Y_%m_%d"),
        file.filename,
    )
    try:
        file_dir = os.path.join(
            settings.shared_storage_url, datetime.now().strftime("%Y_%m_%d")
        )
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        contents = await file.read()
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, "There was an error uploading the file")
    finally:
        await file.close()

    try:
        df = pd.read_csv(BytesIO(contents))
        columns: List[str] = cast(List[str], df.columns.tolist())  # type: ignore
        df.to_parquet(os.path.join(settings.shared_storage_url, file_src))  # type: ignore
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, "There was an error reading the file")

    try:
        csv_file = CSVFileSchemaIn(
            file_name=file.filename,
            file_src=file_src,
            file_size=len(contents),
            columns=columns,
        )
        csv_file = await create_csv_file(db, csv_file)
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, "There was an error processing your request!")

    return csv_file
