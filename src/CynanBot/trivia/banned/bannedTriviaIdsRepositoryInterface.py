from abc import ABC, abstractmethod

from CynanBot.trivia.banned.bannedTriviaQuestion import BannedTriviaQuestion
from CynanBot.trivia.banned.banTriviaQuestionResult import \
    BanTriviaQuestionResult
from CynanBot.trivia.questions.triviaSource import TriviaSource


class BannedTriviaIdsRepositoryInterface(ABC):

    @abstractmethod
    async def ban(
        self,
        triviaId: str,
        userId: str,
        triviaSource: TriviaSource
    ) -> BanTriviaQuestionResult:
        pass

    @abstractmethod
    async def getInfo(
        self,
        triviaId: str,
        triviaSource: TriviaSource
    ) -> BannedTriviaQuestion | None:
        pass

    @abstractmethod
    async def isBanned(self, triviaId: str, triviaSource: TriviaSource) -> bool:
        pass

    @abstractmethod
    async def unban(
        self,
        triviaId: str,
        triviaSource: TriviaSource
    ) -> BanTriviaQuestionResult:
        pass
