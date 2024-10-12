import pytest

from src.decTalk.decTalkMessageCleaner import DecTalkMessageCleaner
from src.decTalk.decTalkMessageCleanerInterface import DecTalkMessageCleanerInterface
from src.emojiHelper.emojiHelper import EmojiHelper
from src.emojiHelper.emojiHelperInterface import EmojiHelperInterface
from src.emojiHelper.emojiRepository import EmojiRepository
from src.emojiHelper.emojiRepositoryInterface import EmojiRepositoryInterface
from src.google.googleJsonMapper import GoogleJsonMapper
from src.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.ttsSettingsRepository import TtsSettingsRepository
from src.tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface


class TestDecTalkMessageCleaner:

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    emojiRepository: EmojiRepositoryInterface = EmojiRepository(
        emojiJsonReader = JsonStaticReader(
            jsonContents = {
                'emojis': [
                    {
                        'code': [
                            "1F600"
                        ],
                        'emoji': '😀',
                        'name': 'grinning face',
                        'category': 'Smileys & Emotion',
                        'subcategory': 'face-smiling',
                        'support': {
                            'apple': True,
                            'google': True,
                            'windows': True
                        }
                    },
                    {
                        'code': [
                            "1F988"
                        ],
                        'emoji': '🦈',
                        'name': 'shark',
                        'category': 'Animals & Nature',
                        'subcategory': 'animal-marine',
                        'support': {
                            'apple': True,
                            'google': True,
                            'windows': True
                        }
                    }
                ]
            }
        ),
        timber = timber
    )

    emojiHelper: EmojiHelperInterface = EmojiHelper(
        emojiRepository = emojiRepository
    )

    googleJsonMapper: GoogleJsonMapperInterface = GoogleJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository
    )

    ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
        googleJsonMapper = googleJsonMapper,
        settingsJsonReader = JsonStaticReader(dict())
    )

    cleaner: DecTalkMessageCleanerInterface = DecTalkMessageCleaner(
        emojiHelper = emojiHelper,
        timber = timber,
        ttsSettingsRepository = ttsSettingsRepository
    )

    @pytest.mark.asyncio
    async def test_clean_withCommaPauseInlineCommand(self):
        result = await self.cleaner.clean('hello world [:comma 50]')
        assert result == 'hello world'

        result = await self.cleaner.clean('hello world [:cp 1000,10000] blah')
        assert result == 'hello world blah'

    @pytest.mark.asyncio
    async def test_clean_withDangerousCharactersString(self):
        result = await self.cleaner.clean('& cd C:\\ & dir')
        assert result == 'cd C:\\ dir'

    @pytest.mark.asyncio
    async def test_clean_withDecTalkFlagsString1(self):
        result = await self.cleaner.clean('-post hello')
        assert result == 'hello'

    @pytest.mark.asyncio
    async def test_clean_withDecTalkFlagsString2(self):
        result = await self.cleaner.clean('-pre hello')
        assert result == 'hello'

    @pytest.mark.asyncio
    async def test_clean_withDecTalkFlagsString3(self):
        result = await self.cleaner.clean('-l hello')
        assert result == 'hello'

    @pytest.mark.asyncio
    async def test_clean_withDecTalkFlagsString4(self):
        result = await self.cleaner.clean('-lw hello')
        assert result == 'hello'

    @pytest.mark.asyncio
    async def test_clean_withDecTalkFlagsString5(self):
        result = await self.cleaner.clean('-l[t] hello')
        assert result == 'hello'

    @pytest.mark.asyncio
    async def test_clean_withDecTalkFlagsString6(self):
        result = await self.cleaner.clean('-v show version information')
        assert result == 'show version information'

    @pytest.mark.asyncio
    async def test_clean_withDecTalkFlagsString7(self):
        result = await self.cleaner.clean('-d userDict')
        assert result == 'userDict'

    @pytest.mark.asyncio
    async def test_clean_withDecTalkFlagsString8(self):
        result = await self.cleaner.clean('-lang uk hello world')
        assert result == 'hello world'

    @pytest.mark.asyncio
    async def test_clean_withDesignVoiceInlineCommand(self):
        result = await self.cleaner.clean('hello world [:dv] qwerty')
        assert result == 'hello world qwerty'

    @pytest.mark.asyncio
    async def test_clean_withDirectoryTraversalString(self):
        result = await self.cleaner.clean('& cd .. & dir')
        assert result == 'cd dir'

    @pytest.mark.asyncio
    async def test_clean_withEmojiString(self):
        result = await self.cleaner.clean('shark 🦈 shark 😀 🤔')
        assert result == 'shark shark shark grinning face'

    @pytest.mark.asyncio
    async def test_clean_withEmptyString(self):
        result = await self.cleaner.clean('')
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withErrorInlineCommand(self):
        result = await self.cleaner.clean('hello world [:error] qwerty')
        assert result == 'hello world qwerty'

        result = await self.cleaner.clean('azerty   [:erro C:\\log.txt]  qwerty ')
        assert result == 'azerty qwerty'

    @pytest.mark.asyncio
    async def test_clean_withExtraneousSpacesString(self):
        result = await self.cleaner.clean('  Hello,    World! ')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_clean_withHelloWorldString(self):
        result = await self.cleaner.clean('Hello, World!')
        assert result == 'Hello, World!'

    @pytest.mark.asyncio
    async def test_clean_withLogInlineCommand(self):
        result = await self.cleaner.clean('apple [:log] google')
        assert result == 'apple google'

        result = await self.cleaner.clean(' microsoft[:log C:\\log.txt]  twitch ')
        assert result == 'microsoft twitch'

    @pytest.mark.asyncio
    async def test_clean_withModeInlineCommand(self):
        result = await self.cleaner.clean('KEKW [:mode 7] LUL')
        assert result == 'KEKW LUL'

    @pytest.mark.asyncio
    async def test_clean_withNone(self):
        result = await self.cleaner.clean(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withOverlyLongMessage(self):
        result = await self.cleaner.clean('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ac velit neque. Suspendisse sed scelerisque metus, eget ultrices mi. Quisque accumsan laoreet sapien, eget euismod ex hendrerit a. Ut mattis ipsum enim, eget ultrices nisl pulvinar at. Sed eu ornare neque. Quisque nec commodo enim. Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas efficitur odio arcu, vel vestibulum metus porttitor ac. Mauris sollicitudin, velit in malesuada scelerisque, magna nisi posuere nisi, ac sodales dolor massa vitae ex. Sed fermentum purus vel purus efficitur varius id ut lacus. Duis eu neque dapibus, ornare mauris porta, placerat enim. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut et nisi mi. Donec efficitur sapien a bibendum tincidunt.')
        assert result == 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ac velit neque. Suspendisse sed scelerisque metus, eget ultrices mi. Quisque accumsan laoreet sapien, eget euismod ex hendrerit a. Ut mattis ipsum enim, eget ultrices nisl pulvinar at. Se'
        assert len(result) == await self.ttsSettingsRepository.getMaximumMessageSize()

    @pytest.mark.asyncio
    async def test_clean_withPeriodPauseInlineCommand(self):
        result = await self.cleaner.clean('apple [:period] google')
        assert result == 'apple google'

        result = await self.cleaner.clean('oatsngoats[:peri 123]imyt')
        assert result == 'oatsngoats imyt'

        result = await self.cleaner.clean('[:pp]')
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withPitchInlineCommand(self):
        result = await self.cleaner.clean('[:pitch] hello')
        assert result == 'hello'

    @pytest.mark.asyncio
    async def test_clean_withPlayInlineCommand(self):
        result = await self.cleaner.clean('[:play \"C:\\song.wav\"]')
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withRateInlineCommand(self):
        result = await self.cleaner.clean('rate [:rate0]?')
        assert result == 'rate ?'

    @pytest.mark.asyncio
    async def test_clean_withSyncInlineCommand(self):
        result = await self.cleaner.clean('time to [:sync 1] ok')
        assert result == 'time to ok'

    @pytest.mark.asyncio
    async def test_clean_withToneInlineCommand(self):
        result = await self.cleaner.clean('this is a tone inline command [:tone]')
        assert result == 'this is a tone inline command'

        result = await self.cleaner.clean('this is a different tone inline command: [:t]')
        assert result == 'this is a different tone inline command:'

    @pytest.mark.asyncio
    async def test_clean_withUniText(self):
        result = await self.cleaner.clean('hello world uni5')
        assert result == 'hello world'

    @pytest.mark.asyncio
    async def test_clean_withWildNestedInlineCommands(self):
        result = await self.cleaner.clean('hello [[[:play \"C:\\song.wav\"]:volume set 10]: dv qwerty] [:pitch 10] world uni5')
        assert result == 'hello world'

    @pytest.mark.asyncio
    async def test_clean_withVolumeInlineCommand(self):
        result = await self.cleaner.clean('this is a volume inline command [:vol set 99]')
        assert result == 'this is a volume inline command'

        result = await self.cleaner.clean('[:volume something]1')
        assert result == '1'

    @pytest.mark.asyncio
    async def test_clean_withWhitespaceString(self):
        result = await self.cleaner.clean(' ')
        assert result is None