import discord
import requests
import re
from shared.config import DISCORD_BOT_TOKEN, BASE_URL, ALLOWED_DISCORD_CHANNEL_ID
from shared.document_validation import extract_any_url, extract_doc_id_from_url,extract_google_doc_url

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

last_doc_url = {}

@client.event
async def on_ready():
    print(f"Bot connected as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != int(ALLOWED_DISCORD_CHANNEL_ID):
        return

    content = message.content
    user_id = message.author.id

    google_doc_url = extract_google_doc_url(content)
    any_url = extract_any_url(content)

    # If user shared some URL but NOT a Google Docs URL
    if any_url and not google_doc_url:
        await message.channel.send("Please provide a Google Docs URL to ask questions about.")
        return

    if google_doc_url:
        if not is_valid_google_doc(google_doc_url):
            await message.channel.send(
                "The Google Docs URL you provided is invalid or inaccessible. Please check the link and permissions."
            )
            return

        last_doc_url[user_id] = google_doc_url
        question = content.replace(google_doc_url, "").strip()
        if not question:
            await message.channel.send("Got the document! Let me know if you’d like a summary or have any specific questions.")
            return
    else:
        google_doc_url = last_doc_url.get(user_id)
        question = content.strip()

        if not google_doc_url:
            await message.channel.send("Please provide a Google Docs URL to ask questions about.")
            return
        if not question:
            await message.channel.send("Please ask a question about the document.")
            return

    payload = {
        "question": question,
        "doc_url": google_doc_url
    }

    try:
        response = requests.post(BASE_URL + "query", json=payload)
        response.raise_for_status()
        answer = response.json().get("answer", "Sorry, I couldn't find an answer.")
    except Exception as e:
        answer = f"Error contacting the server: {e}"

    await message.channel.send(answer)

client.run(DISCORD_BOT_TOKEN)
