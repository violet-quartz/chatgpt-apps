"""
Conversation with chatgpt. 
Refer to Chat Completions API: 
https://platform.openai.com/docs/guides/text-generation/chat-completions-api.
"""
from typing import Tuple
from openai import OpenAI

client = OpenAI() # Don't forget to set environment variable OPENAI_API_KEY="your-api-key"

class Conversation:
    def __init__(self, prompt: str, history_rounds: int = 3, model: str = 'gpt-3.5-turbo') -> None:
        """
        Args:
        prompt: prompt to set the behavior of assistant throughout the conversation.
        history_rounds: how many rounds of chat are included in history.
        model: which version of chatgpt to use, "gpt-4", "gpt-3.5-turbo" or others.
        """
        self.model = model
        self.prompt = prompt
        self.message_rounds = history_rounds
        self.messages = [{"role": "system", "content": self.prompt}]
        

    def ask(self, question: str) -> Tuple[str, str, int]:
        """
        Args: 
        question: question to ask.

        Returns:
        Dictionary
            'status': 'succeeded',
            'message': Replied message,
            'finish_reason': The reason the model stopped generating tokens,
            'total_tokens': Total number of tokens used,
        for successful reply 
        OR
        Dictionary:
            'status': 'failed',
            'error': error met
        for failed reply.
        """
        try:
            self.messages.append({"role": "user", "content": question})
            response = client.chat.completions.create(
                model = self.model,
                messages = self.messages
            )
        except Exception as e:
            print(e)
            return {'status': 'failed', 'error': e}
        
        message = response.choices[0].message.content
        finish_reason = response.choices[0].finish_reason
        total_tokens = response.usage.total_tokens
        self.messages.append({"role": "assistant", "content": message})
        if len(self.messages) > 1 + 2 * self.message_rounds:
            del self.messages[1:3] # Keep prompt and delete the earliest round.

        return {'status': 'succeeded', 'message': message, 
                'finish_reason': finish_reason, 'total_tokens': total_tokens}


if __name__ == '__main__':
    prompt = 'You are a helpful assistant. Answer the questions in Chinese.'
    print(f'System: {prompt}')
    conv = Conversation(prompt)
    q1 = 'Who won the world series in 2020?'
    print(f'User: {q1}')
    response = conv.ask(q1)
    if response['status'] == 'succeeded':        
        print(f'Assistant: {response["message"]}')
    q2 = 'Where it was played?'
    print(f'User: {q2}')
    response = conv.ask(q2)
    if response['status'] == 'succeeded':        
        print(f'Assistant: {response["message"]}')
          