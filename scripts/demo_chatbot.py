from pathlib import Path
import asyncio

from dotenv import load_dotenv

load_dotenv(override=True)

from openai import OpenAI
from fdllm import get_caller
from fdllm.sysutils import register_models
from fdllm.chat import ChatController
from fdllmret.plugin import retrieval_plugin
from fdllmret.helpers.encoding import DocsetEncoding

from audio import play_text, transcribe_input

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

VOICE = "echo"
# can be any of:
# "alloy", "echo", "fable", "onyx", "nova", "shimmer"

TTS_MODEL = "tts-1"
# can be any of:
# "tts-1", "tts-1-hd"

CHATBOT_MODEL = "gpt-4o"
# can be any of:
# "gpt-4o", "gpt-4-turbo", "gpt-4-0125-preview", "gpt-4-1106-preview", "gpt-3.5-turbo-0125"

MODE = "voice"
# can be any of "voice" or "text"

async def create_chatcontroller(caller=CHATBOT_MODEL):
    with open(ROOT / "contexts/context_searcher.txt") as f:
        msg = "\n".join(ln for ln in f if ln.strip() and ln.strip()[0] != "#")
    controller = ChatController(Caller=get_caller(caller), Sys_Msg={0: msg, -1: msg})
    plugin, datastore = await retrieval_plugin()
    controller.register_plugin(plugin)
    return controller, datastore


async def main(voice=VOICE, mode=MODE):
    first = True
    controller, datastore = await create_chatcontroller(caller=CHATBOT_MODEL)
    while True:
        if mode == "voice":
            if first:
                play_text("Awaiting your input", voice=voice)
                first = False
            prompt = transcribe_input()
        else:
            prompt = input("Prompt: ")
        print(prompt)
        if mode == "voice":
            play_text(f"You said: {prompt}. Is that correct?", voice=voice)
            confirm = transcribe_input()
            if not confirm.lower().startswith("yes"):
                play_text(f"OK, please try again. Awaiting your input", voice=voice)
                continue
            play_text("got it", voice=voice)
        if prompt.lower().startswith("exit"):
            break
        _, output = await controller.achat(prompt, max_tokens=1000)
        print(controller.recent_tool_calls)
        print(output.Message)
        if mode == "voice":
            play_text(f"{output.Message}.\n\nAwaiting your input", voice=voice)
            
    await datastore.client.connection_pool.disconnect()


if __name__ == "__main__":
    asyncio.run(main(), debug=True)
