from openai import OpenAI

from prompts import SYSTEM_PROMPT, build_user_prompt
from schema import Answer, Citation
import chromadb
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

ABSTAIN_THRESHOLD = float(os.getenv("ABSTAIN_THRESHOLD", 1.3))

collection= chromadb.PersistentClient(
    path="./chroma_db"
).get_collection(
    name="company_documents"
)




#generate user prompt
def retrieve (question, top_k=5):
    #query the vector database
    results = collection.query(
        query_texts=[question],
        n_results=top_k
    )
    return results["documents"][0], results["metadatas"][0], results["distances"][0]


def validate_citations(citations, metadatas):
    #keep only citations whose chunk_id was actually in what we retrieved
    retrieved_ids = {meta.get("chunk_id") for meta in metadatas}
    valid = []
    for citation in citations:
        if citation.chunk_id in retrieved_ids:
            valid.append(citation)
        else:
            print(f"WARNING: model cited chunk_id '{citation.chunk_id}', which was not in the retrieved context. Dropping it.")
    return valid


def generate_answer(question):

    documents, metadatas, distances = retrieve(question)

    best_distance = min(distances)
    if best_distance > ABSTAIN_THRESHOLD:
        print(f"Abstained: closest match was too weak (distance={best_distance:.2f} > threshold={ABSTAIN_THRESHOLD}).")
        return Answer(
            answer="I couldn't find anything in the documents that answers this question.",
            confidence="low",
            citations=[],
            caveats=[f"Best retrieval distance was {best_distance:.2f}, above the {ABSTAIN_THRESHOLD} threshold."],
            abstained=True,
        )

    user_prompt = build_user_prompt(question, documents, metadatas)
    response  = client.chat.completions.parse (
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}         
        ],
        response_format=Answer
    )
    msg = response.choices[0].message
    msg.parsed.citations = validate_citations(msg.parsed.citations, metadatas)

    if msg.parsed.abstained:
        print("Abstained from answering the question. The documents don't cover this.")
    if msg.parsed.caveats:
        print("Caveats:", msg.parsed.caveats)
    if msg.parsed.citations:
        print("Citations:")
        for citation in msg.parsed.citations:
            print(f"- Document: {citation.document}, Page: {citation.page}, Quote: {citation.quote}, Chunk ID: {citation.chunk_id}")

    return msg.parsed
