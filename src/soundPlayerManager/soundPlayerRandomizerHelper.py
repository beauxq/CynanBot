import random
import re
from typing import Pattern

import aiofiles.os
import aiofiles.ospath

from .soundAlert import SoundAlert
from .soundPlayerRandomizerDirectoryScanResult import SoundPlayerRandomizerDirectoryScanResult
from .soundPlayerRandomizerHelperInterface import SoundPlayerRandomizerHelperInterface
from .soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ..misc import utils as utils
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ..timber.timberInterface import TimberInterface


class SoundPlayerRandomizerHelper(SoundPlayerRandomizerHelperInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface,
        pointRedemptionSoundAlerts: frozenset[SoundAlert] | None = frozenset({
            SoundAlert.POINT_REDEMPTION_01,
            SoundAlert.POINT_REDEMPTION_02,
            SoundAlert.POINT_REDEMPTION_03,
            SoundAlert.POINT_REDEMPTION_04,
            SoundAlert.POINT_REDEMPTION_05,
            SoundAlert.POINT_REDEMPTION_06,
            SoundAlert.POINT_REDEMPTION_07,
            SoundAlert.POINT_REDEMPTION_08,
            SoundAlert.POINT_REDEMPTION_09,
            SoundAlert.POINT_REDEMPTION_10,
            SoundAlert.POINT_REDEMPTION_11,
            SoundAlert.POINT_REDEMPTION_12,
            SoundAlert.POINT_REDEMPTION_13,
            SoundAlert.POINT_REDEMPTION_14,
            SoundAlert.POINT_REDEMPTION_15,
            SoundAlert.POINT_REDEMPTION_16
        })
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif pointRedemptionSoundAlerts is not None and not isinstance(pointRedemptionSoundAlerts, frozenset):
            raise TypeError(f'pointRedemptionSoundAlerts argument is malformed: \"{pointRedemptionSoundAlerts}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber
        self.__pointRedemptionSoundAlerts: frozenset[SoundAlert] | None = pointRedemptionSoundAlerts

        self.__scanResultCache: dict[str, SoundPlayerRandomizerDirectoryScanResult | None] = dict()
        self.__soundAlertCache: dict[SoundAlert, str | None] | None = None
        self.__soundFileRegEx: Pattern = re.compile(r'^\w[\w\s]*\s?(\(shiny\))?\.(mp3|ogg|wav)$', re.IGNORECASE)

    async def clearCaches(self):
        self.__scanResultCache.clear()
        self.__soundAlertCache = None
        self.__timber.log('SoundPlayerRandomizerHelper', 'Caches cleared')

    async def chooseRandomFromDirectorySoundAlert(
        self,
        directoryPath: str | None
    ) -> str | None:
        if not utils.isValidStr(directoryPath):
            return None

        directoryPath = utils.cleanPath(directoryPath)
        scanResult = self.__scanResultCache.get(directoryPath, None)

        if scanResult is None:
            scanResult = await self.__scanDirectoryForSoundFiles(directoryPath)
            self.__scanResultCache[directoryPath] = scanResult

        if len(scanResult.soundFiles) == 0 and len(scanResult.shinySoundFiles) == 0:
            return None

        if await self.__soundPlayerSettingsRepository.areShiniesEnabled():
            shinyProbability = await self.__soundPlayerSettingsRepository.getShinyProbability()

            if len(scanResult.shinySoundFiles) >= 1 and random.random() <= shinyProbability:
                return random.choice(scanResult.shinySoundFiles)

        return random.choice(scanResult.soundFiles)

    async def chooseRandomSoundAlert(self) -> SoundAlert | None:
        cache = self.__soundAlertCache

        if cache is None:
            cache = await self.__loadSoundAlertsCache()
            self.__soundAlertCache = cache

        availableSoundAlerts: list[SoundAlert] = list()

        for soundAlert, filePath in cache.items():
            if not utils.isValidStr(filePath):
                continue

            availableSoundAlerts.append(soundAlert)

        if len(availableSoundAlerts) == 0:
            return None

        return random.choice(availableSoundAlerts)

    async def __loadSoundAlertsCache(self) -> dict[SoundAlert, str | None]:
        cache: dict[SoundAlert, str | None] = dict()

        if self.__pointRedemptionSoundAlerts is not None and len(self.__pointRedemptionSoundAlerts) >= 1:
            for soundAlert in self.__pointRedemptionSoundAlerts:
                filePath = await self.__soundPlayerSettingsRepository.getFilePathFor(soundAlert)

                if not utils.isValidStr(filePath):
                    continue
                elif not await aiofiles.ospath.exists(filePath):
                    continue
                elif await aiofiles.ospath.isdir(filePath):
                    continue

                cache[soundAlert] = filePath

        self.__timber.log('SoundPlayerRandomizerHelper', f'Finished loading in {len(cache)} sound alert(s)')
        return cache

    async def __scanDirectoryForSoundFiles(
        self,
        directoryPath: str
    ) -> SoundPlayerRandomizerDirectoryScanResult:
        if not await aiofiles.ospath.exists(directoryPath):
            self.__timber.log('SoundPlayerRandomizerHelper', f'The given directory path does not exist: \"{directoryPath}\"')

            return SoundPlayerRandomizerDirectoryScanResult(
                soundFiles = list(),
                shinySoundFiles = list()
            )
        elif not await aiofiles.ospath.isdir(directoryPath):
            self.__timber.log('SoundPlayerRandomizerHelper', f'The given directory path is not a directory: \"{directoryPath}\"')

            return SoundPlayerRandomizerDirectoryScanResult(
                soundFiles = list(),
                shinySoundFiles = list()
            )

        directoryContents = await aiofiles.os.scandir(directoryPath)

        if directoryContents is None:
            self.__timber.log('SoundPlayerRandomizerHelper', f'Scanning the given directory path yielded a None directory pointer: \"{directoryPath}\"')

            return SoundPlayerRandomizerDirectoryScanResult(
                soundFiles = list(),
                shinySoundFiles = list()
            )

        soundFilesSet: set[str] = set()
        shinySoundFilesSet: set[str] = set()

        for entry in directoryContents:
            if not entry.is_file():
                continue

            soundFileMatch = self.__soundFileRegEx.fullmatch(entry.name)

            if soundFileMatch is None:
                continue

            shinyGroup: str | None = soundFileMatch.group(1)
            cleanPath = utils.cleanPath(entry.path)

            if utils.isValidStr(shinyGroup):
                shinySoundFilesSet.add(cleanPath)
            else:
                soundFilesSet.add(cleanPath)

        directoryContents.close()
        self.__timber.log('SoundPlayerRandomizerHelper', f'Scanned \"{directoryPath}\" and found {len(soundFilesSet)} sound file(s) and {len(shinySoundFilesSet)} shiny sound file(s)')

        soundFilesList: list[str] = list(soundFilesSet)
        soundFilesList.sort(key = lambda path: path.casefold())

        shinySoundFilesList: list[str] = list(shinySoundFilesSet)
        shinySoundFilesList.sort(key = lambda path: path.casefold())

        return SoundPlayerRandomizerDirectoryScanResult(
            soundFiles = soundFilesList,
            shinySoundFiles = shinySoundFilesList
        )
