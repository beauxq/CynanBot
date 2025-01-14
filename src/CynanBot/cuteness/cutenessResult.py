import locale
from dataclasses import dataclass

import CynanBot.misc.utils as utils
from CynanBot.cuteness.cutenessDate import CutenessDate


@dataclass(frozen = True)
class CutenessResult():
    cutenessDate: CutenessDate
    cuteness: int | None
    userId: str
    userName: str

    @property
    def cutenessStr(self) -> str:
        cuteness = self.requireCuteness()
        return locale.format_string("%d", cuteness, grouping = True)

    def requireCuteness(self) -> int:
        if not utils.isValidInt(self.cuteness):
            raise RuntimeError(f'No cuteness value is available: {self}')

        return self.cuteness
