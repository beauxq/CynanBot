from abc import ABC, abstractmethod

from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.users.userInterface import UserInterface


class AbsTwitchFollowHandler(ABC):

    @abstractmethod
    async def onNewFollow(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        pass
