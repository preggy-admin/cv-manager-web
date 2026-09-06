import os
from openai import OpenAI

class LLMService:
    def __init__(self):
        # We use the Deepseek API key provided by the user
        api_key = os.environ.get('DEEPSEEK_API_KEY')
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com/v1"
        )
        self.model = "deepseek-v4-pro"

    def generate_response(self, system_prompt, history, user_message):
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        for msg in history:
            # Map 'model' to 'assistant' for OpenAI API compatibility
            role = 'assistant' if msg['role'] == 'model' else msg['role']
            messages.append({
                "role": role,
                "content": msg['content']
            })
            
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling Deepseek API: {str(e)}")
            return "I'm sorry, I encountered an error while trying to process your request."

llm_service = LLMService()
