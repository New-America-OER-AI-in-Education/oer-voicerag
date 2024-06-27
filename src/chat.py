from pathlib import Path
import asyncio
import json
from typing import Dict, List

from dotenv import load_dotenv

load_dotenv(override=True)

from openai import OpenAI
from fdllm import get_caller
from fdllm.sysutils import register_models
from fdllm.chat import ChatController
from fdllm.tooluse import Tool, ToolParam, ToolItem
from fdllm.extensions import general_query
from fdllmret.plugin import retrieval_plugin
from fdllmret.helpers.encoding import DocsetEncoding

MODE = "text"
# can be any of "voice" or "text"
if MODE == "voice":
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


class VocabWords(Tool):
    name = "get_vocabulary_words"
    description = "search through a document for vocabulary words"
    params = {
        "ID": ToolParam(
            type="string", description="ID of document to search", required=True
        ),
        "vocab_words": ToolParam(
            type="array",
            items=ToolItem(type="string"),
            description="list of vocabulary words to search for",
            required=True,
        ),
    }
    json_database: Dict | List[Dict]

    def execute(self, **params):
        return super().execute(**params)

    async def aexecute(self, **params):
        document_id = params["ID"]
        document = [doc for doc in self.json_database if doc["id"] == document_id]
        if len(document) > 0:
            document = document[0]
        word_dict = {key.lower(): 0 for key in params["vocab_words"]}
        for word in document["text"].split():
            if word.lower() in word_dict:
                word_dict[word] += 1
        return json.dumps([key for key, val in word_dict.items() if val > 0])


def summarize_message(text, tool_response):
    jsonin = {
        "message:: A message returned by an AI assistant": text,
        "tool_response::"
        " The response from a tool that was used to generate this message": tool_response,
    }
    jsonout = {
        "message_type:: [info_dump/greeting/clarification]": None,
        "info_dump_details::  Only if message type is 'info_dump', fill this in.": {
            "summary:: A 100 word summary of the text": None,
            "bullet_points:: parse the response into separate bullet points. Don't summarize": None,
            "document_list:: list of referenced documents": [
                {"name": None, "id": None, "url": None}
            ],
        },
    }
    return general_query(jsonin, jsonout, caller=get_caller("gpt-4-turbo"))


async def create_chatcontroller(caller=CHATBOT_MODEL):
    with open(ROOT / "contexts/context_searcher_summarize.txt") as f:
        msg = "\n".join(ln for ln in f if ln.strip() and ln.strip()[0] != "#")
    controller = ChatController(Caller=get_caller(caller), Sys_Msg={0: msg, -1: msg})
    plugin, datastore = await retrieval_plugin()
    json_database = plugin.Tools[1].json_database
    plugin.Tools.append(VocabWords(json_database=json_database))
    controller.register_plugin(plugin)
    return controller, datastore

