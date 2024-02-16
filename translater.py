import asyncio
from googletrans import Translator


async def translator_foo(sentence):
    translator = Translator()
    result = translator.translate(sentence)
    return result.text



