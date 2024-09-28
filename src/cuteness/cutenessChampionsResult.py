from dataclasses import dataclass

from frozenlist import FrozenList

from .cutenessLeaderboardEntry import CutenessLeaderboardEntry


@dataclass(frozen = True)
class CutenessChampionsResult:
    champions: FrozenList[CutenessLeaderboardEntry] | None
    twitchChannel: str
    twitchChannelId: str
