import os
import requests
from dotenv import load_dotenv
load_dotenv()

PROMPT = '''You are a precise meeting assistant. Summarize the transcript below using these headings:
Meeting summary
Key discussion points
Decisions made
Action items (owner and deadline if explicitly stated)
Unresolved questions
Never invent names, dates, decisions or assignments. If none are stated, say "Not specified".

TRANSCRIPT:
{transcript}
'''

def summarize(transcript: str, provider: str) -> str:
    if not transcript.strip():
        raise ValueError('No transcript to summarize.')
    prompt = PROMPT.format(transcript=transcript[:50000])
    if provider == 'Ollama (local)':
        model = os.getenv('OLLAMA_MODEL', 'llama3.2')
        url = os.getenv('OLLAMA_URL', 'http://127.0.0.1:11434').rstrip('/') + '/api/generate'
        response = requests.post(url, json={'model': model, 'prompt': prompt, 'stream': False}, timeout=600)
        response.raise_for_status()
        return response.json()['response'].strip()
    if provider == 'IBM Watsonx':
        from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
        from langchain_ibm import WatsonxLLM
        project_id = os.getenv('WATSONX_PROJECT_ID')
        if not project_id:
            raise ValueError('Set WATSONX_PROJECT_ID in your .env file and configure IBM credentials.')
        llm = WatsonxLLM(
            model_id=os.getenv('WATSONX_MODEL_ID', 'meta-llama/llama-4-maverick-17b-128e-instruct-fp8'),
            url=os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com'),
            project_id=project_id,
            params={GenParams.MAX_NEW_TOKENS: 1000, GenParams.TEMPERATURE: 0.1},
        )
        return llm.invoke(prompt)
    raise ValueError('Unsupported provider.')
