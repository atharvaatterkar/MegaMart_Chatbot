import os
from groq import Groq



def talk(query):
    client = Groq(api_key=api_key)
    prompt = f'''You are a helpful and friendly chatbot designed for small talk. You can answer questions about the weather, your name, your purpose, and more.
    
    QUESTION: {query}
    '''
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