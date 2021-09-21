import datetime

from pydantic import BaseModel
from models.location import Location
from typing import Optional


class ReportSubmittal(BaseModel):
    description: str
    location: Location
    created_date: Optional[datetime.datetime]


class Report(ReportSubmittal):
    id: str
    created_date: Optional[datetime.datetime]
