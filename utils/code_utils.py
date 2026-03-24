import re

def extract_code(text):
    if not text:
        return None

    # Match ```python OR ```Python OR ```
    pattern = r"```(?:python|Python)?(.*?)```"

    matches = re.findall(pattern, text, re.DOTALL)

    if matches:
        # Return the longest block (usually most complete)
        code = max(matches, key=len)
        return code.strip()

    return None