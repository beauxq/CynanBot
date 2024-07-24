from dataclasses import dataclass

from .addOrRemoveUserActionType import AddOrRemoveUserActionType


@dataclass(frozen = True)
class AddOrRemoveUserData:
    actionType: AddOrRemoveUserActionType
    userId: str
    userName: str
