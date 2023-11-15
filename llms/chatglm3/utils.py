import re


def extract_code(text: str):
    try:
        pattern = r'```([^\n]*)\n(.*?)```'
        matches = re.findall(pattern, text, re.DOTALL)
        return matches[-1][1]
    except Exception as e:
        return None
