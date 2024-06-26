# %%
from pathlib import Path
import asyncio

from dotenv import load_dotenv
load_dotenv(override=True)

from fdllmret.helpers.encoding import DocsetEncoding
from fdllmret.helpers.upsert import upsert_docenc

# %%
CONFIG = Path(__file__).resolve().parents[1] / "flexbooks_config.yml"

docset = DocsetEncoding.from_config(config_file=CONFIG, encode=True)

# %%
asyncio.run(upsert_docenc(docset))