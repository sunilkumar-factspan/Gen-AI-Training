import ast

def is_valid_python(code):
    if not code or not code.strip():
        return False, "Empty code"

    try:
        ast.parse(code)
        return True, None
    except Exception as e:
        return False, str(e)