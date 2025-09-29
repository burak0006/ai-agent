# Nine-Fin Agent

This project is a **financial RAG agent** built with **LangChain** and **LangGraph**.  
It ingests company financials, validates them with Pydantic, synthesizes the data into text with metadata, and indexes it in **Qdrant** for retrieval.  
Natural language queries are then answered through a graph-based agent pipeline.

---

## Key Points

- The `Dockerfile` is not working as desired due to time limitations. This can be fixed later.  
- **Qdrant** is served via Docker Compose.  
- **LangChain** is used as the framework, and **LangGraph** handles orchestration, persistence, and memory.  
- Redis caching is not enabled yet but can be added later.  
- The agent is structured as a **graph with 3 nodes**:
  1. Query or respond  
  2. RAG tool (retrieval)  
  3. Generate (model output)  
- Memory configuration ensures no information is lost.
- Note: Please bear in mind that Dockerfile is not working as desired due to time limitation which can be mitigated later on (just put a quick fix with requirements.txt which is not desired), qdarnt was served using docker compose. I orchestrated using langchain as framework and langraph for data persistence and memory management. Redis can be added for caching but i left as is for now. I added 3 graph nodes using langraph like multi agent orchestrator but it is included to query or respond tooling, RAG tool and generate response using our model as a graph structure. Memory config is also added so that during the chat, no information get lost The structure includes ETL pipeline and retriaval of data using RAG, The reason is that the financial data can be queried directly and I thought our data needs to be appropriate format for llm queries. Normally it could be converted to graph database and cypher structure, but i did not want to get out of the scope of task.Simply speaking data converted to vector embeddings with metadata filtering In my proposal, I snytehitized text from financial data so a query comes in (ETL), the system will be able to pick up as text with metadata from RAG in order to ensure the scalability. when a query comes in, it will not have to look through whole database. Just RAG + metadata filtering is supposed to be looking for relevant company metrics. But the caveat is that some metrics have only key-value pair which might be a cumbersome and misleading for retriaval (for example tronox 2023 data is confused by system with chemco) To mitigate this i added metadata filtering but I havent implemented to convert query into metadata filtering as it needs to have hardcoded information extraction or another agent. I refrained to use them as they might be a overkill but it is under the hood. To mitigate this, i would propose to use cypher queries for direct requests (neo4j)
---

## Architecture

- **ETL pipeline** prepares the data:  
  - Raw financial JSON is validated with Pydantic schemas.  
  - Synthesized into natural language text + metadata.  
- **RAG retrieval**:  
  - Data is converted into vector embeddings.  
  - Metadata filtering avoids scanning the whole dataset.  
  - Example: queries for *Tronox 2023 sales* will only fetch relevant metrics.  
- **Caveat**: some metrics are simple key–value pairs, which can confuse retrieval.  
  - Mitigated with metadata filtering, but query → metadata conversion is not fully implemented (would need hardcoding or another agent).  
  - Future solution: Cypher queries against a graph database.  
- **Evaluation metrics**:
  - Retrieval: precision@k, recall@k, nDCG@k  
  - LLM: accuracy, conciseness, faithfulness  
- **Logging** is included in relevant parts.  
- **Prompting**: system messages are inside nodes. Recommended improvement: move prompts into YAML config.  
- **Scalability**: batch embeddings can be added later for larger datasets.  

---

## How to run

```bash
pip install poetry
poetry init
poetry install
poetry shell
```

## To run ETL pipeline

```bash
poetry run python src/nine_fin_agent/snythesizer/load.py \
  --input data/financial_data.json \
  --output data/documents.txt \
  --show 5
```

## Run agent local

```bash
poetry run python src/nine_fin_agent/agent.py
```

## To build and run docker

```bash
docker build -t ai-agent .
docker run --rm -it -e OPENAI_API_KEY=YOUR_KEY ai-agent
```

## Qdrant

```bash
docker-compose up --build
```

## To run evaliation

```bash
poetry run python eval/evaluate.py --num-samples 5
```