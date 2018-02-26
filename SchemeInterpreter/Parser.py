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


program = "(begin (define r 10) (* pi (* r r)))"
print(parse(program))
