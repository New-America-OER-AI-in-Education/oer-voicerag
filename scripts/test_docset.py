# %%
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(override=True)

from fdllmret.helpers.encoding import DocsetEncoding
from fdllmret.helpers.analysis import auto_tag_generate

# %%
CONFIG = Path(__file__).resolve().parents[1] / "flexbooks_config.yml"

docset = DocsetEncoding.from_config(config_file=CONFIG, encode=False)

# %%
docset.encode()

# %%
# cluster the chunk embeddings
chunk_size = 800
n_clusters = 5
cluster_kwargs = {"n_init": 10}
cluster_labs, scores = docset.docembs.cluster(
    chunk_size, n_clusters=n_clusters, cluster_kwargs=cluster_kwargs
)

# %%
# visualise the clusters on TSNE plot
docset.docembs.tsne.plot(800, c=cluster_labs)

# %%
# return the top 3 text chunks for each cluster
n_top = 3
topnchunks = docset.topn_cluster_chunks(chunk_size, n_top, cluster_labs, scores)

# %%
# generate labels for each cluster based on the top 3 chunks
tags, flattags = auto_tag_generate(cluster_labs, scores, topnchunks, chunk_size)

# %%
# add the new tags to the documents and save to cache
docset._apply_tags(chunk_size, cluster_labs, tags)
docset.to_cache()
