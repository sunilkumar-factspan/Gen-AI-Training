import ast

ALLOWED_PREFIXES = (
    "playwright",
    "time",
)

BLOCKED_IMPORTS = (
    "os",
    "sys",
    "subprocess",
    "requests",
    "asyncio",
)

BLOCKED_KEYWORDS = [
    "eval(",
    "exec(",
    "__import__",
    "open(",
]

def is_safe_code(code: str) -> bool:
    try:
        tree = ast.parse(code)

        for node in ast.walk(tree):

            # 🔒 Handle: import xyz
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name

                    # ❌ Block dangerous imports
                    if name.startswith(BLOCKED_IMPORTS):
                        return False

                    # ✅ Allow only safe modules
                    if not name.startswith(ALLOWED_PREFIXES):
                        return False

            # 🔒 Handle: from xyz import ...
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                # ❌ Block dangerous imports
                if module.startswith(BLOCKED_IMPORTS):
                    return False

                # ✅ Allow only safe modules
                if not module.startswith(ALLOWED_PREFIXES):
                    return False

        # 🔒 Block dangerous patterns
        for keyword in BLOCKED_KEYWORDS:
            if keyword in code:
                return False

        return True

    except Exception:
        return False