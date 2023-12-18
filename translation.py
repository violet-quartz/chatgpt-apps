import gradio as gr
from conversation import Conversation

prompt = "接下来你会收到中文的输入，请把它翻译成英文。"
translator = Conversation(prompt, history_rounds=0)

def chinese_to_english(chinese:str) -> str:
    error = None
    for attempt in range(3):
        response = translator.ask(chinese)
        if response['status'] == 'succeeded':
            return response['message']
        else:
            error = response['error']
    return f'Operation failed. {error}'

demo = gr.Interface(
    title="Translate Chinese to English",
    fn=chinese_to_english, 
    inputs=gr.Textbox(lines=5, placeholder="Enter text"), 
    outputs=gr.Textbox(lines=5, placeholder="Translation")
    )

demo.launch()
