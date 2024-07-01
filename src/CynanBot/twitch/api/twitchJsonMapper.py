from datetime import datetime, timedelta
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchApiScope import TwitchApiScope
from CynanBot.twitch.api.twitchBanRequest import TwitchBanRequest
from CynanBot.twitch.api.twitchBroadcasterType import TwitchBroadcasterType
from CynanBot.twitch.api.twitchEmoteImageFormat import TwitchEmoteImageFormat
from CynanBot.twitch.api.twitchEmoteImageScale import TwitchEmoteImageScale
from CynanBot.twitch.api.twitchEmoteType import TwitchEmoteType
from CynanBot.twitch.api.twitchJsonMapperInterface import \
    TwitchJsonMapperInterface
from CynanBot.twitch.api.twitchSendChatDropReason import \
    TwitchSendChatDropReason
from CynanBot.twitch.api.twitchSendChatMessageResponse import \
    TwitchSendChatMessageResponse
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from CynanBot.twitch.api.twitchThemeMode import TwitchThemeMode
from CynanBot.twitch.api.twitchTokensDetails import TwitchTokensDetails
from CynanBot.twitch.api.twitchValidationResponse import \
    TwitchValidationResponse


class TwitchJsonMapper(TwitchJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

    async def __calculateExpirationTime(self, expiresInSeconds: int | None) -> datetime:
        now = datetime.now(self.__timeZoneRepository.getDefault())

        if utils.isValidInt(expiresInSeconds) and expiresInSeconds > 0:
            return now + timedelta(seconds = expiresInSeconds)
        else:
            return now - timedelta(weeks = 1)

    async def parseApiScope(
        self,
        apiScope: str | None
    ) -> TwitchApiScope | None:
        if not utils.isValidStr(apiScope):
            return None

        apiScope = apiScope.lower()

        match apiScope:
            case 'bits:read': return TwitchApiScope.BITS_READ
            case 'channel:bot': return TwitchApiScope.CHANNEL_BOT
            case 'channel:manage:moderators': return TwitchApiScope.CHANNEL_MANAGE_MODERATORS
            case 'channel:manage:polls': return TwitchApiScope.CHANNEL_MANAGE_POLLS
            case 'channel:manage:predictions': return TwitchApiScope.CHANNEL_MANAGE_PREDICTIONS
            case 'channel:manage:redemptions': return TwitchApiScope.CHANNEL_MANAGE_REDEMPTIONS
            case 'channel:moderate': return TwitchApiScope.CHANNEL_MODERATE
            case 'channel:read:polls': return TwitchApiScope.CHANNEL_READ_POLLS
            case 'channel:read:predictions': return TwitchApiScope.CHANNEL_READ_PREDICTIONS
            case 'channel:read:redemptions': return TwitchApiScope.CHANNEL_READ_REDEMPTIONS
            case 'channel:read:subscriptions': return TwitchApiScope.CHANNEL_READ_SUBSCRIPTIONS
            case 'channel_editor': return TwitchApiScope.CHANNEL_EDITOR
            case 'chat:edit': return TwitchApiScope.CHAT_EDIT
            case 'chat:read': return TwitchApiScope.CHAT_READ
            case 'moderation:read': return TwitchApiScope.MODERATION_READ
            case 'moderator:manage:banned_users': return TwitchApiScope.MODERATOR_MANAGE_BANNED_USERS
            case 'moderator:manage:chat_messages': return TwitchApiScope.MODERATOR_MANAGE_CHAT_MESSAGES
            case 'moderator:read:chatters': return TwitchApiScope.MODERATOR_READ_CHATTERS
            case 'moderator:read:chat_settings': return TwitchApiScope.MODERATOR_READ_CHAT_SETTINGS
            case 'moderator:read:followers': return TwitchApiScope.MODERATOR_READ_FOLLOWERS
            case 'user:bot': return TwitchApiScope.USER_BOT
            case 'user:read:broadcast': return TwitchApiScope.USER_READ_BROADCAST
            case 'user:read:chat': return TwitchApiScope.USER_READ_CHAT
            case 'user:read:emotes': return TwitchApiScope.USER_READ_EMOTES
            case 'user:read:follows': return TwitchApiScope.USER_READ_FOLLOWS
            case 'user:read:subscriptions': return TwitchApiScope.USER_READ_SUBSCRIPTIONS
            case 'user:write:chat': return TwitchApiScope.USER_WRITE_CHAT
            case 'whispers:edit': return TwitchApiScope.WHISPERS_EDIT
            case 'whispers:read': return TwitchApiScope.WHISPERS_READ
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchApiScope value: \"{apiScope}\"')
                return None

    async def parseBroadcasterType(
        self,
        broadcasterType: str | None
    ) -> TwitchBroadcasterType | None:
        if not utils.isValidStr(broadcasterType):
            return None

        broadcasterType = broadcasterType.lower()

        match broadcasterType:
            case 'affiliate': return TwitchBroadcasterType.AFFILIATE
            case 'partner': return TwitchBroadcasterType.PARTNER
            case _: return TwitchBroadcasterType.NORMAL

    async def parseEmoteImageFormat(
        self,
        emoteImageFormat: str | None
    ) -> TwitchEmoteImageFormat | None:
        if not utils.isValidStr(emoteImageFormat):
            return None

        emoteImageFormat = emoteImageFormat.lower()

        match emoteImageFormat:
            case 'animated': return TwitchEmoteImageFormat.ANIMATED
            case 'static': return TwitchEmoteImageFormat.STATIC
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchEmoteImageFormat value: \"{emoteImageFormat}\"')
                return None

    async def parseEmoteImageScale(
        self,
        emoteImageScale: str | None
    ) -> TwitchEmoteImageScale | None:
        if not utils.isValidStr(emoteImageScale):
            return None

        emoteImageScale = emoteImageScale.lower()

        match emoteImageScale:
            case 'url_1x': return TwitchEmoteImageScale.SMALL
            case 'url_2x': return TwitchEmoteImageScale.MEDIUM
            case 'url_4x': return TwitchEmoteImageScale.LARGE
            case '1.0': return TwitchEmoteImageScale.SMALL
            case '2.0': return TwitchEmoteImageScale.MEDIUM
            case '3.0': return TwitchEmoteImageScale.LARGE
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchEmoteImageScale value: \"{emoteImageScale}\"')
                return None

    async def parseEmoteType(
        self,
        emoteType: str | None
    ) -> TwitchEmoteType | None:
        if not utils.isValidStr(emoteType):
            return None

        emoteType = emoteType.lower()

        match emoteType:
            case 'bitstier': return TwitchEmoteType.BITS
            case 'follower': return TwitchEmoteType.FOLLOWER
            case 'subscriptions': return TwitchEmoteType.SUBSCRIPTIONS
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchEmoteType value: \"{emoteType}\"')
                return None

    async def parseSendChatDropReason(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchSendChatDropReason | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        code = utils.getStrFromDict(jsonResponse, 'code')

        message: str | None
        if 'message' in jsonResponse and utils.isValidStr(jsonResponse.get('message')):
            message = utils.getStrFromDict(jsonResponse, 'message')

        return TwitchSendChatDropReason(
            code = code,
            message = message
        )

    async def parseSendChatMessageResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchSendChatMessageResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        data: list[dict[str, Any]] | Any | None = jsonResponse.get('data')
        if not isinstance(data, list) or len(data) == 0:
            return None

        dataEntry: dict[str, Any] | Any | None = data[0]
        if not isinstance(dataEntry, dict) or len(dataEntry) == 0:
            return None

        isSent = utils.getBoolFromDict(dataEntry, 'is_sent', fallback = False)
        messageId = utils.getStrFromDict(dataEntry, 'message_id')
        dropReason = await self.parseSendChatDropReason(dataEntry.get('drop_reason'))

        return TwitchSendChatMessageResponse(
            isSent = isSent,
            messageId = messageId,
            dropReason = dropReason
        )

    async def parseSubscriberTier(
        self,
        subscriberTier: str | None
    ) -> TwitchSubscriberTier | None:
        if not utils.isValidStr(subscriberTier):
            return None

        subscriberTier = subscriberTier.lower()

        match subscriberTier:
            case 'prime': return TwitchSubscriberTier.PRIME
            case '1000': return TwitchSubscriberTier.TIER_ONE
            case '2000': return TwitchSubscriberTier.TIER_TWO
            case '3000': return TwitchSubscriberTier.TIER_THREE
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchSubscriberTier value: \"{subscriberTier}\"')
                return None

    async def parseThemeMode(
        self,
        themeMode: str | None
    ) -> TwitchThemeMode | None:
        if not utils.isValidStr(themeMode):
            return None

        themeMode = themeMode.lower()

        match themeMode:
            case 'dark': return TwitchThemeMode.DARK
            case 'light': return TwitchThemeMode.LIGHT
            case _:
                self.__timber.log('TwitchJsonMapper', f'Encountered unknown TwitchThemeMode value: \"{themeMode}\"')
                return None

    async def parseTokensDetails(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchTokensDetails | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        expirationTime = await self.__calculateExpirationTime(
            expiresInSeconds = utils.getIntFromDict(jsonResponse, 'expires_in', fallback = -1)
        )

        if not 'access_token' in jsonResponse or not utils.isValidStr(jsonResponse.get('access_token')):
            self.__timber.log('TwitchJsonMapper', f'Tokens details JSON data does not include valid \"access_token\" value ({jsonResponse=})')
            return None

        accessToken = utils.getStrFromDict(jsonResponse, 'access_token')

        if not 'refresh_token' in jsonResponse or not utils.isValidStr(jsonResponse.get('refresh_token')):
            self.__timber.log('TwitchJsonMapper', f'Tokens details JSON data does not include valid \"refresh_token\" value ({jsonResponse=})')
            return None

        refreshToken = utils.getStrFromDict(jsonResponse, 'refresh_token')

        return TwitchTokensDetails(
            expirationTime = expirationTime,
            accessToken = accessToken,
            refreshToken = refreshToken
        )

    async def parseValidationResponse(
        self,
        jsonResponse: dict[str, Any] | Any | None
    ) -> TwitchValidationResponse | None:
        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            return None

        expiresInSeconds = utils.getIntFromDict(jsonResponse, 'expires_in')
        clientId = utils.getStrFromDict(jsonResponse, 'client_id')
        login = utils.getStrFromDict(jsonResponse, 'login')
        userId = utils.getStrFromDict(jsonResponse, 'user_id')

        now = datetime.now(self.__timeZoneRepository.getDefault())
        expiresAt = now + timedelta(seconds = expiresInSeconds)

        scopesArray: list[str] | None = jsonResponse.get('scopes')
        scopes: set[TwitchApiScope] = set()

        if isinstance(scopesArray, list) and len(scopesArray) >= 1:
            for index, scopeString in enumerate(scopesArray):
                scope = await self.parseApiScope(scopeString)

                if scope is None:
                    self.__timber.log('TwitchJsonMapper', f'Unable to parse value at index {index} for \"scopes\" data ({scopeString=}) ({jsonResponse=})')
                else:
                    scopes.add(scope)

        return TwitchValidationResponse(
            expiresAt = expiresAt,
            expiresInSeconds = expiresInSeconds,
            clientId = clientId,
            scopes = scopes,
            login = login,
            userId = userId
        )

    async def requireSubscriberTier(
        self,
        subscriberTier: str | None
    ) -> TwitchSubscriberTier:
        result = await self.parseSubscriberTier(subscriberTier)

        if result is None:
            raise ValueError(f'Unable to parse \"{subscriberTier}\" into TwitchSubscriberTier value!')

        return result

    async def serializeBanRequest(
        self,
        banRequest: TwitchBanRequest
    ) -> dict[str, Any]:
        if not isinstance(banRequest, TwitchBanRequest):
            raise TypeError(f'banRequest argument is malformed: \"{banRequest}\"')

        data: dict[str, Any] = {
            'user_id': banRequest.userIdToBan
        }

        if utils.isValidInt(banRequest.duration):
            data['duration'] = banRequest.duration

        if utils.isValidStr(banRequest.reason):
            data['reason'] = banRequest.reason

        return {
            'data': data
        }
