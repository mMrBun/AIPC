from llms.chatglm3.conversation import preprocess_text, Conversation, Role
from llms.chatglm3.utils import extract_code

SYSTEM_PROMPT = ('你是一位智能AI助手，你叫ChatGLM，你连接着一台电脑，但请注意不能联网。在使用Python'
                 '解决任务时，你可以运行代码并得到结果，如果运行结果有错误，你需要尽可能对代码进行改进。你可以处理用户上传到电脑上的文件，文件默认存储路径是/mnt/data/。')

MAX_LENGTH = 8192
TRUNCATE_LENGTH = 1024


def is_valid_python(code: str) -> bool:
    try:
        code = extract_code(code)
        # 尝试编译代码
        compiled_code = compile(code, '<string>', 'exec')
    except Exception as e:
        # 如果编译失败（例如，代码中包含语法错误），返回False
        return False

    try:
        # 如果编译成功，执行代码
        exec(compiled_code)
    except Exception:
        # 如果执行失败，返回False
        return False

    # 如果编译和执行都成功，返回True
    return True


def main(top_p: float, temperature: float, query: str, client):
    history: list[Conversation] = [Conversation(role=Role.USER, content=query)]

    input_text = preprocess_text(
        SYSTEM_PROMPT,
        None,
        history,
    )
    print("=== Input:")
    print(input_text)
    print("=== History:")
    print(history)

    output_text = ''
    for _ in range(5):
        output_text = ''
        for response in client.generate_stream(
                system=SYSTEM_PROMPT,
                tools=None,
                history=history,
                do_sample=True,
                max_length=MAX_LENGTH,
                temperature=temperature,
                top_p=top_p,
                stop_sequences=[str(r) for r in (Role.USER, Role.OBSERVATION)],
        ):
            output_text += response.token.text
        if is_valid_python(output_text):
            break
    return output_text
