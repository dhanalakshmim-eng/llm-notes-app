
import subprocess
import json
import textwrap

OLLAMA_MODEL = "mistral"

def generate_summary_and_keywords(text):
    prompt = f"""
    Summarize the following notes and extract important keywords:
    ---
    {textwrap.shorten(text, width=4000)}
    ---
    Give response in JSON with keys: "summary", "keywords"
    """

    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt.encode(),
            capture_output=True,
            timeout=120
        )
        output = result.stdout.decode()
        try:
            parsed = json.loads(output)
            return parsed
        except:
            return {"summary": output.strip(), "keywords": []}
    except Exception as e:
        return {"error": f"Failed to generate summary: {str(e)}"}
