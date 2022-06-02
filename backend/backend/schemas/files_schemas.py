from pydantic import BaseModel


class CSVFile(BaseModel):
    file_name: str
