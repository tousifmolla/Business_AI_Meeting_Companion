from pathlib import Path
from datetime import datetime
import gradio as gr
from transcriber import transcribe
from summarizer import summarize

OUTPUTS = Path(__file__).parent / 'outputs'
OUTPUTS.mkdir(exist_ok=True)

def process(audio, model_size, provider):
    try:
        transcript = transcribe(audio, model_size)
        summary = summarize(transcript, provider)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        file = OUTPUTS / f'meeting_{timestamp}.md'
        file.write_text(f'# Meeting Companion Report\n\n## Transcript\n{transcript}\n\n## AI Summary\n{summary}\n', encoding='utf-8')
        return transcript, summary, str(file), 'Completed successfully.'
    except Exception as exc:
        return '', '', None, f'Error: {exc}'

with gr.Blocks(title='Business AI Meeting Companion') as demo:
    gr.Markdown('# Business AI Meeting Companion\nUpload or record audio, transcribe with Whisper, and summarize using Ollama or IBM Watsonx.')
    audio = gr.Audio(sources=['upload', 'microphone'], type='filepath', label='Meeting audio')
    with gr.Row():
        size = gr.Dropdown(['tiny', 'base', 'small', 'medium'], value='base', label='Whisper model')
        provider = gr.Dropdown(['Ollama (local)', 'IBM Watsonx'], value='Ollama (local)', label='Summary provider')
    run = gr.Button('Transcribe and summarize', variant='primary')
    transcript = gr.Textbox(label='Transcript', lines=12)
    summary = gr.Markdown(label='Meeting summary')
    report = gr.File(label='Download meeting report')
    status = gr.Textbox(label='Status', interactive=False)
    run.click(process, inputs=[audio, size, provider], outputs=[transcript, summary, report, status])

if __name__ == '__main__':
    demo.launch(server_name='127.0.0.1', server_port=7860)
