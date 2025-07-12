import pandas as pd
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions


faqs_path = Path(__file__).parent / "/Resources/faq_data.csv"
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



if __name__ == "__main__":
    print(faqs_path)
    # ingest_faq_data(path)
    query = "what's your policy on defective products?"
    result = get_relevant_qa(query)