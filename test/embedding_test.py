message = [
    {"role": "user", "content": "你是谁？"},
    {"role": "assistant", "content": "我是一名人工智能助手，可以回答你的问题。"},
]

import json

json_message = json.dumps(message, ensure_ascii=False)
print(json_message)