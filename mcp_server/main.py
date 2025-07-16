from fastapi import FastAPI, Request
from mcp_server.plugins.gdocs_plugin import get_doc_text
from mcp_server.plugins.groq_plugin import query_llm
from .prompt_builder import build_prompt
from shared.document_validation import extract_doc_id_from_url

app = FastAPI()

@app.post("/mcp")
async def handle_mcp_query(req: Request):
    data = await req.json()
    user_input = data.get("input", {})
    message = user_input.get("message", "")
    context_info = user_input.get("context", {})

    if not message or not context_info.get("doc_url"):
        return {"error": "Both 'input.message' and 'input.context.doc_url' are required."}

    try:
        doc_id = extract_doc_id_from_url(context_info["doc_url"])
        notes = get_doc_text(doc_id)
    except Exception as e:
        return {"error": f"Failed to load document: {str(e)}"}
    
    messages = build_prompt(message, notes)

    try:
        answer = query_llm(messages)
    except Exception as e:
        return {"error": f"LLM call failed: {str(e)}"}

    return {"response": answer}

