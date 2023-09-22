from threading import Thread
from typing import Iterator, List, Tuple

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer, AutoModelForTableQuestionAnswering, pipeline
import requests
import pandas as pd

model = "meta-llama/Llama-2-7b-chat-hf"

llama_2_tokenizer = AutoTokenizer.from_pretrained(model, token='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')

model_tapas = "google/tapas-large-finetuned-wtq"
tokenizer_tapas = AutoTokenizer.from_pretrained(model_tapas)
model_tapas = AutoModelForTableQuestionAnswering.from_pretrained(model_tapas)
pipe_tapas = pipeline(
    "table-question-answering", model=model_tapas, tokenizer=tokenizer_tapas
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    torch_dtype=torch.float32,
    device_map='auto',
    trust_remote_code=True,
    offload_folder = 'llama',
    token = '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',
    # load_in_4bit=True
)


DEFAULT_SYSTEM_PROMPT = """\
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.  Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.\
"""
def get_prompt(message: str, chat_history: List[Tuple[str, str]],
               system_prompt: str=DEFAULT_SYSTEM_PROMPT) -> str:
    texts = [f'<s>[INST] <<SYS>>\n{system_prompt}\n<</SYS>>\n\n']
    # The first user input is _not_ stripped
    do_strip = False
    for user_input, response in chat_history:
        user_input = user_input.strip() if do_strip else user_input
        do_strip = True
        texts.append(f'{user_input} [/INST] {response.strip()} </s><s>[INST] ')
    message = message.strip() if do_strip else message
    texts.append(f'{message} [/INST]')
    return ''.join(texts)

def get_input_token_length(message: str, chat_history: List[Tuple[str, str]], system_prompt: str) -> int:
    prompt = get_prompt(message, chat_history, system_prompt)
    input_ids = llama_2_tokenizer([prompt], return_tensors='np', add_special_tokens=False)['input_ids']
    return input_ids.shape[-1]

def run(message: str,
        chat_history: List[Tuple[str, str]],
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        max_new_tokens: int = 1024,
        temperature: float = 1,
        top_p: float = 0.95,
        top_k: int = 50) -> Iterator[str]:
    prompt = get_prompt(message, chat_history, system_prompt)
    inputs = llama_2_tokenizer([prompt], return_tensors='pt', add_special_tokens=False)#.to('cuda')

#     print("token length",len(inputs.tokens()))
    streamer = TextIteratorStreamer(llama_2_tokenizer,
                                    timeout=100.,
                                    skip_prompt=True,
                                    skip_special_tokens=True)
    print("input token length", get_input_token_length(message, chat_history, system_prompt))
    generate_kwargs = dict(
        inputs,
        streamer=streamer,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        top_p=top_p,
        top_k=top_k,
        temperature=temperature,
        num_beams=1,
    )
    t = Thread(target=model.generate, kwargs=generate_kwargs)
    t.start()

    outputs = []
    for text in streamer:
        outputs.append(text)
        yield ''.join(outputs)

def chat(message, history_with_input):
    history = history_with_input[:-1]
    output = run(message, history)
    # try:
    #     first_response = next(generator)
    #     yield history + [(message, first_response)]
    # except StopIteration:
    #     yield history + [(message, '')]
    for response in output:
        pass
    return history + [(message, response)]

def generate_response(user_msg, history, df):
    history.append((user_msg, ''))
#     table_text = f"answer the upcoming questions using following table {sales_100_rows}"
#     table_text = ""
    result_tapas = pipe_tapas(table=df.astype(str), query=user_msg)
    follow_up_text = ""
    if result_tapas['coordinates']:
        required_rows, required_columns = set(), set()
        for r, c in result_tapas['coordinates']:
            required_rows.add(r)
            required_columns.add(c)
        required_table = df.iloc[list(required_rows), :]
        follow_up_text = f" Answer the following question using following table - {required_table.to_string()}\n"
    user_msg = follow_up_text + user_msg
    try:
        history = chat(user_msg, history)
    except:
        history = chat(user_msg, [])
        history[0][1] = "Apology, I had to clear the chat from my memory due to memory constraints\n"+ history[0][1]
    return history