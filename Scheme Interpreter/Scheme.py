import Env


def tokenize(chars):
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(program):
    return read_tokens(tokenize(program))


def read_tokens(tokens):
    if len(tokens) <= 0:
        raise SyntaxError('unexpected EOF while reading')

    first_token = tokens.pop(0)

    if first_token == ')':
        raise SyntaxError('unexpected " ) "')
    elif first_token == '(':
        exp = []
        while tokens[0] != ')':
            exp.append(read_tokens(tokens))
        tokens.pop(0)
        return exp
    else:
        return atom(first_token)


def atom(token):
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return str(token)  # Symbol(token)


def scheme_eval(x, env=Env.global_env):
    """对在某个环境下的表达式进行求值"""
    if isinstance(x, Env.Symbol):  # 变量引用
        return env[x]
    elif not isinstance(x, Env.List):  # 字面常量
        return x
    elif x[0] == 'if':  # 条件
        (_, test, conseq, alt) = x
        exp = (conseq if scheme_eval(test, env) else alt)
        return scheme_eval(exp, env)
    elif x[0] == 'define':  # 定义
        (_, var, exp) = x
        env[var] = scheme_eval(exp, env)
    elif x[0] == 'apply':  # apply
        exp = [x[1]]
        exp.extend([scheme_eval(arg, env) for arg in x[-1][1:]])
        return scheme_eval(exp, env)
    else:  # 过程调用
        proc = scheme_eval(x[0], env)
        args = [scheme_eval(arg, env) for arg in x[1:]]
        return proc(*args)


def repl(prompt='scheme.py> '):
    """REPL的懒人实现。"""
    while True:
        val = scheme_eval(parse(input(prompt)))
        if val is not None:
            print(schemestr(val))


def schemestr(exp):
    "将一个Python对象转换回可以被Scheme读取的字符串。"
    if isinstance(exp, list):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)


repl()
# program = "(define a 1)"
# print(scheme_eval(parse(program)))
# print(scheme_eval(parse("a")))
