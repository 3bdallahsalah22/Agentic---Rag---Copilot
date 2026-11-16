from app.services.ingestion import load_file , chunk_documnets
from pathlib import Path
from app.rag.vectorstore import add_documents


docs = load_file(Path("data/sample_kb/company_it_hanbook.md"))

docs = chunk_documnets(docs)

add_documents(docs)