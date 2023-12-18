import gradio as gr
from conversation import Conversation
import time

prompt = "你是一个做饭助手，用中文回答做菜的问题。你的回答要尽量精简"

conv = Conversation(prompt, 5)

def predict(input, history=[]):
    history.append(input)
    error = None
    for attempt in range(3):
        response = conv.ask(input)
        if response['status'] == 'succeeded':
            history.append(response['message'])
            break
        else:
            error = response['error']
            time.sleep(0.1)
    else:
        history.append(f'Sorry, failed to get response.{error}')

    responses = [(u,b) for u,b in zip(history[::2], history[1::2])]
    return responses, history

with gr.Blocks(css="#chatbot{height:500px} .overflow-y-auto{height:600px}") as demo:
    chatbot = gr.Chatbot(elem_id="chatbot")
    state = gr.State([])

    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter")

    txt.submit(predict, [txt, state], [chatbot, state])

demo.launch()

