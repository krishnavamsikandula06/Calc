import ast


class EvalError(ValueError):
    pass


ALLOWED_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a ** b,
    ast.Mod: lambda a, b: a % b,
}

ALLOWED_UNARYOPS = {
    ast.UAdd: lambda a: +a,
    ast.USub: lambda a: -a,
}


def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise EvalError('Only numeric constants are allowed')

    if isinstance(node, ast.Num):
        return node.n

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_BINOPS:
            raise EvalError(f'Operator {op_type.__name__} not allowed')
        left = _eval(node.left)
        right = _eval(node.right)
        return ALLOWED_BINOPS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in ALLOWED_UNARYOPS:
            raise EvalError(f'Unary operator {op_type.__name__} not allowed')
        operand = _eval(node.operand)
        return ALLOWED_UNARYOPS[op_type](operand)

    raise EvalError(f'Unsupported expression: {ast.dump(node)}')


def evaluate(expr: str):
    if not isinstance(expr, str) or not expr.strip():
        raise EvalError('Empty expression')
    try:
        node = ast.parse(expr, mode='eval')
    except Exception as exc:
        raise EvalError('Invalid expression') from exc
    # walk AST to ensure safety: only allow specific node types
    for n in ast.walk(node):
        if not isinstance(n, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant, ast.Load, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.UAdd, ast.USub, ast.Expr)):
            raise EvalError('Disallowed expression element')
    return _eval(node)
