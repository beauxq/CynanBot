from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class TwitchChannelEditor:
    createdAt: datetime
    userId: str
    userName: str
