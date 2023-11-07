import gradio as gr
import requests

wizard_server, mistral_server = 'https://ldrenteuvo7rdk-80.proxy.runpod.net', 'https://xuqocmk4f2ve75-80.proxy.runpod.net'
model_name_wizard, model_name_mistral = 'WizardLM-13B-V1.2', 'Mistral-7B-v0.1'

def generate_prompt(prompt: str, model_name: str) -> str:
    if model_name == 'WizardLM-13B-V1.2':
        prompt = f"""
        A chat between a curious user and an artificial intelligence assistant. 
        The assistant gives helpful, detailed, and polite answers to the user's 
        questions. USER: {prompt} ASSISTANT: </s>
        """.strip()
    else:
        prompt = f"""
        You are a helpful AI assistant.
        
        USER: {prompt}
        ASSISTANT:

        """.strip()
    return prompt

def make_request(prompt:str, temperature: int, max_new_tokens: int, model_name: str): 
    data = {
        "inputs": prompt,
        "parameters": {"best_of": 1, "temperature":temperature, "max_new_tokens": max_new_tokens},
    }
    headers = {
        "Content-Type": "application/json",
    }
    if model_name == 'WizardLM-13B-V1.2':
        server = wizard_server
    else:
        server = mistral_server
    answer = requests.post(f"{server}/generate", json=data, headers=headers)
    return answer.json()['generated_text'].strip()


def chatbot_response(message, history, model_name, temperature, max_new_tokens):
    if model_name == 1:
        model_name = 'WizardLM-13B-V1.2'
    else:
        model_name = 'Mistral-7B-v0.1' 
    prompt = generate_prompt(message, model_name)
    response = make_request(prompt, temperature, max_new_tokens, model_name)
    return response

with gr.Blocks() as demo:
    gr.Markdown(f"Choose the model: 1 for {model_name_wizard}, 0 for {model_name_mistral}")
    model_name = gr.Slider(0, 1, value=0, step = 1)
    gr.Markdown("You can manipulate the temperature of the model")
    temperature = gr.Slider(0, 1, value=0.1, step = 0.1)
    gr.Markdown("You can manipulate the max tokens of the output of the model")
    max_new_tokens = gr.Slider(512, 4096, value=512, step = 10)
  
    gr.ChatInterface(chatbot_response, additional_inputs=[model_name, temperature, max_new_tokens])

demo.queue().launch(share=True)
