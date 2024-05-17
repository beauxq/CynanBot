from dataclasses import dataclass

from CynanBot.language.languageEntry import LanguageEntry


@dataclass(frozen = True)
class DeepLTranslationResponse():
    detectedSourceLanguage: LanguageEntry | None
    text: str
