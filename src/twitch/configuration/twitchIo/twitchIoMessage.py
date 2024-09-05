from typing import Any

from frozendict import frozendict
from twitchio import Message

from .exceptions import TwitchIoHasMalformedTagsException, TwitchIoTagsIsMissingMessageIdException, \
    TwitchIoTagsIsMissingRoomIdException
from .twitchIoAuthor import TwitchIoAuthor
from .twitchIoChannel import TwitchIoChannel
from ..twitchAuthor import TwitchAuthor
from ..twitchChannel import TwitchChannel
from ..twitchConfigurationType import TwitchConfigurationType
from ..twitchMessage import TwitchMessage
from ..twitchMessageTags import TwitchMessageTags
from ....misc import utils as utils
from ....users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TwitchIoMessage(TwitchMessage):

    def __init__(
        self,
        message: Message,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(message, Message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__message: Message = message
        self.__author: TwitchAuthor = TwitchIoAuthor(message.author)
        self.__channel: TwitchChannel = TwitchIoChannel(
            channel = message.channel,
            userIdsRepository = userIdsRepository
        )

        self.__checkedForReplyData: bool = False
        self.__messageId: str | None = None
        self.__twitchChannelId: str | None = None
        self.__tags: TwitchMessageTags | None = None

    def getAuthor(self) -> TwitchAuthor:
        return self.__author

    def getAuthorId(self) -> str:
        return self.__author.getId()

    def getAuthorName(self) -> str:
        return self.__author.getName()

    def getChannel(self) -> TwitchChannel:
        return self.__channel

    def getContent(self) -> str | None:
        return self.__message.content

    async def getMessageId(self) -> str:
        tags = await self.getTags()
        return tags.messageId

    async def getTags(self) -> TwitchMessageTags:
        tags = self.__tags

        if tags is not None:
            return tags

        rawTagsDictionary = await self.__requireRawTagsDictionary()

        messageId: str | Any | None = rawTagsDictionary.get('id', None)
        if not utils.isValidStr(messageId):
            raise TwitchIoTagsIsMissingMessageIdException(f'Twitch message tags are missing \"id\" value ({messageId=}) ({tags=})')

        roomId: str | Any | None = rawTagsDictionary.get('room-id', None)
        if not utils.isValidStr(roomId):
            raise TwitchIoTagsIsMissingRoomIdException(f'Twitch message tags are missing \"room-id\" value ({roomId=}) ({tags=})')

        replyParentMsgBody: str | Any | None = rawTagsDictionary.get('reply-parent-msg-body', None)
        replyParentMsgId: str | Any | None = rawTagsDictionary.get('reply-parent-msg-id', None)
        replyParentUserId: str | Any | None = rawTagsDictionary.get('reply-parent-user-id', None)
        replyParentUserLogin: str | Any | None = rawTagsDictionary.get('reply-parent-user-login', None)

        tags = TwitchMessageTags(
            rawTags = frozendict(rawTagsDictionary),
            messageId = messageId,
            replyParentMsgBody = replyParentMsgBody,
            replyParentMsgId = replyParentMsgId,
            replyParentUserId = replyParentUserId,
            replyParentUserLogin = replyParentUserLogin,
            twitchChannelId = roomId
        )

        self.__tags = tags
        return tags

    async def getTwitchChannelId(self) -> str:
        tags = await self.getTags()
        return tags.twitchChannelId

    def getTwitchChannelName(self) -> str:
        return self.__channel.getTwitchChannelName()

    @property
    def isEcho(self) -> bool:
        return self.__message.echo

    async def isReply(self) -> bool:
        tags = await self.getTags()
        return utils.isValidStr(tags.replyParentMsgId)

    async def __requireRawTagsDictionary(self) -> dict[Any, Any]:
        tags: dict[Any, Any] | Any | None = self.__message.tags

        if not isinstance(tags, dict) or len(tags) == 0:
            raise TwitchIoHasMalformedTagsException(f'Encountered malformed `tags` value ({tags=}) ({self=})')

        return tags

    @property
    def twitchConfigurationType(self) -> TwitchConfigurationType:
        return TwitchConfigurationType.TWITCHIO
