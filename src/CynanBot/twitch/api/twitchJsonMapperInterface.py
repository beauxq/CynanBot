from abc import ABC, abstractmethod
from typing import Any

from CynanBot.twitch.api.twitchApiScope import TwitchApiScope
from CynanBot.twitch.api.twitchBanRequest import TwitchBanRequest
from CynanBot.twitch.api.twitchBroadcasterType import TwitchBroadcasterType
from CynanBot.twitch.api.twitchSendChatDropReason import \
    TwitchSendChatDropReason
from CynanBot.twitch.api.twitchSendChatMessageResponse import \
    TwitchSendChatMessageResponse
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from CynanBot.twitch.api.twitchTokensDetails import TwitchTokensDetails
from CynanBot.twitch.api.twitchValidationResponse import \
    TwitchValidationResponse


class TwitchJsonMapperInterface(ABC):

    @abstractmethod
    async def parseApiScope(
        self,
        apiScope: str | None
    ) -> TwitchApiScope | None:
        pass

    @abstractmethod
    async def parseBroadcasterType(
        self,
        broadcasterType: str | None
    ) -> TwitchBroadcasterType | None:
        pass

    @abstractmethod
    async def parseSendChatDropReason(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchSendChatDropReason | None:
        pass

    @abstractmethod
    async def parseSendChatMessageResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchSendChatMessageResponse | None:
        pass

    @abstractmethod
    async def parseSubscriberTier(
        self,
        subscriberTier: str | None
    ) -> TwitchSubscriberTier | None:
        pass

    @abstractmethod
    async def parseTokensDetails(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchTokensDetails | None:
        pass

    @abstractmethod
    async def parseValidationResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchValidationResponse | None:
        pass

    @abstractmethod
    async def requireSubscriberTier(
        self,
        subscriberTier: str | None
    ) -> TwitchSubscriberTier:
        pass

    @abstractmethod
    async def serializeBanRequest(
        self,
        banRequest: TwitchBanRequest
    ) -> dict[str, Any]:
        pass
