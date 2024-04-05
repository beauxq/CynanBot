import random

import CynanBot.misc.utils as utils
from CynanBot.storage.backingDatabase import BackingDatabase
from CynanBot.storage.databaseConnection import DatabaseConnection
from CynanBot.storage.databaseType import DatabaseType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.triviaEmoteGeneratorInterface import \
    TriviaEmoteGeneratorInterface


class TriviaEmoteGenerator(TriviaEmoteGeneratorInterface):

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        timber: TimberInterface
    ):
        if not isinstance(backingDatabase, BackingDatabase):
            raise TypeError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber arguent is malformed: \"{timber}\"')

        self.__backingDatabase: BackingDatabase = backingDatabase
        self.__timber: TimberInterface = timber

        self.__isDatabaseReady: bool = False
        self.__emotesDict: dict[str, set[str] | None] = self.__createEmotesDict()
        self.__emotesList: list[str] = list(self.__emotesDict)

    def __createEmotesDict(self) -> dict[str, set[str] | None]:
        # Creates and returns a dictionary of emojis, with a set of emojis that should be
        # considered equivalent. For example: 👨‍🔬 (man scientist) and 👩‍🔬 (woman scientist)
        # should both be considered equivalents of the primary "root" 🧑‍🔬 (scientist) emoji.
        #
        # If a set is either None or empty, then the given emoji has no equivalent.

        emotesDict: dict[str, set[str] | None] = dict()
        emotesDict['🧮'] = None
        emotesDict['👽'] = None
        emotesDict['👾'] = None
        emotesDict['🥑'] = None
        emotesDict['🥓'] = None
        emotesDict['🎒'] = None
        emotesDict['🍌'] = None
        emotesDict['📊'] = None
        emotesDict['🏖️'] = { '⛱️', '☂️', '☔' }
        emotesDict['🫑'] = None
        emotesDict['🐦'] = { '🐤' }
        emotesDict['🎂'] = { '🍰' }
        emotesDict['🫐'] = None
        emotesDict['📚'] = None
        emotesDict['💼'] = None
        emotesDict['🚌'] = None
        emotesDict['🍬'] = { '🍭' }
        emotesDict['📇'] = None
        emotesDict['🥕'] = None
        emotesDict['🧀'] = None
        emotesDict['🍒'] = None
        emotesDict['🏛️'] = { '🏦' }
        emotesDict['📋'] = None
        emotesDict['💽'] = { '📀', '💿' }
        emotesDict['🍪'] = { '🥠' }
        emotesDict['🐄'] = { '🐮' }
        emotesDict['🦀'] = None
        emotesDict['🖍️'] = None
        emotesDict['🧁'] = None
        emotesDict['🍛'] = None
        emotesDict['🧬'] = None
        emotesDict['🐬'] = None
        emotesDict['🐉'] = { '🐲', '🦖' }
        emotesDict['🐘'] = None
        emotesDict['🧐'] = None
        emotesDict['🚒'] = None
        emotesDict['💾'] = None
        emotesDict['🐸'] = None
        emotesDict['👻'] = None
        emotesDict['🍇'] = None
        emotesDict['🍏'] = None
        emotesDict['🚁'] = None
        emotesDict['🌶️'] = None
        emotesDict['🎃'] = None
        emotesDict['📒'] = None
        emotesDict['💡'] = None
        emotesDict['🦁'] = None
        emotesDict['🕰️'] = None
        emotesDict['🍈'] = { '🍉' }
        emotesDict['🔬'] = None
        emotesDict['🐒'] = { '🐵' }
        emotesDict['🍄'] = None
        emotesDict['🤓'] = None
        emotesDict['📓'] = None
        emotesDict['📎'] = None
        emotesDict['🍐'] = None
        emotesDict['🐧'] = None
        emotesDict['🥧'] = None
        emotesDict['🐖'] = { '🐷' }
        emotesDict['🍍'] = None
        emotesDict['🍕'] = None
        emotesDict['🥔'] = None
        emotesDict['🍎'] = None
        emotesDict['🌈'] = None
        emotesDict['🍙'] = None
        emotesDict['🍠'] = None
        emotesDict['🤖'] = None
        emotesDict['🚀'] = None
        emotesDict['🏫'] = None
        emotesDict['🦐'] = { '🍤' }
        emotesDict['🐚'] = None
        emotesDict['🦑'] = { '🐙' }
        emotesDict['📏'] = None
        emotesDict['🍓'] = None
        emotesDict['🍊'] = None
        emotesDict['🔭'] = None
        emotesDict['🤔'] = None
        emotesDict['💭'] = None
        emotesDict['🐅'] = { '🐯' }
        emotesDict['📐'] = None
        emotesDict['🌷'] = { '🌹' }
        emotesDict['🐢'] = None
        emotesDict['🌊'] = { '💧', '💦' }
        emotesDict['🐋'] = None

        return emotesDict

    async def getCurrentEmoteFor(self, twitchChannel: str, twitchChannelId: str) -> str:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        emoteIndex = await self.__getCurrentEmoteIndexFor(twitchChannel)

        if emoteIndex < 0 or emoteIndex >= len(self.__emotesList):
            self.__timber.log('TriviaEmoteGenerator', f'Encountered out of bounds emoteIndex for \"{twitchChannel}\": {emoteIndex}')
            emoteIndex = 0

        return self.__emotesList[emoteIndex]

    async def __getCurrentEmoteIndexFor(self, twitchChannel: str) -> int:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        connection = await self.__getDatabaseConnection()
        record = await connection.fetchRow(
            '''
                SELECT emoteindex FROM triviaemotes
                WHERE twitchchannel = $1
                LIMIT 1
            ''',
            twitchChannel
        )

        emoteIndex: int | None = None
        if record is not None and len(record) >= 1:
            emoteIndex = record[0]

        await connection.close()

        if not utils.isValidInt(emoteIndex) or emoteIndex < 0 or emoteIndex >= len(self.__emotesList):
            emoteIndex = 0

        return emoteIndex

    async def __getDatabaseConnection(self) -> DatabaseConnection:
        await self.__initDatabaseTable()
        return await self.__backingDatabase.getConnection()

    async def getNextEmoteFor(self, twitchChannel: str, twitchChannelId: str) -> str:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')

        emoteIndex = await self.__getCurrentEmoteIndexFor(twitchChannel)
        emoteIndex = (emoteIndex + 1) % len(self.__emotesList)

        connection = await self.__getDatabaseConnection()
        await connection.execute(
            '''
                INSERT INTO triviaemotes (emoteindex, twitchchannel)
                VALUES ($1, $2)
                ON CONFLICT (twitchchannel) DO UPDATE SET emoteindex = EXCLUDED.emoteindex
            ''',
            emoteIndex, twitchChannel
        )

        await connection.close()
        return self.__emotesList[emoteIndex]

    def getRandomEmote(self) -> str:
        return random.choice(self.__emotesList)

    async def getValidatedAndNormalizedEmote(self, emote: str | None) -> str | None:
        if not utils.isValidStr(emote):
            return None

        if emote in self.__emotesDict:
            return emote

        for emoteKey, equivalentEmotes in self.__emotesDict.items():
            if equivalentEmotes is not None and len(equivalentEmotes) >= 1:
                if emote in equivalentEmotes:
                    return emoteKey

        return None

    async def __initDatabaseTable(self):
        if self.__isDatabaseReady:
            return

        self.__isDatabaseReady = True
        connection = await self.__backingDatabase.getConnection()

        if connection.getDatabaseType() is DatabaseType.POSTGRESQL:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS triviaemotes (
                        emoteindex smallint DEFAULT 0 NOT NULL,
                        twitchchannel public.citext NOT NULL PRIMARY KEY
                    )
                '''
            )
        elif connection.getDatabaseType() is DatabaseType.SQLITE:
            await connection.createTableIfNotExists(
                '''
                    CREATE TABLE IF NOT EXISTS triviaemotes (
                        emoteindex INTEGER NOT NULL DEFAULT 0,
                        twitchchannel TEXT NOT NULL PRIMARY KEY COLLATE NOCASE
                    )
                '''
            )
        else:
            raise RuntimeError(f'Encountered unexpected DatabaseType when trying to create tables: \"{connection.getDatabaseType()}\"')

        await connection.close()
