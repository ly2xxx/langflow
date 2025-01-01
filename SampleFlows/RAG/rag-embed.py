from langflow.load import run_flow_from_json
TWEAKS = {
  "SplitText-hJxHw": {
    "chunk_overlap": 100,
    "chunk_size": 1000,
    "separator": "\n"
  },
  "OllamaEmbeddings-h6d81": {
    "base_url": "http://localhost:11434",
    "model": "nomic-embed-text"
  },
  "Chroma-MEuBh": {
    "allow_duplicates": False,
    "chroma_server_cors_allow_origins": "",
    "chroma_server_grpc_port": None,
    "chroma_server_host": "",
    "chroma_server_http_port": None,
    "chroma_server_ssl_enabled": False,
    "collection_name": "langflow",
    "limit": None,
    "number_of_results": 10,
    "persist_directory": ".\\chroma\\",
    "search_query": "",
    "search_type": "Similarity"
  },
  "Directory-x4zLw": {
    "depth": 0,
    "load_hidden": False,
    "max_concurrency": 2,
    "path": ".\\input\\",
    "recursive": False,
    "silent_errors": False,
    "types": [
      "pdf"
    ],
    "use_multithreading": False
  }
}

result = run_flow_from_json(flow="RAG-embed-Ollama.json",
                            input_value="",
                            session_id="", # provide a session id if you want to use session state
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)