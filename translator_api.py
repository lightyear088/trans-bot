from deep_translator import GoogleTranslator


async def get_languages():
    return list(map(
        str.upper,
        GoogleTranslator().get_supported_languages(True).values()
    ))


async def translate(text: str, language: str):
    return GoogleTranslator(source="auto", target=language.lower()).translate(text)
