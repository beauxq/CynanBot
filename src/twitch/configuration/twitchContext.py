from abc import abstractmethod

from .twitchAuthor import TwitchAuthor
from .twitchConfigurationType import TwitchConfigurationType
from .twitchMessageTags import TwitchMessageTags
from .twitchMessageable import TwitchMessageable


class TwitchContext(TwitchMessageable):

    @abstractmethod
    def getAuthor(self) -> TwitchAuthor:
        pass

    @abstractmethod
    def getAuthorDisplayName(self) -> str:
        pass

    @abstractmethod
    def getAuthorId(self) -> str:
        pass

    @abstractmethod
    def getAuthorName(self) -> str:
        pass

    @abstractmethod
    def getMessageContent(self) -> str | None:
        pass

    @abstractmethod
    async def getMessageId(self) -> str:
        pass

    @abstractmethod
    async def getMessageTags(self) -> TwitchMessageTags:
        pass

    @abstractmethod
    def getTwitchChannelName(self) -> str:
        pass

    @abstractmethod
    def isAuthorMod(self) -> bool:
        pass

    @abstractmethod
    def isAuthorVip(self) -> bool:
        pass

    @abstractmethod
    async def isMessageFromExternalSharedChat(self) -> bool:
        pass

    @abstractmethod
    async def isMessageReply(self) -> bool:
        pass

    @abstractmethod
    async def send(self, message: str):
        pass

    @property
    @abstractmethod
    def twitchConfigurationType(self) -> TwitchConfigurationType:
        pass
