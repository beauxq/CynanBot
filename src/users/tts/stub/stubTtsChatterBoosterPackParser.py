from typing import Any

from frozendict import frozendict

from ....tts.ttsProvider import TtsProvider
from ...ttsChatters.ttsChatterBoosterPack import TtsChatterBoosterPack
from ...ttsChatters.ttsChatterBoosterPackParserInterface import TtsChatterBoosterPackParserInterface


class StubTtsChatterBoosterPackParser(TtsChatterBoosterPackParserInterface):

    def parseBoosterPack(
        self,
        defaultTtsProvider: TtsProvider,
        jsonContents: dict[str, Any]
    ) -> TtsChatterBoosterPack:
        # this method is intentionally empty
        raise RuntimeError()

    def parseBoosterPacks(
        self,
        defaultTtsProvider: TtsProvider,
        jsonContents: list[dict[str, Any]] | Any | None
    ) -> frozendict[str, TtsChatterBoosterPack] | None:
        return None