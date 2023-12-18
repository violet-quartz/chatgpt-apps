import gradio as gr
from conversation import Conversation

conv = Conversation(prompt="你是一个做饭助手，用中文回答做菜的问题。你的回答要尽量精简", history_rounds=5)
def reply(message, history):
    error = None
    for attempt in range(3):
        response = conv.ask(message)
        if response['status'] == 'succeeded':
            return response['message']
        else:
            error = response['error']
    return f'Operation failed. {error}'

demo = gr.ChatInterface(reply)
demo.launch()