from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime


class CheerActionRemodData():

    def __init__(
        self,
        remodDateTime: SimpleDateTime,
        broadcasterUserId: str,
        broadcasterUserName: str,
        userId: str
    ):
        if not isinstance(remodDateTime, SimpleDateTime):
            raise TypeError(f'remodDateTime argument is malformed: \"{remodDateTime}\"')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(broadcasterUserName):
            raise TypeError(f'broadcasterUserName argument is malformed: \"{broadcasterUserName}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        self.__remodDateTime: SimpleDateTime = remodDateTime
        self.__broadcasterUserId: str = broadcasterUserId
        self.__broadcasterUserName: str = broadcasterUserName
        self.__userId: str = userId

    def getBroadcasterUserId(self) -> str:
        return self.__broadcasterUserId

    def getBroadcasterUserName(self) -> str:
        return self.__broadcasterUserName

    def getRemodDateTime(self) -> SimpleDateTime:
        return self.__remodDateTime

    def getUserId(self) -> str:
        return self.__userId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'broadcasterUserId': self.__broadcasterUserId,
            'broadcasterUserName': self.__broadcasterUserName,
            'remodDateTime': self.__remodDateTime,
            'userId': self.__userId
        }
