from google.oauth2 import service_account
from googleapiclient.discovery import build
from shared.config import GOOGLE_CREDENTIALS

def get_doc_text(doc_id):
    creds = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS,
        scopes=["https://www.googleapis.com/auth/documents.readonly"]
    )
    service = build("docs", "v1", credentials=creds)
    doc = service.documents().get(documentId=doc_id).execute()

    text = ""
    for el in doc.get("body", {}).get("content", []):
        for e in el.get("paragraph", {}).get("elements", []):
            text += e.get("textRun", {}).get("content", "")
    return text
