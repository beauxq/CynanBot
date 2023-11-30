from abc import ABC, abstractmethod

from CynanBot.tts.ttsEvent import TtsEvent


class TtsManagerInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitTtsEvent(self, event: TtsEvent):
        pass
