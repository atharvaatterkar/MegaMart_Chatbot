import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from groq import Groq

faqs_path = Path(__file__).parent / "/resources/faq_data.csv"
chroma_client = chromadb.Client()
collection_name_faq = 'faqs'

ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)


def ingest_faq_data(path):
    if collection_name_faq in [c.name for c in chroma_client.list_collections()]:
        print("Ingesting FAQ data into chromadb...")
        collection = chroma_client.get_or_create_collection(name=collection_name_faq,
                                            embedding_function=ef)
        df = pd.read_csv(path)
        docs = df['question'].to_list()
        metadata = [{'answer': ans} for ans in df['answer'].to_list()]
        ids = [f"id_{i}" for i in range(len(docs))]

        collection.add(
            documents=docs,
            metadatas=metadata,
            ids = ids
        )
        print(f"FAQ Data Sucessfully ingested into chroma Collection {collection_name_faq}")

    else:
        print(f"Collection {collection_name_faq} already exists!")


def get_relevant_qa(query):
    collection = chroma_client.get_collection(name=collection_name_faq)(
        name=collection_name_faq,
        embedding_function=ef
    )
    result = collection.query(
        query_texts=[query],
        n_results= 2
    )
    return result

def generate_answer(query, context, api_key):
    prompt = f'''Given the following context and question, generate answer based on this context only.
    If the answer is not found in the context, kindly state "I don't know". Don't try to make up an answer.
    
    CONTEXT: {context}
    
    QUESTION: {query}
    '''

    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
       model="llama-3.3-70b-versatile",
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )
    return completion.choices[0].message.content


def faq_chain(query, api_key): 
    result = get_relevant_qa(query)
    context = "".join([r.get('answer') for r in result['metadatas'][0]])
    answer = generate_answer(query, context, api_key)
    return answer



if __name__ == '__main__':
    ingest_faq_data(faqs_path)
    query = "what's your policy on defective products?"
    query = "Do you take cash as a payment option?"
    # result = get_relevant_qa(query)
    answer = faq_chain(query)
    print("Answer:",answer)