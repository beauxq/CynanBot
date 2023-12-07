from typing import Optional

from twitchio.channel import Channel

import CynanBot.misc.utils as utils
from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.configuration.twitchConfigurationType import \
    TwitchConfigurationType
from CynanBot.twitch.configuration.twitchMessageable import TwitchMessageable
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface


class TwitchIoChannel(TwitchChannel, TwitchMessageable):

    def __init__(
        self,
        channel: Channel,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(channel, Channel):
            raise ValueError(f'channel argument is malformed: \"{channel}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__channel: Channel = channel
        self.__channelId: Optional[str] = None
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def getTwitchChannelId(self) -> str:
        channelId = self.__channelId

        if channelId is None:
            channelId = await self.__userIdsRepository.requireUserId(
                userName = self.getTwitchChannelName()
            )

        return channelId

    def getTwitchChannelName(self) -> str:
        return self.__channel.name

    def getTwitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO

    async def send(self, message: str):
        await self.__channel.send(message)

    def __str__(self) -> str:
        return self.getTwitchChannelName()
