# Business AI Meeting Companion

Windows 11 Gradio app using OpenAI Whisper for local transcription and either Ollama or IBM Watsonx for meeting summaries.

## Setup (PowerShell)

Install Python 3.10 or 3.11, FFmpeg (make sure `ffmpeg -version` works), and optionally Ollama.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
Copy-Item .env.example .env
```

For Ollama, install Ollama from https://ollama.com and run `ollama pull llama3.2`. Keep Ollama running.
For IBM Watsonx, set your own WATSONX_API_KEY and WATSONX_PROJECT_ID in `.env`; IBM lab credentials do not automatically transfer to your PC. You must have access to the configured model.

## Run

```powershell
python app.py
```

Open http://127.0.0.1:7860. Upload or record audio, select provider, then click **Transcribe and summarize**. Reports are saved in `outputs/`.

The first Whisper run downloads model weights. Large recordings can take time, particularly on CPU. If Ollama is not running, summary generation will fail. No transcript is sent to IBM unless IBM Watsonx is selected. Review privacy and consent requirements before recording meetings.
