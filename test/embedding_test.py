from torch.profiler import profile, ProfilerActivity
from transformers import AutoTokenizer, TextStreamer, AutoModelForCausalLM
from threading import Thread
import intel_npu_acceleration_library
import torch
import time
import sys

model_id = "D:\developer\storage\models\Qwen2.5-0.5B-Instruct"

model = AutoModelForCausalLM.from_pretrained(model_id, use_cache=True).eval()
tokenizer = AutoTokenizer.from_pretrained(model_id, use_default_system_prompt=True)
# tokenizer.pad_token_id = tokenizer.eos_token_id
streamer = TextStreamer(tokenizer, skip_special_tokens=True)

print("Compile model for the NPU")
model = intel_npu_acceleration_library.compile(model)

query = "你会做什么？"
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": query}
]
prefix = tokenizer.apply_chat_template(messages, add_generation_prompt=True, return_tensors="pt")

generation_kwargs = dict(
    input_ids=prefix,
    streamer=streamer,
    do_sample=True,
    top_p=0.9,
    max_length=1024,
)

print("Run inference")
_ = model.generate(**generation_kwargs)
