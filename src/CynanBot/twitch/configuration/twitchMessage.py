from abc import ABC, abstractmethod

from CynanBot.twitch.configuration.twitchAuthor import TwitchAuthor
from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchConfigurationType import \
    TwitchConfigurationType


class TwitchMessage(ABC):

    @abstractmethod
    def getAuthor(self) -> TwitchAuthor:
        pass

    @abstractmethod
    def getAuthorId(self) -> str:
        pass

    @abstractmethod
    def getAuthorName(self) -> str:
        pass

    @abstractmethod
    def getChannel(self) -> TwitchChannel:
        pass

    @abstractmethod
    def getContent(self) -> str | None:
        pass

    @abstractmethod
    async def getTwitchChannelId(self) -> str:
        pass

    @abstractmethod
    def getTwitchChannelName(self) -> str:
        pass

    @abstractmethod
    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        pass

    @abstractmethod
    def isEcho(self) -> bool:
        pass

    @abstractmethod
    def isReply(self) -> bool:
        pass
