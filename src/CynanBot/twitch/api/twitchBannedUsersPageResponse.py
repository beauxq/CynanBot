from typing import Any, Dict, List, Optional

from CynanBot.twitch.api.twitchBannedUser import TwitchBannedUser
from CynanBot.twitch.twitchPaginationResponse import TwitchPaginationResponse


class TwitchBannedUsersPageResponse():

    def __init__(
        self,
        users: Optional[List[TwitchBannedUser]],
        pagination: Optional[TwitchPaginationResponse]
    ):
        if users is not None and not isinstance(users, List):
            raise ValueError(f'users argument is malformed: \"{users}\"')
        elif pagination is not None and not isinstance(pagination, TwitchPaginationResponse):
            raise ValueError(f'pagination argument is malformed: \"{pagination}\"')

        self.__users: Optional[List[TwitchBannedUser]] = users
        self.__pagination: Optional[TwitchPaginationResponse] = pagination

    def getPagination(self) -> Optional[TwitchPaginationResponse]:
        return self.__pagination

    def getUsers(self) -> Optional[List[TwitchBannedUser]]:
        return self.__users

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'pagination': self.__pagination,
            'users': self.__users
        }
