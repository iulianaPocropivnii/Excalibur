import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

memory = []

def summarize_text(text):
    if len(text) > 1024:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": f"Please summarize the following text: {text}"},
            ],
            model="llama3-8b-8192",
        )
        summary = chat_completion.choices[0].message.content
        return summary
    else:
        return text

def query_llm(text):
    text_to_send = summarize_text(text)

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": text_to_send},
            {"role": "system", "content": "Answer is.."},
        ],
        model="llama3-8b-8192",
    )
    
    response = chat_completion.choices[0].message.content
    memory.append({"question": text, "answer": response}) 
    return response

def is_similar(text1, text2, threshold=0.7):
    common_words = set(text1.lower().split()) & set(text2.lower().split())
    similarity_ratio = len(common_words) / max(len(text1.split()), len(text2.split()))
    return similarity_ratio >= threshold

def search_memory(text):
    for entry in memory:
        if is_similar(text, entry["question"]):
            return f"Ai mai întrebat asta anterior. Răspunsul a fost: {entry['answer']}"
    return None

print("Memorie:", memory)

while True:
    prompt = input("USER: ")
    response = search_memory(prompt)
    
    if response is None:
        response = query_llm(prompt)
    print(f"ASSISTANT: {response}")
