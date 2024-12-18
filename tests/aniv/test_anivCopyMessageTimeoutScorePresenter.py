import pytest

from src.aniv.anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from src.aniv.anivCopyMessageTimeoutScorePresenter import AnivCopyMessageTimeoutScorePresenter
from src.aniv.anivCopyMessageTimeoutScorePresenterInterface import AnivCopyMessageTimeoutScorePresenterInterface
from src.language.languageEntry import LanguageEntry


class TestAnivCopyMessageTimeoutScorePresenter:

    presenter: AnivCopyMessageTimeoutScorePresenterInterface = AnivCopyMessageTimeoutScorePresenter()

    @pytest.mark.asyncio
    async def test_toString_with0Dodges0TimeoutsScoreAndEnglish(self):
        chatterUserName = 'stashiocat'

        score = AnivCopyMessageTimeoutScore(
            mostRecentDodge = None,
            mostRecentTimeout = None,
            dodgeScore = 0,
            timeoutScore = 0,
            chatterUserId = 'abc123',
            chatterUserName = chatterUserName,
            twitchChannel = 'smCharles',
            twitchChannelId = 'def456'
        )

        printOut = await self.presenter.toString(
            score = score,
            language = LanguageEntry.ENGLISH,
            chatterUserName = 'stashiocat'
        )

        assert printOut == f'ⓘ @{chatterUserName} has no aniv timeouts'

    @pytest.mark.asyncio
    async def test_toString_with0Dodges0TimeoutsScoreAndSpanish(self):
        chatterUserName = 'stashiocat'

        score = AnivCopyMessageTimeoutScore(
            mostRecentDodge = None,
            mostRecentTimeout = None,
            dodgeScore = 0,
            timeoutScore = 0,
            chatterUserId = 'abc123',
            chatterUserName = chatterUserName,
            twitchChannel = 'smCharles',
            twitchChannelId = 'def456'
        )

        printOut = await self.presenter.toString(
            score = score,
            language = LanguageEntry.SPANISH,
            chatterUserName = chatterUserName
        )

        assert printOut == f'ⓘ @{chatterUserName} no tiene suspensiones de aniv'
