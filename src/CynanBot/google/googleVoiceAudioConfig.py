from dataclasses import dataclass

from CynanBot.google.googleVoiceAudioEncoding import GoogleVoiceAudioEncoding


@dataclass(frozen = True)
class GoogleVoiceAudioConfig():
    pitch: float | None
    speakingRate: float | None
    volumeGainDb: float | None
    sampleRateHertz: int | None
    audioEncoding: GoogleVoiceAudioEncoding
