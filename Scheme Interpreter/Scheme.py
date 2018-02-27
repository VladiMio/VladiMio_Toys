import math
import operator as op
from functools import reduce

Symbol = str
List = list
Number = (int, float)


# Env = dict  # 环境是{变量: 值}之间的映射
class Procedure(object):
    """用户定义的Scheme过程。"""

    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args):
        return scheme_eval(self.body, Env(self.parms, args, self.env))


class Env(dict):
    """环境是以{'var':val}为键对的字典，它还带着一个指向外层环境的引用。"""

    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        """寻找变量出现的最内层环境。"""
        return self if (var in self) else self.outer.find(var)
        # if var in self:
        #     return self
        # else:
        #     return self.outer.find(var)


def standard_env():
    """一个包含着一些Scheme标准过程的环境。"""
    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update({
        '+': lambda *x: sum(x),
        '-': lambda *x: x[0] - sum(x[1:]),
        '*': lambda *x: reduce(op.mul, x, 1),
        '/': lambda *x: x[0] / reduce(op.mul, x[1:], 1),
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs,
        'append': op.add,
        # 'apply': lambda x, *y: x(*y),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: list(x),
        'list?': lambda x: isinstance(x, list),
        'map': map,
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env


global_env = standard_env()


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


def scheme_eval(x, env=global_env):
    """对在某个环境下的表达式进行求值"""
    if isinstance(x, Symbol):  # 变量引用
        return env.find(x)[x]
    elif not isinstance(x, List):  # 字面常量
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
    elif x[0] == 'set!':  # 赋值
        (_, var, exp) = x
        env.find(var)[var] = scheme_eval(exp, env)
    elif x[0] == 'lambda':  # 过程
        (_, parms, body) = x
        return Procedure(parms, body, env)
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
