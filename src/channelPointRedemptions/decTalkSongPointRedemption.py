from frozenlist import FrozenList

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..storage.jsonFileReader import JsonFileReader
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..tts.ttsEvent import TtsEvent
from ..tts.ttsProvider import TtsProvider
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage


class DecTalkSongPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')

        self.__streamAlertsManager = streamAlertsManager
        self.__timber: TimberInterface = timber

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.twitchUser
        if not twitchUser.isDecTalkSongsEnabled:
            return False

        decTalkSongBoosterPacks = twitchUser.decTalkSongBoosterPacks
        if decTalkSongBoosterPacks is None or len(decTalkSongBoosterPacks) == 0:
            return False

        decTalkSongBoosterPack = decTalkSongBoosterPacks.get(twitchChannelPointsMessage.rewardId, None)
        if decTalkSongBoosterPack is None:
            return False

        songKey = decTalkSongBoosterPack.song
        decTalkSongsRepository = JsonFileReader('decTalkSongsRepository.json').readJson()
        if decTalkSongsRepository is None:
            return False

        songData = FrozenList(decTalkSongsRepository.get(songKey, None))
        if len(songData) == 0:
            return False

        songData = ''.join(songData)

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = twitchUser.handle,
            twitchChannelId = await twitchChannel.getTwitchChannelId(),
            ttsEvent = TtsEvent(
                message = songData,
                twitchChannel = twitchUser.handle,
                twitchChannelId = await twitchChannel.getTwitchChannelId(),
                userId = twitchChannelPointsMessage.userId,
                userName = twitchChannelPointsMessage.userName,
                donation = None,
                provider = TtsProvider.SINGING_DEC_TALK,
                raidInfo = None
            )
        ))

        self.__timber.log('DecTalkSongPointRedemption', f'Redeemed decTalkSong of {songKey} for {twitchChannelPointsMessage.userName}:{twitchChannelPointsMessage.userId} in {twitchUser.handle}')
        return True
