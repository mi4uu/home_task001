from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class CSVFileSchemaIn(BaseModel):
    file_name: str
    file_src: str
    file_size: int
    columns: List[str]


class CSVFileSchema(CSVFileSchemaIn):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class CSVFileSchemaSimplified(BaseModel):
    file_name: str
    file_src: str
    file_size: int
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class APIDataSchemaIn(BaseModel):
    url: str
    file_src: str
    file_size: int
    columns: List[str]


class APIDataSchema(APIDataSchemaIn):
    url: str
    file_src: str
    file_size: int
    columns: List[str]
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class DataFromAPI(BaseModel):
    path: str
    columns: List[str]
    size: Optional[int] = None
