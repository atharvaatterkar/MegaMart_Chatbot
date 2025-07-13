import pandas as pd
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq

model = SentenceTransformer("all-MiniLM-L6-v2")

faqs_path = Path(__file__).resolve().parents[1] / "Resources" / "faq_data.csv"
faq_df = pd.read_csv(faqs_path)'

faq_embeddings = model.encode(faq_df["question"].tolist())



def get_relevant_qa(query):
    query_embedding = model.encode([query], convert_to_tensor=True)
    similarities = cosine_similarity(query_embedding, faq_embeddings)[0]

    # Get top 2 results
    top_indices = similarities.argsort()[-2:][::-1]
    results = faq_df.iloc[top_indices]
    return results

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
    results = get_relevant_qa(query)
    context = "\n".join(results["answer"].tolist())
    answer = generate_answer(query, context, api_key)
    return answer



if __name__ == '__main__':
     query = "Do you take cash as a payment option?"
    api_key = "your-api-key-here"
    print("Answer:", faq_chain(query, api_key))
