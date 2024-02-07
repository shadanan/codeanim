import ast


def parse(path: str, labels: list[str] | None) -> list[str]:
    with open(path) as f:
        lines = f.read().splitlines()

    codeanim_lines = []
    is_codeanim = False
    for line in lines:
        if line.startswith("```python"):
            tokens = line.strip().split()
            codeanim = len(tokens) > 1 and tokens[1] == "codeanim"
            label = tokens[2] if len(tokens) > 2 else ""
            is_codeanim = codeanim and (labels is None or label in labels)
            continue
        if line == "```":
            is_codeanim = False
            continue
        if is_codeanim:
            codeanim_lines.append(line)

    module = ast.parse("\n".join(codeanim_lines))
    expressions = []
    for node in module.body:
        start = node.lineno - 1
        end = node.end_lineno if node.end_lineno is not None else start
        expressions.append("\n".join(codeanim_lines[start:end]))
    return expressions
