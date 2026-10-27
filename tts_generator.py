"""Narration ko awaaz me badalta hai (edge-tts, free, no API key)."""
import asyncio
import edge_tts
import config as C


async def _synth(text, path):
    comm = edge_tts.Communicate(text, C.VOICE, rate=C.TTS_RATE, pitch=C.TTS_PITCH)
    await comm.save(path)


def synthesize(text, path):
    asyncio.run(_synth(text, path))
    return path
