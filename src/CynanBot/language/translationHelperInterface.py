from abc import ABC, abstractmethod

from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.translationResponse import TranslationResponse


class TranslationHelperInterface(ABC):

    @abstractmethod
    async def translate(
        self,
        text: str,
        targetLanguage: LanguageEntry | None = None
    ) -> TranslationResponse:
        pass
