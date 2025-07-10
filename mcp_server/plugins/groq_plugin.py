import requests
import os

def query_llm(prompt: str):
    url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = os.getenv("GROQ_API_KEY")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",  
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    print("---- Request Payload ----")
    print(payload)

    response = requests.post(url, headers=headers, json=payload)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("---- Groq Error Response ----")
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        raise

    return response.json()["choices"][0]["message"]["content"]
