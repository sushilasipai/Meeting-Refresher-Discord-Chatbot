from fastapi import FastAPI, Request
from mcp_server.plugins.gdocs_plugin import get_doc_text
from mcp_server.plugins.groq_plugin import query_llm
from shared.document_validation import extract_doc_id_from_url

app = FastAPI()

@app.post("/query")
async def handle_query(req: Request):
    data = await req.json()
    question = data.get("question")
    doc_url = data.get("doc_url")

    if not question or not doc_url:
        return {"error": "Both 'question' and 'doc_url' are required."}
    try:
        doc_id = extract_doc_id_from_url(doc_url)
    except ValueError as e:
        return {"error": str(e)}s
    try:
        notes = get_doc_text(doc_id)
    except Exception as e:
        return {"error": f"Google Docs access failed: {str(e)}"}

    prompt = f"""You are an assistant helping with meeting notes.

                    Meeting Notes:
                    {notes}

                    Question:
                    {question}

                    Instructions:
                        - If the user message is a question or request related to the meeting notes, provide a clear, concise, and helpful answer.
                        - If the user says thank you or expresses gratitude, respond naturally (e.g., "You're welcome!", "Glad to help!").
                        - If the message is casual or unrelated, respond with a friendly and polite prompt (e.g., "Let me know if you'd like to discuss anything about the meeting notes.").
                """
    answer = query_llm(prompt)
    return {"answer": answer}
