import math

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.builder.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBot.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.tts.ttsSubscriptionDonation import TtsSubscriptionDonation
from CynanBot.tts.ttsSubscriptionDonationGiftType import \
    TtsSubscriptionDonationGiftType
from CynanBot.twitch.absTwitchSubscriptionHandler import \
    AbsTwitchSubscriptionHandler
from CynanBot.twitch.api.twitchCommunitySubGift import TwitchCommunitySubGift
from CynanBot.twitch.api.twitchResub import TwitchResub
from CynanBot.twitch.api.twitchSubGift import TwitchSubGift
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier
from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.twitch.twitchTokensUtilsInterface import \
    TwitchTokensUtilsInterface
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface


class TwitchSubscriptionHandler(AbsTwitchSubscriptionHandler):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface | None,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None,
        twitchChannelProvider: TwitchChannelProvider,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if streamAlertsManager is not None and not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameBuilder is not None and not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif triviaGameMachine is not None and not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise TypeError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface | None = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: TriviaGameBuilderInterface | None = triviaGameBuilder
        self.__triviaGameMachine: TriviaGameMachineInterface | None = triviaGameMachine
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider
        self.__twitchTokensUtils: TwitchTokensUtilsInterface = twitchTokensUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def __isRedundantSubscriptionAlert(
        self,
        isGift: bool | None,
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> bool:
        # This method intends to prevent an annoying situation where some subscription events end
        # up causing two distinct subscription event alerts to come from Twitch, where both are
        # just subtly different yet each inform of the same new subscriber/subscription event.

        if isGift is False and subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE or \
                isGift is None and subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE or \
                isGift is None and subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT:
            return True

        return False

    async def onNewSubscription(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        payload = dataBundle.requirePayload()
        event = payload.event
        subscription = payload.subscription

        if event is None or subscription is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that has no event (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        subscriptionType = subscription.subscriptionType
        isAnonymous = event.isAnonymous
        isGift = event.isGift
        communitySubGift = event.communitySubGift
        message = event.message
        broadcasterUserId = event.broadcasterUserId
        eventId = event.eventId
        resub = event.resub
        subGift = event.subGift
        eventUserId = event.userId
        eventUserInput = event.userInput
        eventUserLogin = event.userLogin
        eventUserName = event.userName
        tier = event.tier

        if not utils.isValidStr(broadcasterUserId) or tier is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({subscriptionType=}) ({isAnonymous=}) ({isGift=}) ({communitySubGift=}) ({resub=}) ({subGift=}) ({message=}) ({broadcasterUserId=}) ({eventId=}) ({eventUserId=}) ({eventUserInput=}) ({eventUserLogin=}) ({eventUserName=}) ({tier=})')
            return

        self.__timber.log('TwitchSubscriptionHandler', f'Received a subscription event: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({subscriptionType=}) ({isAnonymous=}) ({isGift=}) ({communitySubGift=}) ({resub=}) ({subGift=}) ({message=}) ({broadcasterUserId=}) ({eventId=}) ({eventUserId=}) ({eventUserInput=}) ({eventUserLogin=}) ({eventUserName=}) ({tier=})')

        if user.isSuperTriviaGameEnabled():
            await self.__processSuperTriviaEvent(
                broadcasterUserId = broadcasterUserId,
                communitySubGift = communitySubGift,
                tier = tier,
                subscriptionType = subscriptionType,
                user = user
            )

        if user.isTtsEnabled():
            await self.__processTtsEvent(
                isAnonymous = isAnonymous,
                isGift = isGift,
                broadcasterUserId = broadcasterUserId,
                message = message,
                userId = eventUserId,
                userInput = eventUserInput,
                userLogin = eventUserLogin,
                userName = eventUserName,
                communitySubGift = communitySubGift,
                resub = resub,
                subGift = subGift,
                tier = tier,
                subscriptionType = subscriptionType,
                user = user
            )

    async def __processSuperTriviaEvent(
        self,
        broadcasterUserId: str,
        communitySubGift: TwitchCommunitySubGift | None,
        tier: TwitchSubscriberTier,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface
    ):
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif communitySubGift is not None and not isinstance(communitySubGift, TwitchCommunitySubGift):
            raise TypeError(f'communitySubGift argument is malformed: \"{communitySubGift}\"')
        elif not isinstance(tier, TwitchSubscriberTier):
            raise TypeError(f'tier argument is malformed: \"{tier}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        triviaGameBuilder = self.__triviaGameBuilder
        triviaGameMachine = self.__triviaGameMachine

        if triviaGameBuilder is None or triviaGameMachine is None:
            return
        elif not user.isSuperTriviaGameEnabled():
            return
        elif subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIBE:
            return

        superTriviaSubscribeTriggerAmount = user.getSuperTriviaSubscribeTriggerAmount()
        if not utils.isValidNum(superTriviaSubscribeTriggerAmount) or superTriviaSubscribeTriggerAmount <= 0:
            return

        numberOfSubs = 1
        if communitySubGift is not None:
            numberOfSubs = communitySubGift.total

        numberOfGames = int(math.floor(numberOfSubs / superTriviaSubscribeTriggerAmount))
        if numberOfGames < 1:
            return

        action = await triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.getHandle(),
            twitchChannelId = broadcasterUserId,
            numberOfGames = numberOfGames
        )

        if action is not None:
            triviaGameMachine.submitAction(action)

    async def __processTtsEvent(
        self,
        isAnonymous: bool | None,
        isGift: bool | None,
        broadcasterUserId: str,
        message: str | None,
        userId: str | None,
        userInput: str | None,
        userLogin: str | None,
        userName: str | None,
        communitySubGift: TwitchCommunitySubGift | None,
        resub: TwitchResub | None,
        subGift: TwitchSubGift | None,
        tier: TwitchSubscriberTier,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface,
    ):
        if isAnonymous is not None and not utils.isValidBool(isAnonymous):
            raise TypeError(f'isAnonymous argument is malformed: \"{isAnonymous}\"')
        elif isGift is not None and not utils.isValidBool(isGift):
            raise TypeError(f'isGift argument is malformed: \"{isGift}\"')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif userId is not None and not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif userInput is not None and not isinstance(userInput, str):
            raise TypeError(f'userInput argument is malformed: \"{userInput}\"')
        elif userLogin is not None and not utils.isValidStr(userLogin):
            raise TypeError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif userName is not None and not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif communitySubGift is not None and not isinstance(communitySubGift, TwitchCommunitySubGift):
            raise TypeError(f'communitySubGift argument is malformed: \"{communitySubGift}\"')
        elif resub is not None and not isinstance(resub, TwitchResub):
            raise TypeError(f'resub argument is malformed: \"{resub}\"')
        elif subGift is not None and not isinstance(subGift, TwitchSubGift):
            raise TypeError(f'subGift argument is malformed: \"{subGift}\"')
        elif not isinstance(tier, TwitchSubscriberTier):
            raise TypeError(f'tier argument is malformed: \"{tier}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        streamAlertsManager = self.__streamAlertsManager

        if streamAlertsManager is None:
            return
        elif not user.isTtsEnabled():
            return
        elif await self.__isRedundantSubscriptionAlert(
            isGift = isGift,
            subscriptionType = subscriptionType
        ):
            self.__timber.log('TwitchSubscriptionHandler', f'Encountered redundant subscription alert event ({isGift=}) ({communitySubGift=}) ({resub=}) ({subGift=}) ({subscriptionType=}) ({user=})')
            return

        actualMessage = message
        if not utils.isValidStr(actualMessage):
            actualMessage = userInput

        if isAnonymous is None:
            isAnonymous = False

        actualUserId = userId
        actualUserName = userName

        if not utils.isValidStr(actualUserId) or not utils.isValidStr(actualUserName):
            if isAnonymous:
                twitchAccessToken = await self.__twitchTokensUtils.requireAccessTokenByIdOrFallback(
                    twitchChannelId = broadcasterUserId
                )

                actualUserId = await self.__userIdsRepository.requireAnonymousUserId()

                actualUserName = await self.__userIdsRepository.requireAnonymousUserName(
                    twitchAccessToken = twitchAccessToken
                )
            else:
                self.__timber.log('TwitchSubscriptionHandler', f'Attempted to process subscription event into a TTS message, but data is weird? ({isAnonymous=}) ({isGift=}) ({userId=}) ({userName=}) ({communitySubGift=}) ({subscriptionType=})')
                return

        giftType: TtsSubscriptionDonationGiftType | None = None

        if isGift is True:
            giftType = TtsSubscriptionDonationGiftType.RECEIVER
        elif subscriptionType is TwitchWebsocketSubscriptionType.SUBSCRIPTION_GIFT:
            giftType = TtsSubscriptionDonationGiftType.GIVER

        donation: TtsDonation = TtsSubscriptionDonation(
            isAnonymous = isAnonymous,
            giftType = giftType,
            tier = tier
        )

        ttsEvent = TtsEvent(
            message = actualMessage,
            twitchChannel = user.getHandle(),
            twitchChannelId = broadcasterUserId,
            userId = actualUserId,
            userName = actualUserName,
            donation = donation,
            provider = TtsProvider.DEC_TALK,
            raidInfo = None
        )

        streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.SUBSCRIBE,
            twitchChannel = user.getHandle(),
            twitchChannelId = broadcasterUserId,
            ttsEvent = ttsEvent
        ))
