import typing_extensions as typing


class GeminiImageAnalyzer(typing.TypedDict):
    description: str


class GeminiAudioAnalyzer(typing.TypedDict):
    transcription: str
