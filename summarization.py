import gradio as gr
from conversation import Conversation

prompt = "接下来用户会输入一段文本，请对文本进行总结，长度缩减至少一半"
summarizer = Conversation(prompt, history_rounds=0)

def summarize(input:str) -> str:
    error = None
    for attempt in range(3):
        response = summarizer.ask(input)
        if response['status'] == 'succeeded':
            return response['message']
        else:
            error = response['error']
    return f'Operation failed. {error}'

demo = gr.Interface(
    title="Summarize Text",
    fn = summarize,
    inputs = gr.Textbox(label='Input', lines=5, placeholder="Enter text"),
    outputs = gr.Textbox(label="Output", lines=3, placeholder="Summarization")
)

demo.launch()
