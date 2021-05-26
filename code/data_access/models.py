from dataclasses import dataclass
from datetime import datetime


@dataclass
class Job:
    id: int
    name: str
    interval_value: int
    interval_name: str
    is_running: bool
    last_executed: datetime = None
    last_outcome: str = None
    exception: str = None
    enabled: bool = False
