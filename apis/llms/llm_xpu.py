import torch
from transformers import AutoTokenizer
from ipex_llm.transformers import AutoModelForCausalLM
from ipex_llm.transformers.streamer import TextIteratorStreamer

model_name_or_path = "D:\\developer\\storage\\models\\Qwen2.5-0.5B-Instruct"
save_path = "D:\\developer\\storage\\models\\Qwen2.5-0.5B-Instruct-4bit"
model = AutoModelForCausalLM.load_low_bit(save_path)
model = model.half().to("xpu")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(save_path,
                                          trust_remote_code=True)
warmup_inputs = tokenizer(["hi"], return_tensors="pt").to("xpu")
model.generate(
    warmup_inputs.input_ids,
    max_new_tokens=10
)


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
