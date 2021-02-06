import locale

from authHelper import AuthHelper
from cutenessRepository import CutenessRepository
from cynanBot import CynanBot
from CynanBotCommon.analogueStoreRepository import AnalogueStoreRepository
from CynanBotCommon.backingDatabase import BackingDatabase
from CynanBotCommon.jishoHelper import JishoHelper
from CynanBotCommon.jokesRepository import JokesRepository
from CynanBotCommon.nonceRepository import NonceRepository
from CynanBotCommon.timeZoneRepository import TimeZoneRepository
from CynanBotCommon.wordOfTheDayRepository import WordOfTheDayRepository
from locationsRepository import LocationsRepository
from userIdsRepository import UserIdsRepository
from usersRepository import UsersRepository
from userTokensRepository import UserTokensRepository
from weatherRepository import WeatherRepository


locale.setlocale(locale.LC_ALL, 'en_US.utf8')

analogueStoreRepository = AnalogueStoreRepository()
nonceRepository = NonceRepository()
authHelper = AuthHelper(nonceRepository=nonceRepository)
backingDatabase = BackingDatabase()
jishoHelper = JishoHelper()
JokesRepository = JokesRepository()
userIdsRepository = UserIdsRepository(
    backingDatabase=backingDatabase
)
cutenessRepository = CutenessRepository(
    backingDatabase=backingDatabase,
    leaderboardSize=10,
    localLeaderboardSize=5,
    userIdsRepository=userIdsRepository
)
timeZoneRepository = TimeZoneRepository()
locationsRepository = LocationsRepository(
    timeZoneRepository=timeZoneRepository
)
usersRepository = UsersRepository(
    timeZoneRepository=timeZoneRepository
)
userTokensRepository = UserTokensRepository()
weatherRepository = WeatherRepository(
    iqAirApiKey=authHelper.getIqAirApiKey(),
    oneWeatherApiKey=authHelper.getOneWeatherApiKey()
)
wordOfTheDayRepository = WordOfTheDayRepository()

cynanBot = CynanBot(
    analogueStoreRepository=analogueStoreRepository,
    authHelper=authHelper,
    cutenessRepository=cutenessRepository,
    jishoHelper=jishoHelper,
    jokesRepository=JokesRepository,
    locationsRepository=locationsRepository,
    nonceRepository=nonceRepository,
    userIdsRepository=userIdsRepository,
    usersRepository=usersRepository,
    userTokensRepository=userTokensRepository,
    weatherRepository=weatherRepository,
    wordOfTheDayRepository=wordOfTheDayRepository
)

print('Starting CynanBot...')
cynanBot.run()
