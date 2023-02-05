import asyncio
import locale

from authRepository import AuthRepository
from cutenessUtils import CutenessUtils
from cynanBot import CynanBot
from CynanBotCommon.chatLogger.chatLogger import ChatLogger
from CynanBotCommon.cuteness.cutenessRepository import CutenessRepository
from CynanBotCommon.funtoon.funtoonRepository import FuntoonRepository
from CynanBotCommon.language.jishoHelper import JishoHelper
from CynanBotCommon.language.languagesRepository import LanguagesRepository
from CynanBotCommon.language.translationHelper import TranslationHelper
from CynanBotCommon.language.wordOfTheDayRepository import \
    WordOfTheDayRepository
from CynanBotCommon.location.locationsRepository import LocationsRepository
from CynanBotCommon.network.aioHttpClientProvider import AioHttpClientProvider
from CynanBotCommon.network.networkClientProvider import NetworkClientProvider
from CynanBotCommon.network.networkClientType import NetworkClientType
from CynanBotCommon.network.requestsClientProvider import \
    RequestsClientProvider
from CynanBotCommon.pkmn.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWars.starWarsQuotesRepository import \
    StarWarsQuotesRepository
from CynanBotCommon.storage.backingDatabase import BackingDatabase
from CynanBotCommon.storage.backingPsqlDatabase import BackingPsqlDatabase
from CynanBotCommon.storage.backingSqliteDatabase import BackingSqliteDatabase
from CynanBotCommon.storage.databaseType import DatabaseType
from CynanBotCommon.storage.psqlCredentialsProvider import \
    PsqlCredentialsProvider
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from CynanBotCommon.trivia.bannedTriviaIdsRepository import \
    BannedTriviaIdsRepository
from CynanBotCommon.trivia.bannedWordsRepository import BannedWordsRepository
from CynanBotCommon.trivia.bongoTriviaQuestionRepository import \
    BongoTriviaQuestionRepository
from CynanBotCommon.trivia.funtoonTriviaQuestionRepository import \
    FuntoonTriviaQuestionRepository
from CynanBotCommon.trivia.jokeTriviaQuestionRepository import \
    JokeTriviaQuestionRepository
from CynanBotCommon.trivia.jServiceTriviaQuestionRepository import \
    JServiceTriviaQuestionRepository
from CynanBotCommon.trivia.lotrTriviaQuestionsRepository import \
    LotrTriviaQuestionRepository
from CynanBotCommon.trivia.millionaireTriviaQuestionRepository import \
    MillionaireTriviaQuestionRepository
from CynanBotCommon.trivia.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from CynanBotCommon.trivia.openTriviaQaTriviaQuestionRepository import \
    OpenTriviaQaTriviaQuestionRepository
from CynanBotCommon.trivia.pkmnTriviaQuestionRepository import \
    PkmnTriviaQuestionRepository
from CynanBotCommon.trivia.queuedTriviaGameStore import QueuedTriviaGameStore
from CynanBotCommon.trivia.quizApiTriviaQuestionRepository import \
    QuizApiTriviaQuestionRepository
from CynanBotCommon.trivia.shinyTriviaHelper import ShinyTriviaHelper
from CynanBotCommon.trivia.shinyTriviaOccurencesRepository import \
    ShinyTriviaOccurencesRepository
from CynanBotCommon.trivia.superTriviaCooldownHelper import \
    SuperTriviaCooldownHelper
from CynanBotCommon.trivia.triviaAnswerChecker import TriviaAnswerChecker
from CynanBotCommon.trivia.triviaAnswerCompiler import TriviaAnswerCompiler
from CynanBotCommon.trivia.triviaBanHelper import TriviaBanHelper
from CynanBotCommon.trivia.triviaContentScanner import TriviaContentScanner
from CynanBotCommon.trivia.triviaDatabaseTriviaQuestionRepository import \
    TriviaDatabaseTriviaQuestionRepository
from CynanBotCommon.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBotCommon.trivia.triviaGameControllersRepository import \
    TriviaGameControllersRepository
from CynanBotCommon.trivia.triviaGameGlobalControllersRepository import \
    TriviaGameGlobalControllersRepository
from CynanBotCommon.trivia.triviaGameMachine import TriviaGameMachine
from CynanBotCommon.trivia.triviaGameStore import TriviaGameStore
from CynanBotCommon.trivia.triviaHistoryRepository import \
    TriviaHistoryRepository
from CynanBotCommon.trivia.triviaIdGenerator import TriviaIdGenerator
from CynanBotCommon.trivia.triviaQuestionCompanyTriviaQuestionRepository import \
    TriviaQuestionCompanyTriviaQuestionRepository
from CynanBotCommon.trivia.triviaQuestionCompiler import TriviaQuestionCompiler
from CynanBotCommon.trivia.triviaRepository import TriviaRepository
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.trivia.triviaSettingsRepository import \
    TriviaSettingsRepository
from CynanBotCommon.trivia.triviaSourceInstabilityHelper import \
    TriviaSourceInstabilityHelper
from CynanBotCommon.trivia.triviaVerifier import TriviaVerifier
from CynanBotCommon.trivia.willFryTriviaQuestionRepository import \
    WillFryTriviaQuestionRepository
from CynanBotCommon.trivia.wwtbamTriviaQuestionRepository import \
    WwtbamTriviaQuestionRepository
from CynanBotCommon.twitch.twitchApiService import TwitchApiService
from CynanBotCommon.twitch.twitchTokensRepository import TwitchTokensRepository
from CynanBotCommon.users.userIdsRepository import UserIdsRepository
from CynanBotCommon.weather.weatherRepository import WeatherRepository
from generalSettingsRepository import GeneralSettingsRepository
from triviaUtils import TriviaUtils
from twitch.twitchUtils import TwitchUtils
from users.modifyUserDataHelper import ModifyUserDataHelper
from users.usersRepository import UsersRepository

locale.setlocale(locale.LC_ALL, 'en_US.utf8')


#################################
## Misc initialization section ##
#################################

eventLoop = asyncio.get_event_loop()
generalSettingsRepository = GeneralSettingsRepository()
timber = Timber(
    eventLoop = eventLoop
)

backingDatabase: BackingDatabase = None
if generalSettingsRepository.getAll().requireDatabaseType() is DatabaseType.POSTGRESQL:
    backingDatabase: BackingDatabase = BackingPsqlDatabase(
        eventLoop = eventLoop,
        psqlCredentialsProvider = PsqlCredentialsProvider()
    )
elif generalSettingsRepository.getAll().requireDatabaseType() is DatabaseType.SQLITE:
    backingDatabase: BackingDatabase = BackingSqliteDatabase(
        eventLoop = eventLoop
    )
else:
    raise RuntimeError(f'Unknown/misconfigured database type: \"{generalSettingsRepository.getAll().requireDatabaseType()}\"')

networkClientProvider: NetworkClientProvider = None
if generalSettingsRepository.getAll().requireNetworkClientType() is NetworkClientType.AIOHTTP:
    networkClientProvider: NetworkClientProvider = AioHttpClientProvider(
        eventLoop = eventLoop,
        timber = timber
    )
elif generalSettingsRepository.getAll().requireNetworkClientType() is NetworkClientType.REQUESTS:
    networkClientProvider: NetworkClientProvider = RequestsClientProvider(
        timber = timber
    )
else:
    raise RuntimeError(f'Unknown/misconfigured network client type: \"{generalSettingsRepository.getAll().requireNetworkClientType()}\"')

authRepository = AuthRepository()
twitchApiService = TwitchApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    twitchCredentialsProviderInterface = authRepository
)
twitchTokensRepository = TwitchTokensRepository(
    timber = timber,
    twitchApiService = twitchApiService
)
userIdsRepository = UserIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchApiService = twitchApiService
)
timeZoneRepository = TimeZoneRepository()
usersRepository = UsersRepository(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)
cutenessRepository = CutenessRepository(
    backingDatabase = backingDatabase,
    userIdsRepository = userIdsRepository
)
funtoonRepository = FuntoonRepository(
    networkClientProvider = networkClientProvider,
    timber = timber
)
languagesRepository = LanguagesRepository()

authSnapshot = authRepository.getAll()

translationHelper: TranslationHelper = None
if authSnapshot.hasDeepLAuthKey():
    translationHelper = TranslationHelper(
        languagesRepository = languagesRepository,
        networkClientProvider = networkClientProvider,
        deepLAuthKey = authSnapshot.requireDeepLAuthKey(),
        timber = timber
    )

weatherRepository: WeatherRepository = None
if authSnapshot.hasOneWeatherApiKey():
    weatherRepository = WeatherRepository(
        networkClientProvider = networkClientProvider,
        oneWeatherApiKey = authSnapshot.requireOneWeatherApiKey(),
        timber = timber
    )


###################################
## Trivia initialization section ##
###################################

bannedWordsRepository = BannedWordsRepository(
    timber = timber
)
shinyTriviaOccurencesRepository = ShinyTriviaOccurencesRepository(
    backingDatabase = backingDatabase
)
triviaAnswerCompiler = TriviaAnswerCompiler()
triviaIdGenerator = TriviaIdGenerator()
triviaQuestionCompiler = TriviaQuestionCompiler()
triviaSettingsRepository = TriviaSettingsRepository()
bannedTriviaIdsRepository = BannedTriviaIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
shinyTriviaHelper = ShinyTriviaHelper(
    cutenessRepository = cutenessRepository,
    shinyTriviaOccurencesRepository = shinyTriviaOccurencesRepository,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaBanHelper = TriviaBanHelper(
    bannedTriviaIdsRepository = bannedTriviaIdsRepository,
    funtoonRepository = funtoonRepository
)
triviaContentScanner = TriviaContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaEmoteGenerator = TriviaEmoteGenerator(
    backingDatabase = backingDatabase,
    timber = timber
)
triviaGameControllersRepository = TriviaGameControllersRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)
triviaGameGlobalControllersRepository = TriviaGameGlobalControllersRepository(
    administratorProviderInterface = generalSettingsRepository,
    backingDatabase = backingDatabase,
    timber = timber,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)
triviaHistoryRepository = TriviaHistoryRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    triviaSettingsRepository = triviaSettingsRepository
)
triviaScoreRepository = TriviaScoreRepository(
    backingDatabase = backingDatabase
)
triviaUtils = TriviaUtils(
    administratorProviderInterface = generalSettingsRepository,
    timber = timber,
    triviaGameControllersRepository = triviaGameControllersRepository,
    triviaGameGlobalControllersRepository = triviaGameGlobalControllersRepository,
    usersRepository = usersRepository
)

pokepediaRepository = PokepediaRepository(
    networkClientProvider = networkClientProvider,
    timber = timber
)

quizApiTriviaQuestionRepository: QuizApiTriviaQuestionRepository = None
if authSnapshot.hasQuizApiKey():
    quizApiTriviaQuestionRepository = QuizApiTriviaQuestionRepository(
        networkClientProvider = networkClientProvider,
        quizApiKey = authSnapshot.requireQuizApiKey(),
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    )

triviaRepository = TriviaRepository(
    bongoTriviaQuestionRepository = BongoTriviaQuestionRepository(
        networkClientProvider = networkClientProvider,
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaIdGenerator = triviaIdGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    funtoonTriviaQuestionRepository = FuntoonTriviaQuestionRepository(
        networkClientProvider = networkClientProvider,
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    jokeTriviaQuestionRepository = JokeTriviaQuestionRepository(
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    jServiceTriviaQuestionRepository = JServiceTriviaQuestionRepository(
        networkClientProvider = networkClientProvider,
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaIdGenerator = triviaIdGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    lotrTriviaQuestionRepository = LotrTriviaQuestionRepository(
        timber = timber,
        triviaAnswerCompiler = triviaAnswerCompiler,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    millionaireTriviaQuestionRepository = MillionaireTriviaQuestionRepository(
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    openTriviaDatabaseTriviaQuestionRepository = OpenTriviaDatabaseTriviaQuestionRepository(
        networkClientProvider = networkClientProvider,
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaIdGenerator = triviaIdGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    openTriviaQaTriviaQuestionRepository = OpenTriviaQaTriviaQuestionRepository(
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    pkmnTriviaQuestionRepository = PkmnTriviaQuestionRepository(
        pokepediaRepository = pokepediaRepository,
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaIdGenerator = triviaIdGenerator,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    quizApiTriviaQuestionRepository = quizApiTriviaQuestionRepository,
    timber = timber,
    triviaDatabaseTriviaQuestionRepository = TriviaDatabaseTriviaQuestionRepository(
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    triviaQuestionCompanyTriviaQuestionRepository = TriviaQuestionCompanyTriviaQuestionRepository(
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    triviaSourceInstabilityHelper = TriviaSourceInstabilityHelper(
        timber = timber
    ),
    triviaSettingsRepository = triviaSettingsRepository,
    triviaVerifier = TriviaVerifier(
        bannedTriviaIdsRepository = bannedTriviaIdsRepository,
        timber = timber,
        triviaContentScanner = triviaContentScanner,
        triviaHistoryRepository = triviaHistoryRepository
    ),
    willFryTriviaQuestionRepository = WillFryTriviaQuestionRepository(
        networkClientProvider = networkClientProvider,
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaIdGenerator = triviaIdGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    ),
    wwtbamTriviaQuestionRepository = WwtbamTriviaQuestionRepository(
        timber = timber,
        triviaEmoteGenerator = triviaEmoteGenerator,
        triviaQuestionCompiler = triviaQuestionCompiler,
        triviaSettingsRepository = triviaSettingsRepository
    )
)


#####################################
## CynanBot initialization section ##
#####################################

cynanBot = CynanBot(
    eventLoop = eventLoop,
    authRepository = authRepository,
    bannedWordsRepository = bannedWordsRepository,
    chatLogger = ChatLogger(
        eventLoop = eventLoop,
    ),
    cutenessRepository = cutenessRepository,
    cutenessUtils = CutenessUtils(),
    funtoonRepository = funtoonRepository,
    generalSettingsRepository = generalSettingsRepository,
    jishoHelper = JishoHelper(
        networkClientProvider = networkClientProvider,
        timber = timber
    ),
    languagesRepository = languagesRepository,
    locationsRepository = LocationsRepository(
        timeZoneRepository = timeZoneRepository
    ),
    modifyUserDataHelper = ModifyUserDataHelper(
        timber = timber
    ),
    pokepediaRepository = pokepediaRepository,
    shinyTriviaOccurencesRepository = shinyTriviaOccurencesRepository,
    starWarsQuotesRepository = StarWarsQuotesRepository(),
    timber = timber,
    translationHelper = translationHelper,
    triviaBanHelper = triviaBanHelper,
    triviaEmoteGenerator = triviaEmoteGenerator,
    triviaGameControllersRepository = triviaGameControllersRepository,
    triviaGameGlobalControllersRepository = triviaGameGlobalControllersRepository,
    triviaGameMachine = TriviaGameMachine(
        eventLoop = eventLoop,
        cutenessRepository = cutenessRepository,
        queuedTriviaGameStore = QueuedTriviaGameStore(
            timber = timber,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        shinyTriviaHelper = shinyTriviaHelper,
        superTriviaCooldownHelper = SuperTriviaCooldownHelper(
            triviaSettingsRepository = triviaSettingsRepository
        ),
        timber = timber,
        triviaAnswerChecker = TriviaAnswerChecker(
            timber = timber,
            triviaAnswerCompiler = triviaAnswerCompiler,
            triviaSettingsRepository = triviaSettingsRepository
        ),
        triviaGameStore = TriviaGameStore(),
        triviaRepository = triviaRepository,
        triviaScoreRepository = triviaScoreRepository
    ),
    triviaHistoryRepository = triviaHistoryRepository,
    triviaScoreRepository = triviaScoreRepository,
    triviaSettingsRepository = triviaSettingsRepository,
    triviaUtils = triviaUtils,
    twitchTokensRepository = twitchTokensRepository,
    twitchUtils = TwitchUtils(
        eventLoop = eventLoop,
        timber = timber
    ),
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository,
    weatherRepository = weatherRepository,
    wordOfTheDayRepository = WordOfTheDayRepository(
        networkClientProvider = networkClientProvider,
        timber = timber
    )
)


#########################################
## Section for starting the actual bot ##
#########################################

timber.log('initCynanBot', 'Starting CynanBot...')
cynanBot.run()
