import re
import uuid
from typing import Pattern

import CynanBot.misc.utils as utils
from CynanBot.cheerActions.cheerActionIdGeneratorInterface import \
    CheerActionIdGeneratorInterface


class CheerActionIdGenerator(CheerActionIdGeneratorInterface):

    def __init__(self, maxLength: int = 3):
        if not utils.isValidInt(maxLength):
            raise TypeError(f'maxLength argument is malformed: \"{maxLength}\"')
        elif maxLength < 3 or maxLength > 8:
            raise ValueError(f'maxLength argument is out of bounds: {maxLength}')

        self.__maxLength: int = maxLength
        self.__actionIdRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def generateActionId(self) -> str:
        newUuid = str(uuid.uuid4())
        cleanedUuid = self.__actionIdRegEx.sub('', newUuid)

        if len(cleanedUuid) > self.__maxLength:
            cleanedUuid = cleanedUuid[:self.__maxLength]

        return cleanedUuid
