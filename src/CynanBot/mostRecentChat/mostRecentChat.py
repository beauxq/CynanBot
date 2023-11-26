from typing import Any, Dict

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime


class MostRecentChat():

    def __init__(
        self,
        mostRecentChat: SimpleDateTime,
        twitchChannelId: str,
        userId: str
    ):
        if not isinstance(mostRecentChat, SimpleDateTime):
            raise ValueError(f'mostRecentChat argument is malformed: \"{mostRecentChat}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise ValueError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')

        self.__mostRecentChat: SimpleDateTime = mostRecentChat
        self.__twitchChannelId: str = twitchChannelId
        self.__userId: str = userId

    def getMostRecentChat(self) -> SimpleDateTime:
        return self.__mostRecentChat

    def getTwitchChannelId(self) -> str:
        return self.__twitchChannelId

    def getUserId(self) -> str:
        return self.__userId

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'mostRecentChat': self.__mostRecentChat,
            'twitchChannelId': self.__twitchChannelId,
            'userId': self.__userId
        }
