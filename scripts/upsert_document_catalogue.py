# %%
from pathlib import Path
import asyncio
import os

from dotenv import load_dotenv
load_dotenv(override=True)

from fdllmret.helpers.encoding import DocsetEncoding
from fdllmret.helpers.upsert import upsert_docenc
import redis

# %%
# wipe existing DB

HOST = os.environ.get("REDIS_HOST")
PASS = os.environ.get("REDIS_PASSWORD")
PORT = int(os.environ.get("REDIS_PORT", 6379))
SSL = os.environ.get("REDIS_SSL", "false").lower() == "true"

print(HOST)
print(PORT)
print(SSL)

r = redis.Redis(host=HOST, port=PORT, password=PASS, ssl=SSL)
r.flushall()

# %%
CONFIG = Path(__file__).resolve().parents[1] / "flexbooks_config.yml"

docset = DocsetEncoding.from_config(config_file=CONFIG, encode=True)

# %%
asyncio.run(upsert_docenc(docset))