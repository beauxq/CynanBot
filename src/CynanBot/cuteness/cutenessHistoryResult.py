import locale
from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessHistoryEntry import CutenessHistoryEntry


class CutenessHistoryResult():

    def __init__(
        self,
        userId: str,
        userName: str,
        bestCuteness: Optional[CutenessHistoryEntry] = None,
        totalCuteness: Optional[int] = None,
        entries: Optional[List[CutenessHistoryEntry]] = None
    ):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif bestCuteness is not None and not isinstance(bestCuteness, CutenessHistoryEntry):
            raise ValueError(f'bestCuteness argument is malformed: \"{bestCuteness}\"')
        elif totalCuteness is not None and not utils.isValidInt(totalCuteness):
            raise ValueError(f'totalCuteness argument is malformed: \"{totalCuteness}\"')
        elif totalCuteness is not None and (totalCuteness < 0 or totalCuteness > utils.getLongMaxSafeSize()):
            raise ValueError(f'totalCuteness argument is out of bounds: {totalCuteness}')
        elif entries is not None and not isinstance(entries, List):
            raise ValueError(f'entries argument is malformed: \"{entries}\"')

        self.__userId: str = userId
        self.__userName: str = userName
        self.__bestCuteness: Optional[CutenessHistoryEntry] = bestCuteness
        self.__totalCuteness: Optional[int] = totalCuteness
        self.__entries: Optional[List[CutenessHistoryEntry]] = entries

    def getBestCuteness(self) -> Optional[CutenessHistoryEntry]:
        return self.__bestCuteness

    def getEntries(self) -> Optional[List[CutenessHistoryEntry]]:
        return self.__entries

    def getTotalCuteness(self) -> Optional[int]:
        return self.__totalCuteness

    def getTotalCutenessStr(self) -> str:
        totalCuteness = self.requireTotalCuteness()
        return locale.format_string("%d", totalCuteness, grouping = True)

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def requireTotalCuteness(self) -> int:
        totalCuteness = self.__totalCuteness

        if not utils.isValidInt(totalCuteness):
            raise RuntimeError(f'No totalCuteness value is available: {totalCuteness}')

        return totalCuteness
