import chromadb
from datetime import datetime
from pdf_loader import chunks

client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="company_documents"
)

ids = [f"chunk_{i}" for i in range(len(chunks))]
ingested_at = datetime.now().isoformat()

collection.upsert(
    ids=ids,
    documents=[c.page_content for c in chunks],
    metadatas=[
        {**c.metadata, "chunk_id": ids[i], "ingested_at": ingested_at}
        for i, c in enumerate(chunks)
    ]
)


results = collection.query(
    query_texts=[
        "when can employees take leaves?"
    ],
    n_results=3
)

print(results["documents"], results["metadatas"])

for q in ['how many annual leave days do employees get?', 'what is the weather on mars today?', 'casual leave']:
    r = collection.query(query_texts=[q], n_results=3)
    print(q, '→', r['distances'][0])