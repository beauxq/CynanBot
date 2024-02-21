from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.tts.ttsRaidInfo import TtsRaidInfo


class TtsEvent():

    def __init__(
        self,
        message: Optional[str],
        twitchChannel: str,
        userId: str,
        userName: str,
        donation: Optional[TtsDonation],
        provider: TtsProvider,
        raidInfo: Optional[TtsRaidInfo]
    ):
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif donation is not None and not isinstance(donation, TtsDonation):
            raise TypeError(f'donation argument is malformed: \"{donation}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')
        elif raidInfo is not None and not isinstance(raidInfo, TtsRaidInfo):
            raise TypeError(f'raidInfo argument is malformed: \"{raidInfo}\"')

        self.__message: Optional[str] = message
        self.__twitchChannel: str = twitchChannel
        self.__userId: str = userId
        self.__userName: str = userName
        self.__donation: Optional[TtsDonation] = donation
        self.__provider: TtsProvider = provider
        self.__raidInfo: Optional[TtsRaidInfo] = raidInfo

    def getDonation(self) -> Optional[TtsDonation]:
        return self.__donation

    def getMessage(self) -> Optional[str]:
        return self.__message

    def getProvider(self) -> TtsProvider:
        return self.__provider

    def getRaidInfo(self) -> Optional[TtsRaidInfo]:
        return self.__raidInfo

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'donation': self.__donation,
            'message': self.__message,
            'provider': self.__provider,
            'raidInfo': self.__raidInfo,
            'twitchChannel': self.__twitchChannel,
            'userId': self.__userId,
            'userName': self.__userName
        }
