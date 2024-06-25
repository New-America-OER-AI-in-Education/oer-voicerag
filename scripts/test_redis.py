# %%
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)


import redis

# %%
HOST = os.environ.get("REDIS_HOST")
PASS = os.environ.get("REDIS_PASSWORD")

print(HOST)

r = redis.Redis(host=HOST, port=6381, password=PASS, ssl=True)

print(r.ping())

print(r.keys("*"))
# %%
r.set("test", 1)
print(r.keys("*"))

r.flushall()
print(r.keys("*"))