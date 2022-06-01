import json
import os
from typing import Dict

import aiofile
import CynanBotCommon.utils as utils

from persistence.generalSettingsSnapshot import GeneralSettingsSnapshot


class GeneralSettingsRepository():

    def __init__(
        self,
        generalSettingsFile: str = 'persistence/generalSettingsRepository.json'
    ):
        if not utils.isValidStr(generalSettingsFile):
            raise ValueError(f'generalSettingsFile argument is malformed: \"{generalSettingsFile}\"')

        self.__generalSettingsFile: str = generalSettingsFile

    def getAll(self) -> GeneralSettingsSnapshot:
        jsonContents = self.__readJson()
        return GeneralSettingsSnapshot(jsonContents)

    async def getAllAsync(self) -> GeneralSettingsSnapshot:
        jsonContents = await self.__readJsonAsync()
        return GeneralSettingsSnapshot(jsonContents)

    def __readJson(self) -> Dict[str, object]:
        if not os.path.exists(self.__generalSettingsFile):
            raise FileNotFoundError(f'General settings file not found: \"{self.__generalSettingsFile}\"')

        with open(self.__generalSettingsFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from general settings file: \"{self.__generalSettingsFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of general settings file \"{self.__generalSettingsFile}\" is empty')

        return jsonContents

    async def __readJsonAsync(self) -> Dict[str, object]:
        if not os.path.exists(self.__generalSettingsFile):
            raise FileNotFoundError(f'General settings file not found: \"{self.__generalSettingsFile}\"')

        async with aiofile.async_open(self.__generalSettingsFile, 'r') as file:
            data = await file.read()
            jsonContents = json.loads(data)

        if jsonContents is None:
            raise IOError(f'Error reading from general settings file: \"{self.__generalSettingsFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of general settings file \"{self.__generalSettingsFile}\" is empty')

        return jsonContents
