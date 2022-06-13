# type: ignore
from backend.config import AppSettings
import dask.dataframe as dd

import os
import hashlib
from uuid import uuid1
import randomname
from .dask_setup import get_dask_client
from backend.schemas import schemas
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


async def get_data_from_api(url: str, settings: AppSettings) -> schemas.APIDataSchemaIn:

    with get_dask_client() as client:

        def read_data(url: str) -> schemas.APIDataSchemaIn:

            df = dd.read_json(url, orient="series")

            url_md5 = hashlib.md5(url.encode("utf-8")).hexdigest()
            file_name = f'{url_md5}'
            file_src = os.path.join(
                datetime.now().strftime("%Y_%m_%d"),
                file_name,
            )
            df.to_parquet(os.path.join(settings.shared_storage_url, file_src))

            return schemas.APIDataSchemaIn(
                url=url,
                file_src=file_src,
                file_size=df.memory_usage(deep=True).sum().compute(),
                columns=df.columns.tolist(),
            )

        task = client.submit(read_data, url)
        result = await task.result()
        return result


def combine_parquets(
    shared_path: str, src0: str, src1: str, join_by0: str | None, join_by1: str | None
) -> schemas.CSVFileSchemaIn:
    src0 = os.path.join(shared_path, src0)
    src1 = os.path.join(shared_path, src1)

    df0 = dd.read_parquet(src0)
    df1 = dd.read_parquet(src1)

    output_file_name = os.path.join(datetime.now().strftime("%Y_%m_%d"), uuid1().hex)
    outout_path = os.path.join(shared_path, output_file_name)

    if join_by0 is None:
        join_by0 = df0.columns[0]
    if join_by1 is None:
        join_by1 = df1.columns[0]

    result = df0.merge(df1, left_on=[join_by0], right_on=[join_by1], how="left")

    result.to_parquet(outout_path)

    csv_file = schemas.CSVFileSchemaIn(
        file_name=randomname.get_name(),
        file_src=output_file_name,
        file_size=result.memory_usage(deep=True).sum().compute(),
        columns=result.columns.tolist(),
    )

    return csv_file


async def combine_files(
    src0: str,
    src1: str,
    join_by0: str | None,
    join_by1: str | None,
    settings: AppSettings,
) -> schemas.CSVFileSchema:
    with get_dask_client() as client:
        task = client.submit(
            combine_parquets,
            settings.shared_storage_url,
            src0,
            src1,
            join_by0,
            join_by1,
        )
        result = await task.result()

        return result
