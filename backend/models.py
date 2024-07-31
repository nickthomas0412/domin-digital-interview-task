"""This file contains the model definition of the SQLAlchemy models and database connection."""

from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///sensor_data.db"
TABLE_NAME = "sensor_data"
DEBUG_ECHO = True

Base = declarative_base()


class SensorData(Base):
    """Class containing the columns of the sensorData table.

    Args:
        Base: Base sqlalchemy table type.
    """
    __tablename__ = TABLE_NAME
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.now())
    sensor_name = Column(String, nullable=False)
    sensor_type = Column(String, nullable=False)
    attributes = Column(JSON, nullable=False)


# Create engine, session and tables
engine = create_engine(DATABASE_URL, echo=DEBUG_ECHO)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
