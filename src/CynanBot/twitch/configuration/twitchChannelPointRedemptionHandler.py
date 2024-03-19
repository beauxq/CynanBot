import CynanBot.misc.utils as utils
from CynanBot.channelPointRedemptions.absChannelPointRedemption import \
    AbsChannelPointRedemption
from CynanBot.channelPointRedemptions.casualGamePollRedemption import \
    CasualGamePollRedemption
from CynanBot.channelPointRedemptions.stubChannelPointRedemption import \
    StubPointRedemption
from CynanBot.channelPointRedemptions.triviaGamePointRedemption import \
    TriviaGamePointRedemption
from CynanBot.pointRedemptions import (CutenessRedemption,
                                       PkmnBattleRedemption,
                                       PkmnCatchRedemption,
                                       PkmnEvolveRedemption,
                                       PkmnShinyRedemption,
                                       SuperTriviaGameRedemption)
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.absTwitchChannelPointRedemptionHandler import \
    AbsTwitchChannelPointRedemptionHandler
from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.twitch.configuration.twitchChannelPointsMessage import \
    TwitchChannelPointsMessage
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface


class TwitchChannelPointRedemptionHandler(AbsTwitchChannelPointRedemptionHandler):

    def __init__(
        self,
        casualGamePollRedemption: AbsChannelPointRedemption,
        cutenessRedemption: AbsChannelPointRedemption,
        pkmnBattleRedemption: AbsChannelPointRedemption,
        pkmnCatchRedemption: AbsChannelPointRedemption,
        pkmnEvolveRedemption: AbsChannelPointRedemption,
        pkmnShinyRedemption: AbsChannelPointRedemption,
        superTriviaGameRedemption: AbsChannelPointRedemption,
        triviaGamePointRedemption: AbsChannelPointRedemption,
        timber: TimberInterface,
        twitchChannelProvider: TwitchChannelProvider,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(casualGamePollRedemption, CasualGamePollRedemption) and not isinstance(casualGamePollRedemption, StubPointRedemption):
            raise TypeError(f'casualGamePollRedemption argument is malformed: \"{casualGamePollRedemption}\"')
        elif not isinstance(cutenessRedemption, CutenessRedemption) and not isinstance(cutenessRedemption, StubPointRedemption):
            raise TypeError(f'cutenessRedemption argument is malformed: \"{cutenessRedemption}\"')
        elif not isinstance(pkmnBattleRedemption, PkmnBattleRedemption) and not isinstance(pkmnBattleRedemption, StubPointRedemption):
            raise TypeError(f'pkmnBattleRedemption argument is malformed: \"{pkmnBattleRedemption}\"')
        elif not isinstance(pkmnCatchRedemption, PkmnCatchRedemption) and not isinstance(pkmnCatchRedemption, StubPointRedemption):
            raise TypeError(f'pkmnCatchRedemption argument is malformed: \"{pkmnCatchRedemption}\"')
        elif not isinstance(pkmnEvolveRedemption, PkmnEvolveRedemption) and not isinstance(pkmnEvolveRedemption, StubPointRedemption):
            raise TypeError(f'pkmnEvolveRedemption argument is malformed: \"{pkmnEvolveRedemption}\"')
        elif not isinstance(pkmnShinyRedemption, PkmnShinyRedemption) and not isinstance(pkmnShinyRedemption, StubPointRedemption):
            raise TypeError(f'pkmnShinyRedemption argument is malformed: \"{pkmnShinyRedemption}\"')
        elif not isinstance(superTriviaGameRedemption, SuperTriviaGameRedemption) and not isinstance(superTriviaGameRedemption, StubPointRedemption):
            raise TypeError(f'superTriviaGameRedemption argument is malformed: \"{superTriviaGameRedemption}\"')
        elif not isinstance(triviaGamePointRedemption, TriviaGamePointRedemption) and not isinstance(triviaGamePointRedemption, StubPointRedemption):
            raise TypeError(f'triviaGamePointRedemption argument is malformed: \"{triviaGamePointRedemption}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise TypeError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__casualGamePollRedemption: AbsChannelPointRedemption = casualGamePollRedemption
        self.__cutenessRedemption: AbsChannelPointRedemption = cutenessRedemption
        self.__pkmnBattleRedemption: AbsChannelPointRedemption = pkmnBattleRedemption
        self.__pkmnCatchRedemption: AbsChannelPointRedemption = pkmnCatchRedemption
        self.__pkmnEvolveRedemption: AbsChannelPointRedemption = pkmnEvolveRedemption
        self.__pkmnShinyRedemption: AbsChannelPointRedemption = pkmnShinyRedemption
        self.__superTriviaGameRedemption: AbsChannelPointRedemption = superTriviaGameRedemption
        self.__triviaGamePointRedemption: AbsChannelPointRedemption = triviaGamePointRedemption
        self.__timber: TimberInterface = timber
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def onNewChannelPointRedemption(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise ValueError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().getEvent()

        if event is None:
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that has no event: \"{dataBundle}\"')
            return

        eventId = dataBundle.getMetadata().getMessageId()
        reward = event.getReward()
        redemptionUserId = event.getUserId()
        redemptionUserInput = event.getUserInput()
        redemptionUserLogin = event.getUserLogin()

        if not utils.isValidStr(eventId) or reward is None or not utils.isValidStr(redemptionUserId) or not utils.isValidStr(redemptionUserLogin):
            self.__timber.log('TwitchChannelPointRedemptionHandler', f'Received a data bundle that is missing crucial data: ({eventId=}) ({reward=}) ({redemptionUserId=}) ({redemptionUserInput=}) ({redemptionUserLogin=})')
            return

        self.__timber.log('TwitchChannelPointRedemptionHandler', f'Channel point reward ({reward}) redeemed by {redemptionUserLogin}:{redemptionUserId} in {user.getHandle()}:{userId} ({redemptionUserInput=})')

        await self.__userIdsRepository.setUser(
            userId = redemptionUserId,
            userName = redemptionUserLogin
        )

        twitchChannel = await self.__twitchChannelProvider.getTwitchChannel(user.getHandle())

        channelPointsMessage = TwitchChannelPointsMessage(
            eventId = eventId,
            redemptionMessage = redemptionUserInput,
            rewardId = reward.getRewardId(),
            twitchUser = user,
            userId = redemptionUserId,
            userName = redemptionUserLogin
        )

        if user.isCasualGamePollEnabled() and channelPointsMessage.getRewardId() == user.getCasualGamePollRewardId():
            if await self.__casualGamePollRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isCutenessEnabled() and user.hasCutenessBoosterPacks():
            if await self.__cutenessRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isPkmnEnabled():
            if channelPointsMessage.getRewardId() == user.getPkmnBattleRewardId():
                if await self.__pkmnBattleRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if user.hasPkmnCatchBoosterPacks():
                if await self.__pkmnCatchRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if channelPointsMessage.getRewardId() == user.getPkmnEvolveRewardId():
                if await self.__pkmnEvolveRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

            if channelPointsMessage.getRewardId() == user.getPkmnShinyRewardId():
                if await self.__pkmnShinyRedemption.handlePointRedemption(
                    twitchChannel = twitchChannel,
                    twitchChannelPointsMessage = channelPointsMessage
                ):
                    return

        if user.isTriviaGameEnabled() and channelPointsMessage.getRewardId() == user.getTriviaGameRewardId():
            if await self.__triviaGamePointRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return

        if user.isSuperTriviaGameEnabled() and channelPointsMessage.getRewardId() == user.getSuperTriviaGameRewardId():
            if await self.__superTriviaGameRedemption.handlePointRedemption(
                twitchChannel = twitchChannel,
                twitchChannelPointsMessage = channelPointsMessage
            ):
                return
