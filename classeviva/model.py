from collections import namedtuple
from datetime import date, datetime
from typing import List

from pydantic.dataclasses import dataclass

Grade = namedtuple(
    "Grade", ["value", "display_value", "subject", "date", "color", "comment"]
)


@dataclass
class Entry:
    id: int
    code: str
    author: str
    notes: str
    starts_at: str
    ends_at: str
    subject: str = None


@dataclass
class Notice:
    id: int
    published_at: datetime
    valid_from: date
    valid_to: date
    title: str
    attachments: List[str]
