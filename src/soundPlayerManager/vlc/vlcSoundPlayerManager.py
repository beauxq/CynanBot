import asyncio
import traceback
from typing import Collection

import aiofiles.ospath
from frozenlist import FrozenList

from .vlcMediaPlayer import VlcMediaPlayer
from ..soundAlert import SoundAlert
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface
from ..soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ...chatBand.chatBandInstrument import ChatBandInstrument
from ...chatBand.chatBandInstrumentSoundsRepositoryInterface import ChatBandInstrumentSoundsRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class VlcSoundPlayerManager(SoundPlayerManagerInterface):

    def __init__(
        self,
        chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface | None,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        timber: TimberInterface,
        playbackLoopSleepTimeSeconds: float = 0.25
    ):
        if chatBandInstrumentSoundsRepository is not None and not isinstance(chatBandInstrumentSoundsRepository, ChatBandInstrumentSoundsRepositoryInterface):
            raise TypeError(f'chatBandInstrumentSoundsRepository argument is malformed: \"{chatBandInstrumentSoundsRepository}\"')
        elif not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidNum(playbackLoopSleepTimeSeconds):
            raise TypeError(f'playbackLoopSleepTimeSeconds argument is malformed: \"{playbackLoopSleepTimeSeconds}\"')
        elif playbackLoopSleepTimeSeconds < 0.25 or playbackLoopSleepTimeSeconds > 1:
            raise ValueError(f'playbackLoopSleepTimeSeconds argument is out of bounds: {playbackLoopSleepTimeSeconds}')

        self.__chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface | None = chatBandInstrumentSoundsRepository
        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__timber: TimberInterface = timber
        self.__playbackLoopSleepTimeSeconds: float = playbackLoopSleepTimeSeconds

        self.__isProgressingThroughPlaylist: bool = False
        self.__mediaPlayer: VlcMediaPlayer | None = None

    @property
    def isPlaying(self) -> bool:
        if self.__isProgressingThroughPlaylist:
            return True

        mediaPlayer = self.__mediaPlayer
        return mediaPlayer is not None and mediaPlayer.isPlaying

    async def playChatBandInstrument(
        self,
        instrument: ChatBandInstrument,
        volume: int | None = None
    ) -> bool:
        if not isinstance(instrument, ChatBandInstrument):
            raise TypeError(f'instrument argument is malformed: \"{instrument}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')

        chatBandInstrumentSoundsRepository = self.__chatBandInstrumentSoundsRepository

        if chatBandInstrumentSoundsRepository is None:
            self.__timber.log('VlcSoundPlayerManager', f'The ChatBandInstrumentSoundsRepository is not available in order to play the given chat band instrument ({instrument=})')
            return False
        elif not await self.__soundPlayerSettingsRepository.isEnabled():
            return False
        elif self.isPlaying:
            self.__timber.log('VlcSoundPlayerManager', f'There is already an ongoing sound!')
            return False

        filePath = await chatBandInstrumentSoundsRepository.getRandomSound(instrument)

        if not utils.isValidStr(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'No file path available for chat band instrument ({instrument=}) ({filePath=})')
            return False

        filePaths: FrozenList[str] = FrozenList()
        filePaths.append(filePath)
        filePaths.freeze()

        return await self.playPlaylist(
            filePaths = filePaths,
            volume = volume
        )

    async def playPlaylist(
        self,
        filePaths: Collection[str],
        volume: int | None = None
    ) -> bool:
        if not isinstance(filePaths, Collection):
            raise TypeError(f'filePaths argument is malformed: \"{filePaths}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')

        frozenFilePaths: FrozenList[str] = FrozenList(filePaths)
        frozenFilePaths.freeze()

        if len(frozenFilePaths) == 0:
            self.__timber.log('VlcSoundPlayerManager', f'filePaths argument has no elements: \"{filePaths}\"')
            return False

        for index, filePath in enumerate(frozenFilePaths):
            if not utils.isValidStr(filePath):
                self.__timber.log('VlcSoundPlayerManager', f'The given file path at index {index} is not a valid string: \"{filePath}\"')
                return False
            elif not await aiofiles.ospath.exists(filePath):
                self.__timber.log('VlcSoundPlayerManager', f'The given file path at index {index} does not exist: \"{filePath}\"')
                return False
            elif not await aiofiles.ospath.isfile(filePath):
                self.__timber.log('VlcSoundPlayerManager', f'The given file path at index {index} is not a file: \"{filePath}\"')
                return False

        if not utils.isValidInt(volume):
            volume = await self.__soundPlayerSettingsRepository.getMediaPlayerVolume()

        mediaPlayer = await self.__retrieveMediaPlayer()

        await self.__progressThroughPlaylist(
            playlistFilePaths = frozenFilePaths,
            volume = volume,
            mediaPlayer = mediaPlayer
        )

        return True

    async def playSoundAlert(
        self,
        alert: SoundAlert,
        volume: int | None = None
    ) -> bool:
        if not isinstance(alert, SoundAlert):
            raise TypeError(f'alert argument is malformed: \"{alert}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')

        if not await self.__soundPlayerSettingsRepository.isEnabled():
            return False
        elif self.isPlaying:
            self.__timber.log('VlcSoundPlayerManager', f'There is already an ongoing sound!')
            return False

        filePath = await self.__soundPlayerSettingsRepository.getFilePathFor(alert)

        if not utils.isValidStr(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'No file path available for sound alert ({alert=}) ({filePath=})')
            return False

        return await self.playSoundFile(
            filePath = filePath,
            volume = volume
        )

    async def playSoundFile(
        self,
        filePath: str | None,
        volume: int | None = None
    ) -> bool:
        if filePath is not None and not isinstance(filePath, str):
            raise TypeError(f'filePath argument is malformed: \"{filePath}\"')
        elif volume is not None and not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')
        elif volume is not None and (volume < 0 or volume > 100):
            raise ValueError(f'volume argument is out of bounds: {volume}')

        if not utils.isValidStr(filePath):
            self.__timber.log('VlcSoundPlayerManager', f'The given file path is not a valid string: \"{filePath}\"')
            return False
        elif not await self.__soundPlayerSettingsRepository.isEnabled():
            return False
        elif self.isPlaying:
            self.__timber.log('VlcSoundPlayerManager', f'There is already an ongoing sound!')
            return False

        filePaths: FrozenList[str] = FrozenList()
        filePaths.append(filePath)
        filePaths.freeze()

        return await self.playPlaylist(
            filePaths = filePaths,
            volume = volume
        )

    async def __progressThroughPlaylist(
        self,
        playlistFilePaths: FrozenList[str],
        volume: int,
        mediaPlayer: VlcMediaPlayer
    ):
        if not isinstance(playlistFilePaths, FrozenList) or len(playlistFilePaths) == 0:
            raise TypeError(f'playlist argument is malformed: \"{playlistFilePaths}\"')
        elif not utils.isValidInt(volume):
            raise TypeError(f'volume argument is malformed: \"{volume}\"')
        elif volume < 0 or volume > 100:
            raise ValueError(f'volume argument is out of bounds: {volume}')
        elif not isinstance(mediaPlayer, VlcMediaPlayer):
            raise TypeError(f'mediaPlayer argument is malformed: \"{mediaPlayer}\"')

        await mediaPlayer.setVolume(volume)

        self.__isProgressingThroughPlaylist = True
        playErrorOccurred: bool = False
        currentPlaylistIndex: int = -1
        currentFilePath: str | None = None

        self.__timber.log('VlcSoundPlayerManager', f'Started playing playlist ({playlistFilePaths=}) ({volume=}) (({mediaPlayer=})')

        try:
            while not playErrorOccurred and (currentPlaylistIndex < len(playlistFilePaths) or mediaPlayer.isPlaying):
                match mediaPlayer.playbackState:
                    case VlcMediaPlayer.PlaybackState.ERROR:
                        playErrorOccurred = True

                    case VlcMediaPlayer.PlaybackState.PLAYING:
                        # intentionally empty
                        pass

                    case VlcMediaPlayer.PlaybackState.STOPPED:
                        if currentPlaylistIndex == -1:
                            currentPlaylistIndex = 0
                        else:
                            currentPlaylistIndex += 1

                        if currentPlaylistIndex < len(playlistFilePaths):
                            currentFilePath = playlistFilePaths[currentPlaylistIndex]
                            await mediaPlayer.setMedia(currentFilePath)

                            if not await mediaPlayer.play():
                                self.__timber.log('VlcSoundPlayerManager', f'Received bad playback result when attempting to play media element at playlist index ({currentPlaylistIndex=}) ({currentFilePath=}) ({playlistFilePaths=}) ({mediaPlayer=})')
                                playErrorOccurred = True

                await asyncio.sleep(self.__playbackLoopSleepTimeSeconds)
        except Exception as e:
            self.__timber.log('VlcSoundPlayerManager', f'Encountered exception when progressing through playlist ({playErrorOccurred=}) ({currentPlaylistIndex=}) ({currentFilePath=}) ({playlistFilePaths=}) ({mediaPlayer=}): {e}', e, traceback.format_exc())

    async def __retrieveMediaPlayer(self) -> VlcMediaPlayer:
        mediaPlayer = self.__mediaPlayer

        if mediaPlayer is None:
            mediaPlayer = VlcMediaPlayer(timber = self.__timber)
            self.__mediaPlayer = mediaPlayer
            self.__timber.log('VlcSoundPlayerManager', f'Created new VlcMediaPlayer instance: \"{mediaPlayer}\"')

        return mediaPlayer

    async def stop(self):
        mediaPlayer = await self.__retrieveMediaPlayer()
        await mediaPlayer.stop()
