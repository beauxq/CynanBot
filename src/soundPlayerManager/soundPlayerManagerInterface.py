from abc import ABC, abstractmethod
from typing import Collection

from .soundAlert import SoundAlert


class SoundPlayerManagerInterface(ABC):

    @abstractmethod
    async def isPlaying(self) -> bool:
        pass

    @abstractmethod
    async def playPlaylist(
        self,
        filePaths: Collection[str],
        volume: int | None = None
    ) -> bool:
        pass

    @abstractmethod
    async def playSoundAlert(
        self,
        alert: SoundAlert,
        volume: int | None = None
    ) -> bool:
        pass

    @abstractmethod
    async def playSoundFile(
        self,
        filePath: str | None,
        volume: int | None = None
    ) -> bool:
        pass
