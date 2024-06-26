# Improving accessibility by building a voice activated co-pilot chatbot to browse a document catalogue

## Fabdata LLM Retrieval

This project uses the [FabData LLM Retrieval](https://github.com/AI-for-Education/fabdata-llm-retrieval) package, which provides a platform for building a retrieval augmented generation (RAG) system around a set of documents. You can find an overview of the package in the project [README](https://github.com/AI-for-Education/fabdata-llm-retrieval/blob/main/README.md). This is provided as a framework with the tooling necessary to quickly start working on the problem, but please feel free to use other frameworks if you prefer or are familiar with them.


## OpenAI access keys

OpenAI are kindly supporting this event by providing access. You will need to download the `env` file from [here](https://www.robince.net/oerhackathon) and put it in this project folder named `.env`. The username and password to download this will be provided in the workshop.


## Data and Example

You can use whatever content you like from OER Commons. For example there is a large quantity of online courseware. You can use the metadata database from the other projects to investigate this if you like. However, to get you started we have included a number of [Flexbooks](https://www.ck12.org/fbbrowse/) from the CK-12 Foundation, which are textbooks curated from OERCommons hosted content. You can find the available Flexbooks in PDF format [here](https://www.dropbox.com/scl/fo/y67u4dgtdcc8b8qxqsr4m/AK_l7I3-Ac_lXiIbKX6qzqw?rlkey=0bm04kvv1od48xgugwa1m6r2j&dl=0). Download the `Flexbooks` folder and put it in a `data` sub-folder of this project.


## Components of a RAG system

- Catalogue of materials
    - text
    - tags
    - metadata

- LLM embeddings model
    - Embeddings are a numerical representation of text inputs that respect semantic relationships between inputs.
    - Text from the catalogue and text from the user input are both encoded as embeddings for semantic search
    - We have included a working script for processing the `Flexbooks` folder of data here: [encode_document_catalogue](scripts/encode_document_catalogue.py)

- LLM generator model
    - For example gpt-4, gpt-3.5, claude-sonnet, ...
    - Our main chat agent runs through this

- Vector database
    - We need a place to store and query the embeddings from the catalogue
    - Requires fast vector distance search and ability to handle multiple connections
    - Redis, Pinecone, CosmosDB, ...

- Chat agent
    - Basic conversational agent
    - Tool use
    - User interface

# Components of voice activation

- Audio recording
    - Push-to-talk or automated listening agent
- Automatic speech recognition
    - AI-powered or "traditional"
- Text-to-speech
    - AI-powered or "traditional"

