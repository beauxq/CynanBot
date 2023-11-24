import math
from typing import Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.trivia.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBotCommon.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBotCommon.tts.ttsDonation import TtsDonation
from CynanBotCommon.tts.ttsEvent import TtsEvent
from CynanBotCommon.tts.ttsManagerInterface import TtsManagerInterface
from CynanBotCommon.tts.ttsSubscriptionDonation import TtsSubscriptionDonation
from CynanBotCommon.twitch.twitchSubscriberTier import TwitchSubscriberTier
from CynanBotCommon.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBotCommon.twitch.websocket.websocketDataBundle import \
    WebsocketDataBundle
from CynanBotCommon.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBotCommon.users.userInterface import UserInterface
from twitch.absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from twitch.twitchChannelProvider import TwitchChannelProvider


class TwitchSubscriptionHandler(AbsTwitchSubscriptionHandler):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        triviaGameBuilder: Optional[TriviaGameBuilderInterface],
        triviaGameMachine: Optional[TriviaGameMachineInterface],
        ttsManager: Optional[TtsManagerInterface],
        twitchChannelProvider: TwitchChannelProvider,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaGameBuilder is not None and not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise ValueError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif triviaGameMachine is not None and not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif ttsManager is not None and not isinstance(ttsManager, TtsManagerInterface):
            raise ValueError(f'ttsManager argument is malformed: \"{ttsManager}\"')
        elif not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise ValueError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: Optional[TriviaGameBuilderInterface] = triviaGameBuilder
        self.__triviaGameMachine: Optional[TriviaGameMachineInterface] = triviaGameMachine
        self.__ttsManager: Optional[TtsManagerInterface] = ttsManager
        self.__twitchChannelProvider: TwitchChannelProvider = twitchChannelProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def __getTwitchAccessToken(self, user: UserInterface) -> Optional[str]:
        if not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        if await self.__twitchTokensRepository.hasAccessToken(user.getHandle()):
            await self.__twitchTokensRepository.validateAndRefreshAccessToken(user.getHandle())
            return await self.__twitchTokensRepository.getAccessToken(user.getHandle())
        else:
            administratorUserName = await self.__administratorProvider.getAdministratorUserName()
            await self.__twitchTokensRepository.validateAndRefreshAccessToken(administratorUserName)
            return await self.__twitchTokensRepository.getAccessToken(administratorUserName)

    async def onNewSubscription(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, WebsocketDataBundle):
            raise ValueError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.getPayload().getEvent()

        if event is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that has no event: (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        isAnonymous = event.isAnonymous()
        isGift = event.isGift()
        communitySubTotal = event.getCommunitySubTotal()
        total = event.getTotal()
        message = event.getMessage()
        userId = event.getUserId()
        userInput = event.getUserInput()
        userLogin = event.getUserLogin()
        userName = event.getUserName()
        tier = event.getTier()

        if tier is None:
            self.__timber.log('TwitchSubscriptionHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({isAnonymous=}) ({isGift=}) ({communitySubTotal=}) ({total=}) ({message=}) ({userId=}) ({userInput=}) ({userLogin=}) ({userName=}) ({tier=})')
            return

        self.__timber.log('TwitchSubscriptionHandler', f'Received a subscription event: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({isAnonymous=}) ({isGift=}) ({communitySubTotal=}) ({total=}) ({message=}) ({userId=}) ({userInput=}) ({userLogin=}) ({userName=}) ({tier=})')

        if user.isSuperTriviaGameEnabled():
            await self.__processSuperTriviaEvent(
                communitySubTotal = communitySubTotal,
                total = total,
                tier = tier,
                user = user
            )

        if user.isTtsEnabled():
            await self.__processTtsEvent(
                isAnonymous = isAnonymous,
                isGift = isGift,
                message = message,
                userId = userId,
                userLogin = userLogin,
                userName = userName,
                userInput = userInput,
                tier = tier,
                user = user
            )

    async def __processSuperTriviaEvent(
        self,
        communitySubTotal: Optional[int],
        total: Optional[int],
        tier: TwitchSubscriberTier,
        user: UserInterface
    ):
        if communitySubTotal is not None and not utils.isValidInt(communitySubTotal):
            raise ValueError(f'communitySubTotal argument is malformed: \"{communitySubTotal}\"')
        elif communitySubTotal is not None and (communitySubTotal < 0 or communitySubTotal > utils.getIntMaxSafeSize()):
            raise ValueError(f'communitySubTotal argument is out of bounds: {communitySubTotal}')
        elif total is not None and not utils.isValidInt(total):
            raise ValueError(f'total argument is malformed: \"{total}\"')
        elif total is not None and (total < 1 or total > utils.getIntMaxSafeSize()):
            raise ValueError(f'total argument is out of bounds: {total}')
        elif not isinstance(tier, TwitchSubscriberTier):
            raise ValueError(f'tier argument is malformed: \"{tier}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        if self.__triviaGameBuilder is None or self.__triviaGameMachine is None:
            return
        elif not user.isSuperTriviaGameEnabled():
            return
        elif not user.hasSuperTriviaGameShinyMultiplier() or user.getSuperTriviaSubscribeTriggerAmount() <= 0:
            return
        elif (communitySubTotal is None or communitySubTotal < 1) and (total is None or total < 1):
            return

        numberOfSubs = total
        if communitySubTotal is not None:
            numberOfSubs = communitySubTotal

        if not utils.isValidInt(numberOfSubs) or numberOfSubs < 1:
            return

        numberOfGames = math.floor(numberOfSubs / user.getSuperTriviaSubscribeTriggerAmount())

        if numberOfGames < 1:
            return

        action = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.getHandle(),
            numberOfGames = numberOfGames
        )

        if action is not None:
            self.__triviaGameMachine.submitAction(action)

    async def __processTtsEvent(
        self,
        isAnonymous: Optional[bool],
        isGift: Optional[bool],
        message: Optional[str],
        userId: Optional[str],
        userInput: Optional[str],
        userLogin: Optional[str],
        userName: Optional[str],
        tier: TwitchSubscriberTier,
        user: UserInterface
    ):
        if isAnonymous is not None and not utils.isValidBool(isAnonymous):
            raise ValueError(f'isAnonymous argument is malformed: \"{isAnonymous}\"')
        elif isGift is not None and not utils.isValidBool(isGift):
            raise ValueError(f'isGift argument is malformed: \"{isGift}\"')
        elif message is not None and not isinstance(message, str):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif userId is not None and not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userInput is not None and not isinstance(userInput, str):
            raise ValueError(f'userInput argument is malformed: \"{userInput}\"')
        elif userLogin is not None and not utils.isValidStr(userLogin):
            raise ValueError(f'userLogin argument is malformed: \"{userLogin}\"')
        elif userName is not None and not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif not isinstance(tier, TwitchSubscriberTier):
            raise ValueError(f'tier argument is malformed: \"{tier}\"')
        elif not isinstance(user, UserInterface):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        if self.__ttsManager is None:
            return
        elif not user.isTtsEnabled():
            return

        actualMessage = message
        if not utils.isValidStr(actualMessage):
            actualMessage = userInput

        if isAnonymous is None:
            isAnonymous = False

        if isGift is None:
            isGift = False

        actualUserId = userId
        actualUserName = userName
        if not utils.isValidStr(actualUserId) or not utils.isValidStr(userName):
            if isAnonymous:
                actualUserId = await self.__userIdsRepository.fetchAnonymousUserId()
                actualUserName = await self.__userIdsRepository.fetchAnonymousUserName(
                    twitchAccessToken = await self.__getTwitchAccessToken(user)
                )
            else:
                self.__timber.log('TwitchSubscriptionHandler', f'Attempted to process subscription event into a TTS message, but data is weird? ({isAnonymous=}) ({userId=}) ({userName=})')
                return

        donation: TtsDonation = TtsSubscriptionDonation(
            isAnonymous = isAnonymous,
            isGift = isGift,
            tier = tier
        )

        self.__ttsManager.submitTtsEvent(TtsEvent(
            message = actualMessage,
            twitchChannel = user.getHandle(),
            userId = actualUserId,
            userName = actualUserName,
            donation = donation,
            raidInfo = None
        ))