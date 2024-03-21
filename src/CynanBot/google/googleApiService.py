import traceback

import CynanBot.misc.utils as utils
from CynanBot.google.exceptions import (
    GoogleCloudProjectApiKeyUnavailableException,
    GoogleCloudProjectIdUnavailableException)
from CynanBot.google.googleAccessToken import GoogleAccessToken
from CynanBot.google.googleApiAccessTokenStorageInterface import \
    GoogleApiAccessTokenStorageInterface
from CynanBot.google.googleApiServiceInterface import GoogleApiServiceInterface
from CynanBot.google.googleCloudProjectIdProviderInterface import \
    GoogleCloudProjectCredentialsProviderInterface
from CynanBot.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from CynanBot.google.googleTextSynthesisResponse import \
    GoogleTextSynthesisResponse
from CynanBot.google.googleTextSynthesizeRequest import \
    GoogleTextSynthesizeRequest
from CynanBot.google.googleTranslateTextResponse import \
    GoogleTranslateTextResponse
from CynanBot.google.googleTranslationRequest import GoogleTranslationRequest
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.timber.timberInterface import TimberInterface


class GoogleApiService(GoogleApiServiceInterface):

    def __init__(
        self,
        googleApiAccessTokenStorage: GoogleApiAccessTokenStorageInterface,
        googleJsonMapper: GoogleJsonMapperInterface,
        googleCloudProjectCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface,
        networkClientProvider: NetworkClientProvider,
        timber: TimberInterface,
        contentType: str = 'application/json; charset=utf-8'
    ):
        if not isinstance(googleApiAccessTokenStorage, GoogleApiAccessTokenStorageInterface):
            raise TypeError(f'googleApiAccessTokenStorage argument is malformed: \"{googleApiAccessTokenStorage}\"')
        elif not isinstance(googleJsonMapper, GoogleJsonMapperInterface):
            raise TypeError(f'googleJsonMapper argument is malformed: \"{googleJsonMapper}\"')
        elif not isinstance(googleCloudProjectCredentialsProvider, GoogleCloudProjectCredentialsProviderInterface):
            raise TypeError(f'googleCloudProjectCredentialsProvider argument is malformed: \"{googleCloudProjectCredentialsProvider}\"')
        elif not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(contentType):
            raise TypeError(f'contentType argument is malformed: \"{contentType}\"')

        self.__googleApiAccessTokenStorage: GoogleApiAccessTokenStorageInterface = googleApiAccessTokenStorage
        self.__googleJsonMapper: GoogleJsonMapperInterface = googleJsonMapper
        self.__googleCloudProjectCredentialsProvider: GoogleCloudProjectCredentialsProviderInterface = googleCloudProjectCredentialsProvider
        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__timber: TimberInterface = timber
        self.__contentType: str = contentType

    async def __fetchGoogleAccessToken(self) -> GoogleAccessToken:
        accessToken = await self.__googleApiAccessTokenStorage.getAccessToken()

        if accessToken is not None:
            return accessToken

        # TODO
        raise RuntimeError('this method is not yet implemented!')

    async def textToSpeech(self, request: GoogleTextSynthesizeRequest) -> GoogleTextSynthesisResponse:
        if not isinstance(request, GoogleTextSynthesizeRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        self.__timber.log('GoogleApiService', f'Fetching text-to-speech from Google... ({request=})')
        clientSession = await self.__networkClientProvider.get()

        googleApiKey = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudApiKey()
        if not utils.isValidStr(googleApiKey):
            raise GoogleCloudProjectApiKeyUnavailableException(f'No Google Cloud API Key is available: \"{googleApiKey}\"')

        googleProjectId = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudProjectId()
        if not utils.isValidStr(googleProjectId):
            raise GoogleCloudProjectIdUnavailableException(f'No Google Cloud Project ID is available: \"{googleProjectId}\"')

        try:
            response = await clientSession.post(
                url = f'https://texttospeech.googleapis.com/v1/text:synthesize',
                headers = {
                    # 'Authorization': f'Bearer {googleAccessToken.getAccessToken()}',
                    'Content-Type': self.__contentType,
                    'x-goog-api-key': googleApiKey,
                    'x-goog-user-project': googleProjectId
                },
                json = await self.__googleJsonMapper.serializeSynthesizeRequest(request),
            )
        except GenericNetworkException as e:
            self.__timber.log('GoogleApiService', f'Encountered network error when fetching text-to-speech ({request=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'GoogleApiService encountered network error when fetching text-to-speech ({request=}): {e}')

        if response is None:
            self.__timber.log('GoogleApiService', f'Encountered unknown network error when fetching text-to-speech ({request=}) ({response=})')
            raise GenericNetworkException(f'GoogleApiService encountered unknown network error when fetching text-to-speech ({request=}) ({response=})')

        responseStatusCode = response.getStatusCode()
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('GoogleApiService', f'Encountered non-200 HTTP status code when fetching text-to-speech ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(f'GoogleApiService encountered non-200 HTTP status code when fetching text-to-speech ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')

        synthesisResponse = await self.__googleJsonMapper.parseTextSynthesisResponse(jsonResponse)

        if synthesisResponse is None:
            self.__timber.log('GoogleApiService', f'Failed to parse JSON response into GoogleTextSynthesizeRequest instance ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({synthesisResponse=})')
            raise GenericNetworkException(f'GoogleApiService failed to parse JSON response into GoogleTextSynthesizeRequest instance ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({synthesisResponse=})')

        return synthesisResponse

    async def translate(self, request: GoogleTranslationRequest) -> GoogleTranslateTextResponse:
        if not isinstance(request, GoogleTranslationRequest):
            raise TypeError(f'request argument is malformed: \"{request}\"')

        self.__timber.log('GoogleApiService', f'Fetching translation from Google... ({request=})')
        clientSession = await self.__networkClientProvider.get()

        googleApiKey = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudApiKey()
        if not utils.isValidStr(googleApiKey):
            raise GoogleCloudProjectApiKeyUnavailableException(f'No Google Cloud API Key is available: \"{googleApiKey}\"')

        googleProjectId = await self.__googleCloudProjectCredentialsProvider.getGoogleCloudProjectId()
        if not utils.isValidStr(googleProjectId):
            raise GoogleCloudProjectIdUnavailableException(f'No Google Cloud Project ID is available: \"{googleProjectId}\"')

        try:
            response = await clientSession.post(
                url = f'https://translate.googleapis.com/v3/projects/{googleProjectId}:translateText',
                headers = {
                    'Content-Type': self.__contentType,
                    'x-goog-api-key': googleApiKey,
                    'x-goog-user-project': googleProjectId,
                },
                json = await self.__googleJsonMapper.serializeTranslationRequest(request)
            )
        except GenericNetworkException as e:
            self.__timber.log('GoogleApiService', f'Encountered network error when fetching translation ({request=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'GoogleApiService encountered network error when fetching traslation ({request=}): {e}')

        if response is None:
            self.__timber.log('GoogleApiService', f'Encountered unknown network error when fetching translation ({request=}) ({response=})')
            raise GenericNetworkException(f'GoogleApiService encountered unknown network error when fetching translation ({request=}) ({response=})')

        responseStatusCode = response.getStatusCode()
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('GoogleApiService', f'Encountered non-200 HTTP status code when fetching translation ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(f'GoogleApiService encountered non-200 HTTP status code when fetching translation ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')

        translateResponse = await self.__googleJsonMapper.parseTranslateTextResponse(jsonResponse)

        if translateResponse is None:
            self.__timber.log('GoogleApiService', f'Failed to parse JSON response into GoogleTranslationRequest instance ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({translateResponse=})')
            raise GenericNetworkException(f'GoogleApiService failed to parse JSON response into GoogleTranslationRequest instance ({request=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({translateResponse=})')

        return translateResponse
