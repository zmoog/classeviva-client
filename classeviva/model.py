from collections import namedtuple

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
