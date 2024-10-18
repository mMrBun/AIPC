import torch
import time

from transformers import AutoTokenizer, TextGenerationPipeline
from ipex_llm.transformers import AutoModelForCausalLM
from ipex_llm.transformers.streamer import TextIteratorStreamer

model_name_or_path = "D:\\developer\\storage\\models\\Qwen2.5-0.5B-Instruct"
save_path = "D:\\developer\\storage\\models\\Qwen2.5-0.5B-Instruct-4bit"
# Load model in 4 bit,
# which convert the relevant layers in the model into INT4 format
model = AutoModelForCausalLM.load_low_bit(save_path)
model = model.half().to("xpu")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(save_path,
                                          trust_remote_code=True)
warmup_inputs = tokenizer(["hi"], return_tensors="pt").to("xpu")
generated_ids = model.generate(
            warmup_inputs.input_ids,
            max_new_tokens=10
        )
# pipeline = TextGenerationPipeline(model=model, tokenizer=tokenizer, max_new_tokens=32)
# input_str = "Once upon a time, there existed a little girl who liked to have adventures. She wanted to go to places and meet new people, and have fun"
# output = pipeline(input_str)[0]["generated_text"]
# print(f"Prompt: {input_str}")
# print(f"Output: {output}")
# model.save_low_bit(save_path)
# tokenizer.save_pretrained(save_path)
# print(f"Model and tokenizer are saved to {save_path}")

def generate(prompt: str):
    # Generate predicted tokens
    with torch.inference_mode():
        # The following code for generation is adapted from https://huggingface.co/Qwen/Qwen2.5-7B-Instruct#quickstart
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = tokenizer([text], return_tensors="pt").to("xpu")

        streamer = TextIteratorStreamer(tokenizer=tokenizer, skip_prompt=True)
        model.generate(
            model_inputs.input_ids,
            max_new_tokens=1024,
            streamer=streamer
        )
        for chunk in streamer:
            if chunk:
                yield chunk

# generater = generate("Once upon a time, there existed")
# for chunk in generater:
#     print(chunk)