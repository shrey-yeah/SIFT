from openai import OpenAI
import openai

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


def error_answer(message):
    print(f"ERROR: {message}")
    return Answer(
        answer=message,
        confidence="low",
        citations=[],
        caveats=[message],
        abstained=True,
    )


def generate_answer(question):
    try: 

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
            temperature=0,
            seed=1234,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}         
            ],
            response_format=Answer
        )
        print(f"Tokens: prompt={response.usage.prompt_tokens}, completion={response.usage.completion_tokens} | fingerprint={response.system_fingerprint}")
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

    except openai.AuthenticationError:
        return error_answer("The AI service isn't configured correctly — check OPENAI_API_KEY in .env.")
    except openai.RateLimitError as e:
        if e.body and e.body.get("error", {}).get("code") == "insufficient_quota":
            return error_answer("The OpenAI account has no remaining credits/quota.")
        return error_answer("Too many requests right now — please wait a moment and try again.")
    #connection error
    except openai.APIConnectionError:
        return error_answer("The AI service is unreachable right now (network issue).")
    except openai.APITimeoutError:
        return error_answer("The AI service took too long to respond — please try again.")
    except openai.BadRequestError as e:
        return error_answer(f"Internal error generating the answer: {e}")
    except openai.APIStatusError as e:
        return error_answer(f"The AI service returned an unexpected error (status {e.status_code}).")


