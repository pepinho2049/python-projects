import requests
import re
import json

API_KEY = "get your key"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "mistralai/mistral-7b-instruct:free"  # sau alt model

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "SchoolChatbot"
}

def extract_text_from_response(data):
    
    if not isinstance(data, dict):
        return None

    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        pass

    
    try:
        m = data["choices"][0]["message"]
        if isinstance(m, dict) and "content" in m:
            return m["content"]
    except Exception:
        pass

    
    try:
        return data["choices"][0]["text"]
    except Exception:
        pass


    try:
        return data["choices"][0]["content"][0]["text"]
    except Exception:
        pass


    try:
        texts = []
        for c in data.get("choices", []):
            if isinstance(c, dict):
                for k in ("message", "text", "content"):
                    v = c.get(k)
                    if isinstance(v, str):
                        texts.append(v)
                    elif isinstance(v, dict) and "content" in v and isinstance(v["content"], str):
                        texts.append(v["content"])
                    elif isinstance(v, list):
                        
                        for el in v:
                            if isinstance(el, dict):
                                if "text" in el:
                                    texts.append(el["text"])
                                elif "content" in el and isinstance(el["content"], str):
                                    texts.append(el["content"])
        if texts:
            return "\n\n".join(texts)
    except Exception:
        pass

    return None

def clean_model_tokens(text):
    if text is None:
        return None
    if isinstance(text, (dict, list)):
        text = json.dumps(text, ensure_ascii=False)

    text = str(text)

    
    text = re.sub(r"^\s*<s>\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*</s>\s*$", "", text, flags=re.IGNORECASE)

    
    text = re.sub(r"^\s*\[\\?/?s\]\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*\[\\?/?s\]\s*$", "", text, flags=re.IGNORECASE)

    
    text = re.sub(r"^\s*```+", "", text)
    text = re.sub(r"```+\s*$", "", text)

    
    text = re.sub(r"<\|endoftext\|>", "", text)
    text = re.sub(r"</?s>", "", text)

    
    text = text.strip()

    
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text


print("Chat foarte simplu. Scrie 'exit' pentru a ieși.")
while True:
    user = input("Tu: ").strip()
    if user.lower() == "exit":
        print("La revedere!")
        break

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Ești un asistent prietenos care răspunde clar în română."},
            {"role": "user", "content": user}
        ],
        "max_tokens": 300
    }

    r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=60)
   

    try:
        data = r.json()
    except Exception:
        print("[EROARE] Răspuns JSON invalid:", r.text)
        continue

    raw = extract_text_from_response(data)
    cleaned = clean_model_tokens(raw)
    if cleaned:
        print("BOT:", cleaned, "\n")
    else:
        print("[WARN] Nu am găsit text în răspuns — iată JSON complet pentru debugging:")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        print()
