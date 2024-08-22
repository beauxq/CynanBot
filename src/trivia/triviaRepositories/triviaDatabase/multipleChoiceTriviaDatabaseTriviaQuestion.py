from frozenlist import FrozenList

from .triviaDatabaseTriviaQuestion import TriviaDatabaseTriviaQuestion
from ...questions.triviaQuestionType import TriviaQuestionType
from ...triviaDifficulty import TriviaDifficulty
from ....misc import utils as utils


class MultipleChoiceTriviaDatabaseTriviaQuestion(TriviaDatabaseTriviaQuestion):

    def __init__(
        self,
        incorrectAnswers: FrozenList[str],
        category: str | None,
        correctAnswer: str,
        question: str,
        triviaId: str,
        difficulty: TriviaDifficulty
    ):
        super().__init__(
            category = category,
            question = question,
            triviaId = triviaId,
            difficulty = difficulty
        )

        if not isinstance(incorrectAnswers, FrozenList) or len(incorrectAnswers) == 0:
            raise TypeError(f'incorrectAnswers argument is malformed: \"{incorrectAnswers}\"')
        elif not utils.isValidStr(correctAnswer):
            raise TypeError(f'correctAnswer argument is malformed: \"{correctAnswer}\"')

        self.__incorrectAnswers: FrozenList[str] = incorrectAnswers
        self.__correctAnswer: str = correctAnswer

    @property
    def correctAnswer(self) -> str:
        return self.__correctAnswer

    @property
    def incorrectAnswers(self) -> FrozenList[str]:
        return self.__incorrectAnswers

    @property
    def triviaType(self) -> TriviaQuestionType:
        return TriviaQuestionType.MULTIPLE_CHOICE
