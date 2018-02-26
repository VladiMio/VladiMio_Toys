import math
import operator as op
from functools import reduce

Symbol = str
List = list
Number = (int, float)

Env = dict  # 环境是{变量: 值}之间的映射


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
