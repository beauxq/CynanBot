from datetime import datetime

from CynanBot.location.timeZoneRepository import TimeZoneRepository
from CynanBot.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from CynanBot.twitch.api.websocket.twitchWebsocketCondition import \
    TwitchWebsocketCondition
from CynanBot.twitch.api.websocket.twitchWebsocketConnectionStatus import \
    TwitchWebsocketConnectionStatus
from CynanBot.twitch.api.websocket.twitchWebsocketEvent import \
    TwitchWebsocketEvent
from CynanBot.twitch.api.websocket.twitchWebsocketPayload import \
    TwitchWebsocketPayload
from CynanBot.twitch.api.websocket.twitchWebsocketSession import \
    TwitchWebsocketSession
from CynanBot.twitch.api.websocket.twitchWebsocketSubscription import \
    TwitchWebsocketSubscription
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from CynanBot.twitch.api.websocket.twitchWebsocketTransport import \
    TwitchWebsocketTransport


class TestTwitchWebsocketPayload():

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    def __createEvent(self) -> TwitchWebsocketEvent:
        return TwitchWebsocketEvent()

    def __createSession(self) -> TwitchWebsocketSession:
        connectedAt = datetime.now(self.timeZoneRepository.getDefault())

        return TwitchWebsocketSession(
            keepAliveTimeoutSeconds = 100,
            connectedAt = connectedAt,
            reconnectUrl = None,
            sessionId = 'abc123',
            status = TwitchWebsocketConnectionStatus.CONNECTED
        )

    def __createSubscription(self) -> TwitchWebsocketSubscription:
        createdAt = datetime.now(self.timeZoneRepository.getDefault())

        return TwitchWebsocketSubscription(
            cost = 100,
            createdAt = createdAt,
            subscriptionId = 'qwerty',
            version = '1',
            condition = TwitchWebsocketCondition(),
            status = TwitchWebsocketConnectionStatus.CONNECTED,
            subscriptionType = TwitchWebsocketSubscriptionType.CHEER,
            transport = TwitchWebsocketTransport()
        )

    def test_isEmpty_withDefaultConstructor(self):
        payload = TwitchWebsocketPayload()
        assert payload.isEmpty() is True

    def test_isEmpty_withEvent(self):
        payload = TwitchWebsocketPayload(event = self.__createEvent())
        assert payload.isEmpty() is False

    def test_isEmpty_withSession(self):
        payload = TwitchWebsocketPayload(session = self.__createSession())
        assert payload.isEmpty() is False

    def test_isEmpty_withSubscription(self):
        payload = TwitchWebsocketPayload(subscription = self.__createSubscription())
        assert payload.isEmpty() is False
