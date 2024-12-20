from abc import ABC, abstractmethod
from dataclasses import dataclass

from ..models.microsoftSamVoice import MicrosoftSamVoice


class MicrosoftSamMessageVoiceParserInterface(ABC):

    @dataclass(frozen = True)
    class Result:
        message: str
        voice: MicrosoftSamVoice

    @abstractmethod
    async def determineVoiceFromMessage(self, message: str | None) -> Result | None:
        pass
