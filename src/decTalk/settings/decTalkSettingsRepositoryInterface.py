from abc import abstractmethod

from ..models.decTalkVoice import DecTalkVoice
from ...misc.clearable import Clearable


class DecTalkSettingsRepositoryInterface(Clearable):

    @abstractmethod
    async def getDecTalkExecutablePath(self) -> str | None:
        pass

    @abstractmethod
    async def getDefaultVoice(self) -> DecTalkVoice:
        pass

    @abstractmethod
    async def getMediaPlayerVolume(self) -> int | None:
        pass

    @abstractmethod
    async def requireDecTalkExecutablePath(self) -> str:
        pass
