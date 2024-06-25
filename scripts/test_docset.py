# %%
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(override=True)

from fdllmret.helpers.encoding import DocsetEncoding

# %%
CONFIG = Path(__file__).resolve().parents[1] / "flexbooks_config.yml"

docset = DocsetEncoding.from_config(config_file=CONFIG, encode=False)

# %%
docset.encode()

# %%
docset.auto_tag(chunk_size=800, overwrite=True, n_clusters=6)
docset.tags