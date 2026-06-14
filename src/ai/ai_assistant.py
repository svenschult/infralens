import requests


def generate_ai_explanation(finding):
    prompt = f"""
Du bist ein Pentester.

Analysiere diesen Service:

Service: {finding['service']}
Port: {finding['port']}
Version: {finding['version']}
Risiko: {finding['risk']}

Gib eine kurze Einschätzung und nächsten Schritte.
Antworte in maximal 3 kurzen sätzen bitte auf deutsch.
"""

    try:
        response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    },
    timeout=30
)

        result = response.json()
        return result["response"].strip()

    except Exception as e:
        return f"KI Fehler: {e}"