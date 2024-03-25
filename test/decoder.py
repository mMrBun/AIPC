import asyncio

from vllm import AsyncEngineArgs, AsyncLLMEngine, SamplingParams
from transformers import AutoTokenizer


async def _generate():
    tokenizer = AutoTokenizer.from_pretrained("/data/models/chatglm3-6b", trust_remote_code=True)
    with open("../configs/templates/chatglm3.jinja", "r", encoding="utf-8") as f:
        tokenizer.chat_template = f.read()
    print(tokenizer.eos_token_id)
    print(tokenizer.pad_token_id)
    engine_args = AsyncEngineArgs(
        model="/data/models/chatglm3-6b",
        trust_remote_code=True,
        max_model_len=1024,
        tensor_parallel_size=1,
    )
    engine = AsyncLLMEngine.from_engine_args(engine_args)
    messages = [{"role": "user", "content": "你好！"}]
    input_ids = tokenizer.apply_chat_template(
        conversation=messages, tokenize=True, add_generation_prompt=True
    )
    sampling_params = SamplingParams(
        temperature=0.7,
        top_p=0.5,
        max_tokens=1024,
        stop_token_ids=[tokenizer.eos_token_id],
    )
    result_generator = engine.generate(
        prompt=None, sampling_params=sampling_params, request_id="0", prompt_token_ids=input_ids
    )
    return result_generator


async def chat():
    result_generator = await _generate()
    async for chunk in result_generator:
        print(chunk)

asyncio.run(chat())
