from typing import Any

from .ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from ..models.ttsMonsterPrivateApiTtsData import TtsMonsterPrivateApiTtsData
from ..models.ttsMonsterPrivateApiTtsResponse import TtsMonsterPrivateApiTtsResponse
from ...misc import utils as utils


class TtsMonsterPrivateApiJsonMapper(TtsMonsterPrivateApiJsonMapperInterface):

    def __init__(self, provider: str = 'provider'):
        if not utils.isValidStr(provider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__provider: str = provider

    async def parseTtsData(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterPrivateApiTtsData | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        link = utils.getStrFromDict(jsonContents, 'link')

        warning: str | None = None
        if 'warning' in jsonContents and utils.isValidStr(jsonContents.get('warning', None)):
            warning = utils.getStrFromDict(jsonContents, 'warning')

        return TtsMonsterPrivateApiTtsData(
            link = link,
            warning = warning
        )

    async def parseTtsResponse(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> TtsMonsterPrivateApiTtsResponse | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        status = utils.getIntFromDict(jsonContents, 'status')

        data = await self.parseTtsData(jsonContents.get('data'))
        if data is None:
            return None

        return TtsMonsterPrivateApiTtsResponse(
            status = status,
            data = data
        )

    async def serializeGenerateTtsJsonBody(
        self,
        key: str,
        message: str,
        userId: str
    ) -> dict[str, Any]:
        if not utils.isValidStr(key):
            raise TypeError(f'key argument is malformed: \"{key}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')

        return {
            'data': {
                'ai': True,
                'details': {
                    'provider': self.__provider
                },
                'key': key,
                'message': message,
                'userId': userId
            }
        }
