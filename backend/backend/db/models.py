from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy.dialects import postgresql

Base = declarative_base()


class BaseModel(Base):  # type: ignore
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)


class CSVFileModel(BaseModel):
    __tablename__ = "csv_file"
    file_name = Column(String)
    file_src = Column(String)
    file_size = Column(Integer)
    columns = Column(postgresql.ARRAY(String, dimensions=1))


class APIDataModel(BaseModel):
    __tablename__ = "api_data"
    url = Column(String)
    columns = Column(postgresql.ARRAY(String, dimensions=1))
    file_src = Column(String)
    file_size = Column(Integer)
