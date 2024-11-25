from .websocketEventTypeMapperInterface import WebsocketEventTypeMapperInterface
from ..websocketEventType import WebsocketEventType


class WebsocketEventTypeMapper(WebsocketEventTypeMapperInterface):

    def toString(self, eventType: WebsocketEventType) -> str:
        if not isinstance(eventType, WebsocketEventType):
            raise TypeError(f'eventType argument is malformed: \"{eventType}\"')

        match eventType:
            case WebsocketEventType.CHANNEL_PREDICTION: return 'channelPrediction'
            case _: raise RuntimeError(f'unknown WebsocketEventType value: \"{eventType}\"')
