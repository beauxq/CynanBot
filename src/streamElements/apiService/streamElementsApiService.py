import traceback

from .streamElementsApiServiceInterface import StreamElementsApiServiceInterface
from ..models.streamElementsVoice import StreamElementsVoice
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class StreamElementsApiService(StreamElementsApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber

    async def getSpeech(
        self,
        text: str,
        userKey: str,
        voice: StreamElementsVoice
    ) -> bytes:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        elif not utils.isValidStr(userKey):
            raise TypeError(f'userKey argument is malformed: \"{userKey}\"')
        elif not isinstance(voice, StreamElementsVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        clientSession = await self.__networkClientProvider.get()

        try:
            response = await clientSession.get(
                url = f'https://api.streamelements.com/kappa/v2/speech?voice={voice.urlValue}&text={text}&key={userKey}'
            )
        except GenericNetworkException as e:
            self.__timber.log('StreamElementsApiService', f'Encountered network error when fetching speech ({voice=}) ({text=}) ({userKey=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'StreamElementsApiService encountered network error when fetching speech ({voice=}) ({text=}) ({userKey=}): {e}')

        responseStatusCode = response.statusCode
        speechBytes = await response.read()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('StreamElementsApiService', f'Encountered non-200 HTTP status code when fetching speech ({voice=}) ({text=}) ({userKey=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(f'StreamElementsApiService encountered non-200 HTTP status code when fetching speech ({voice=}) ({text=}) ({userKey=}) ({response=}) ({responseStatusCode=})')
        elif speechBytes is None:
            self.__timber.log('StreamElementsApiService', f'Unable to fetch speech bytes ({voice=}) ({text=}) ({userKey=}) ({response=}) ({responseStatusCode=})')
            raise GenericNetworkException(f'StreamElementsApiService unable to fetch speech bytes ({voice=}) ({text=}) ({userKey=}) ({response=}) ({responseStatusCode=})')

        return speechBytes
